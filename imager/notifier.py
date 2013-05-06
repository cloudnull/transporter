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
import smtplib
import time
from email.mime.text import MIMEText
import traceback

from imager.info import __appname__
from imager import utils, prefabs, get_instance_name


class Mailer(object):
    def __init__(self, notice, args, logger):
        """
        Send a message to the system administrator about and issues that may
        be happening. If Email is detected as a no go, the system will log the
        message.
        """
        self.logger = logger
        _notice = {'time': '%s UTC' % time.strftime("%H:%M").lstrip(),
                   'random_string': utils.rand_string(),
                   'appname': __appname__,
                   'contact': args['mail_main_contact']}

        for _kv in notice.keys():
            _notice[_kv] = notice[_kv]
        self.notice = _notice
        self.msg = prefabs.prefabs[self.notice['reason']]
        self.body = self.msg['body'] % self.notice

        # Set Mailer Tuple, to work all values have to be true
        mailer = (args['mail_url'],
                  args['mail_password'],
                  args['mail_user'],
                  args['mail_port'])
        if all(mailer):
            # Auth details for the Mail Server
            smtppath = '%s' % mailer[0]
            password = '%s' % mailer[1]
            username = '%s' % mailer[2]
            smtpport = '%s' % mailer[3]

            self.smtp = smtplib.SMTP(host=smtppath, port=smtpport)
            if args['mail_tls']:
                if args['mail_key'] and args['mail_cert']:
                    keyfile = args['mail_key']
                    certfile = args['mail_cert']
                    self.smtp.starttls(keyfile, certfile)
                else:
                    self.smtp.starttls()

            if username and password:
                self.smtp.login(user=username, password=password)
            elif username and not password:
                self.smtp.login(user=username, password=None)
            elif not username and password:
                self.smtp.login(user=None, password=password)
            else:
                self.smtp.login(user=None, password=None)

            if args['mail_debug']:
                self.smtp.set_debuglevel(True)

            # Deliver Cus Messages
            self.cus_messages()

            # Stop SMTP
            self.smtp.quit()
        else:
            self.logger.warn('No mail facility has been set. So no notification'
                             ' is being sent. Message would have been ==>\t'
                             ' "%s"' % self.body)

    def cus_messages(self):
        """
        Generate Customer Emails
        """
        try:
            mailbody = self.body
            self.logger.info(mailbody)
            customer_message = mailbody + prefabs.footer
            customer_message = customer_message.encode('utf8')
            hostname = get_instance_name()
            em_msg = MIMEText(customer_message, 'plain', None)
            em_msg["Subject"] = '%s - %s' % (self.msg["subject"], __appname__)
            em_msg["From"] = "%s@%s" % (__appname__, hostname)
            em_msg["To"] = self.notice['contact']
            em_msg["Reply-To"] = 'DoNotReply@%s' % hostname

            self.logger.info('Delivering email to %(contact)s at "%(time)s for'
                             ' %(reason)s"' % self.notice)

            # Send Customer Messages
            self.smtp.sendmail(em_msg["From"],
                               [em_msg["To"]],
                               em_msg.as_string())
        except Exception:
            self.logger.warn('Mail Failed to deliver, Error'
                             ' Providing Messaging Services\n\n%s'
                             % traceback.format_exc())
