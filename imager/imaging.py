# ==============================================================================
# Copyright [2013] [Kevin Carter]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import sys
import traceback
from subprocess import Popen, PIPE

from imager import novafunctions, utils, notifier, get_instance_name


class ImagingInProcess(Exception):
    pass


class GeneralImagerFailure(Exception):
    pass


class InstanceImager(object):
    def __init__(self, log, p_args):
        """
        Access Nova and create an image of the instance.
        """
        self.m_args = p_args
        self.log = log
        self._nova = novafunctions.NovaFunctionalLogic(logger=log, args=p_args)
        self.nova = self._nova.os_auth()
        self.uuid = self.get_instance_id()
        self.name = get_instance_name()
        tag = 'CloudNull_imageizer'
        self.image_name = '%s_%s_%s_%s' % (self.name,
                                           self.m_args['image_name'],
                                           self.uuid,
                                           tag)
        self.check_for_image()
        self.create_image()

    def commander(self, cmd):
        """
        Run sub-process (SHELL) commands.
        """
        output = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
        stdout, stderr = output.communicate()
        if stderr:
            raise GeneralImagerFailure(stderr)
        return stdout.strip()

    def get_instance_id(self):
        """
        Get the UUID of the instance that we want to make an image of
        """
        # Check to see if this application will be run as a Daemon
        try:
            xen_s = self.commander(cmd='which xenstore')
            dom_id = self.commander(cmd='%s read domid' % xen_s)
            slice_id = self.commander(cmd='%s read /local/domain/%s/name'
                                      % (xen_s, dom_id))
            slice_id = slice_id.split('-', 1)[1]
            return slice_id
        except Exception:
            _tb = traceback.format_exc()
            self.log.error(_tb)
            sys.exit('%s\n\nSub Process FAILURE!!!' % _tb)

    def check_for_image(self):
        from datetime import datetime as dt, timedelta
        from dateutil import parser
        try:
            img = self._nova.list_image(nova=self.nova)
            for obj in img['images']:
                if (obj['name'] == self.image_name and
                    obj['status'].upper() == 'ACTIVE'):
                    self._nova.destroy_image(image_id=obj['id'],
                                             nova=self.nova)
                elif (obj['name'] == self.image_name and
                    obj['status'].upper() == 'SAVING'):
                    time = obj['updated']
                    _tm = time.replace('Z', '')
                    _time = parser.parse(_tm)
                    _now = dt.utcnow()
                    if (_now - _time) > timedelta(hours=5):
                        obj['reason'] = 'crusty_image'
                        self.notify_me(obj)
                        self._nova.destroy_image(image_id=obj['id'],
                                                 nova=self.nova)
                    else:
                        raise ImagingInProcess('Image ID "%s"' % obj['id'])
        except ImagingInProcess, exp:
            self.log.info('Imaging is presently in progress. %s' % exp)

    def create_image(self):
        try:
            randkey = utils.rand_string()
            self._nova.image_create(nova=self.nova,
                                    server_id=self.uuid,
                                    img_name=self.image_name,
                                    meta_data={'cloudnull': randkey})
            img = self._nova.list_image(nova=self.nova)
            for obj in img['images']:
                if (obj['name'] == self.image_name and
                    obj['status'].upper() == 'SAVING' and
                    'cloudnull' in obj['metadata'] and
                    obj['metadata']['cloudnull'] == randkey):
                    imid = obj['id']
            if imid:
                data = self._nova.status_active(image_id=imid, nova=self.nova)
                if data:
                    data['reason'] = 'image_done'
                    self.notify_me(data)
                else:
                    self._nova.destroy_image(image_id=imid,
                                             nova=self.nova)
                    data['reason'] = 'never_active'
                    self.notify_me(data)
                    raise GeneralImagerFailure('We Failed waiting for image %s'
                                               ' to go active' % imid)
        except Exception, exp:
            data = {'reason': 'image_fail',
                    'data': exp,
                    'trace': traceback.format_exc()}
            self.notify_me(data)

    def notify_me(self, notice):
        notifier.Mailer(notice=notice,
                        args=self.m_args,
                        logger=self.log)
        del notice
