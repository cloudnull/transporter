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
import time
import traceback
import sys
from bookofnova import computelib
from imager import utils


class UnknownStatusError(Exception):
    pass


class FiveHundredApiinfor(Exception):
    pass


class NovaFunctionalLogic(object):
    def __init__(self, logger, args):
        """
        Perform NOVA Commands and then make sure I was not dumb about it
        """
        self.logger = logger
        self.args = args

    def nova_errors(self, status, nova=None, action=None, optional=None):
        """
        Check for errors and see if there were issues. Return False if there
        were problems, return True if all is well.
        """
        if 'nova_status' in status and 'nova_reason' in status:
            msg = ('API ERROR ==> %s ==> %s'
                   % (status['nova_status'], status['nova_reason']))
        else:
            msg = ('Shits Broke API is Busted. Here is what I do know ==> %s'
                   % status)

        if status['nova_status'] > 500:
            self.logger.critical(msg)
            return False
        elif status['nova_status'] == 413:
            self.logger.warn(msg)
            if ('retry-after' in status['nova_reason'] and
                int(status['nova_reason']['retry-after']) == 0):
                info = ('We recieved a Nova error 413 and the retry length was'
                        ' 0. Generally this is because the compute node is out'
                        ' of resources, as such. I died. here are some details'
                        ' on the Status Data ==> %s' % status)
                self.logger.error(info)
                return False
            else:
                _time = int(status['nova_reason']['retry-after'])
                time.sleep(_time)
                if nova:
                    nova.re_authenticate()
                return False
        elif status['nova_status'] == 401:
            self.logger.warn(msg)
            if nova:
                nova.re_authenticate()
            return False
        elif status['nova_status'] == 404:
            if action == 'nuker':
                self.logger.info('Image ID "%s" was not found, likely'
                                 'already Gone' % optional)
                return True
            else:
                info = ('API Action URI Not Found Info we have ==> %s' % status)
                self.logger.warn(info)
            return False
        elif status['nova_status'] == 409:
            self.logger.warn(('API ERROR ==> %s ==> Imaging is in process,'
                              ' please wait, or manuallly delete the present'
                              ' image and try again' % status['nova_status']))
            sys.exit()
        elif status['nova_status'] >= 300:
            self.logger.warn(msg)
            return False
        else:
            return True

    def os_auth(self):
        """
        Perform Authentication and Provide a pre-authenticated Nova method
        """
        for retry in utils.retryloop(attempts=2, timeout=120, delay=15):
            try:
                nova = computelib.NovaCommands(m_args=self.args,
                                               output=self.logger)
                auth_dict = nova.auth()
                error_check = self.nova_errors(status=auth_dict,
                                               action='authentication')
                if error_check:
                    return nova
                else:
                    try:
                        retry()
                    except utils.RetryError:
                        self.logger.critical('NOVA Logic Failed to perform'
                                             ' an error check')
                        return False
            except Exception:
                self.logger.warn(traceback.format_exc())
                try:
                    retry()
                except utils.RetryError:
                    self.logger.critical('Failed to Authenticate after'
                                         ' multiple retries')
                    return False

    def list_image(self, nova):
        """
        List all of the instances using details
        """
        for retry in utils.retryloop(attempts=2, timeout=120, delay=15):
            self.logger.info('Listing Images')
            try:
                nova_list = nova.image_list_detail()
                error_check = self.nova_errors(status=nova_list,
                                               action='nova_list')
                if error_check:
                    return nova_list['nova_resp']
                else:
                    try:
                        retry()
                    except utils.RetryError:
                        return False
            except Exception:
                self.logger.critical('Error While Listing Instances')
                try:
                    retry()
                except utils.RetryError:
                    self.logger.critical('Failed Retry loop while listing'
                                         ' an images')
                    return False

    def destroy_image(self, image_id, nova):
        """
        Delete a running instance.
        """
        try:
            for retry in utils.retryloop(attempts=2,
                                              timeout=120,
                                              delay=15):
                self.logger.warn('Destroying Image ID "%s"' % image_id)
                try:
                    nuked = nova.image_nuker(image_id)
                    error_check = self.nova_errors(status=nuked,
                                                   action='nuker',
                                                   optional=image_id)
                    if error_check:
                        return True
                    else:
                        try:
                            retry()
                        except utils.RetryError:
                            self.logger.critical('Failed Retry loop while'
                                                 ' nuking image')
                            return False
                except Exception:
                    error = traceback.format_exc()
                    self.logger.error('Issues while Destroying Image\n\n%s'
                                      % error)
                    try:
                        retry()
                    except utils.RetryError:
                        self.logger.critical('Failed Retry loop while'
                                             ' destoying an image')
                        return False
        except utils.RetryError:
            self.logger.critical('Failed Retry loop while deleting an image')
            return False

    def image_create(self, nova, server_id, img_name, meta_data=None):
        """
        Create an image of a server
        """
        for retry in utils.retryloop(attempts=2, timeout=120, delay=15):
            self.logger.info('Listing Instaces')
            try:
                nova_img = nova.image_create(server_id, img_name, meta_data)
                error_check = self.nova_errors(status=nova_img,
                                               action='nova_list')
                if error_check:
                    return True
                else:
                    try:
                        retry()
                    except utils.RetryError:
                        return False
            except Exception:
                self.logger.critical('Error While Creating Image')
                try:
                    retry()
                except utils.RetryError:
                    self.logger.critical('Failed Retry loop'
                                         ' while creating Image')
                    return False

    def status_active(self, image_id, nova):
        """
        Wait for an image to go active.
        """
        status_counter = 0
        for retry in utils.retryloop(attempts=200, timeout=1800, delay=20):
            self.logger.info('Image "%s" is waiting for an'
                             ' "ACTIVE" state' % image_id)
            try:
                _data = nova.image_info(image_id)
                _info = _data['nova_resp']['image']
                error_check = self.nova_errors(status=_data,
                                               action='status_active',
                                               optional=image_id)
                if not error_check:
                    status_counter += 1
                    if status_counter >= 5:
                        return False
                    else:
                        self.logger.error('we recieved a fatal error when'
                                   ' attempting to poll the Status'
                                   ' of Image "%s" If this does'
                                   ' not change in a few attempts we'
                                   ' will rebuild the failing node,'
                                   ' current FAIL COUTER is "%s"'
                                   % (image_id, status_counter))
                        try:
                            retry()
                        except utils.RetryError:
                            self.logger.critical('There was a problem with'
                                                 ' waiting on the the Image'
                                                 ' to go active')
                            return False
                else:
                    status = _info['status'].upper().encode('utf8')
                    if status == "ERROR":
                        self.logger.error('The Image "%s" has gone into an'
                                   ' "ERROR" during the imaging process'
                                   % image_id)
                        return False
                    elif status != "ACTIVE":
                        try:
                            retry()
                        except utils.RetryError:
                            self.logger.critical('The image NEVER went active,'
                                       ' and we were not able to'
                                       ' accomplish the imaging after'
                                       ' 200 attempts. Here is the'
                                       ' error that we had ERROR\t:'
                                       '%s ==> %s'
                                       % (_data['nova_status'],
                                          _data['nova_reason']))
                            return False
                    else:
                        data = {}
                        data['name'] = _info['name']
                        data['status'] = _info['status']
                        data['uuid'] = _info['id']
                        return data

            except Exception:
                self.logger.critical('When POLL\'ing HOST ==> "%s" we'
                                     ' encountered an error. Will retry again.'
                                     % image_id)
                try:
                    retry()
                except utils.RetryError:
                    self.logger.critical('Failed Retry loop while'
                               ' booting an instance')
                    return False
