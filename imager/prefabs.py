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
prefabs = {
        'image_done':
                {'subject': 'Image is done Baking',
                 'body': ('Good Day,\n\n'
                          '  This message is to inform you that the'
                          ' image name:\n"%(name)s"\n\nis complete and'
                          ' %(status)s. The ID of this image is "%(uuid)s".')},
        'crusty_image':
                {'subject': 'Stale Images Found',
                 'body': ('Howdie from the Cloud,\n\n'
                          '  Durring Imaging we found an old crusty image.'
                          ' The Image ID was "%(id)s" and the last time it was'
                          ' updated was "%(updated)s". This image was nuked'
                          ' and we are attempting to'
                          ' create another one. As such you should be aware'
                          ' that the image was found in a "%(status)s" state'
                          ' and was old. So at some point in recent history'
                          ' things were not working as intended.')},
        'never_active':
                {'subject': 'Image Never Went Active',
                 'body': ('Salutations,\n\n'
                          '  I am sorry to say that the image process has'
                          ' failed. The Image ID was "%(id)s" while the process'
                          ' looked like it would succeed, the image never went'
                          ' active. This failed image was nuked, while this can'
                          ' happen for a lot of reasons I would recommend you'
                          ' have a look at the instance to see if you have a'
                          ' bazillion INODES or if the instance is simply'
                          ' taking up too much space, which would make it less'
                          ' than practicle to create instance images. Otherwise'
                          ' you can login and fire off a manual image or see'
                          ' if this happens again on the next run.')},
        'image_fail':
                {'subject': 'Sorry to Say but We have had Failures',
                 'body': ('Dear User,\n\n'
                          '  Its with regret that I inform you that while'
                          ' attempting to create an image of your instance,'
                          ' we have failed. We are not 100 percent sure why'
                          ' this happened, however here is what we do know.'
                          '\n\nERROR = %(data)s\nTRACE = %(trace)s')}
                }

footer = ('\nBest Regards,\n\n--\n\nThe CloudNull Self Imager.'
          ' By Kevin Carter\nCheck me out at http://cloudnull.io\n'
          'Experience... Fanatical Support!\n')
