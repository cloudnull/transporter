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
import argparse
import sys
import os

# Local Modules
from imager import systemconfig, info


def get_all_the_values():
    """
    Look for flags, these are all of the available options.
    """
    parser = argparse.ArgumentParser(
        formatter_class=lambda
        prog: argparse.HelpFormatter(prog,
                                     max_help_position=31),
        usage='%(prog)s',
        description=info.__description__,
        argument_default=None,
        epilog=info.VINFO)

    # Positional Groups being used
    openstack = parser.add_argument_group(title='OpenStack Arguments',
                                           description=('Optional Arguments'
                                                        ' for use with'
                                                        ' OpenStack. NOTE:'
                                                        ' ALL of the Openstack'
                                                        ' Credentials need to'
                                                        ' go into the system-'
                                                        'config file.'))

    mail = parser.add_argument_group(title='Mail Credentials',
                                           description=('Used for external '
                                                        'Mail notifications'
                                                        ))

    parser.add_argument('--system-config',
                        type=str,
                        required=True,
                        metavar='[Path]',
                        default=None,
                        help=('Uses a System Config File, for all'
                              ' checks, any available MySQL DBs, and'
                              ' OpenStack Credentials'))

    parser.add_argument('--log-level',
                        default='info',
                        choices=['debug',
                                 'info',
                                 'warn',
                                 'error',
                                 'critical'],
                        help='Set Log Verbosity')

    parser.add_argument('--image-name',
                        required=True,
                        type=str,
                        help='Set the name of the image')

    mail.add_argument('--mail-password',
                      type=str,
                      metavar='[Mail_Pasword]',
                      default=None,
                      help='Password for the Mail Server')

    mail.add_argument('--mail-user',
                      type=str,
                      metavar='[MailUser]',
                      default=None,
                      help='Username for the mail Account')

    mail.add_argument('--mail-url',
                      type=str,
                      metavar='[MailURL]',
                      default=None,
                      help='URL to the Mail Server')

    mail.add_argument('--mail-port',
                      type=str,
                      metavar='[MailPort]',
                      default=None,
                      help='Por the Mail Server will use')

    mail.add_argument('--mail-tls',
                      action='store_true',
                      default=None,
                      help='Does the Mail Server use TLS')

    mail.add_argument('--mail-key',
                      type=str,
                      metavar='[HostIP]',
                      default=None,
                      help='If using TLS is their a Key File')

    mail.add_argument('--mail-cert',
                      type=str,
                      metavar='[HostIP]',
                      default=None,
                      help='If Using TLS is their a Cert File')

    mail.add_argument('--mail-main-contact',
                      metavar='[Email@Address]',
                      default=None,
                      help='Who should I notify')

    mail.add_argument('--mail-debug',
                      action='store_true',
                      default=None,
                      help='Makes the SMTP Service Noisy')

    openstack.add_argument('--os-version',
                           metavar='[VERSION_NUM]',
                           default='v2.0',
                           help='env[OS_VERSION]')

    openstack.add_argument('--os-verbose',
                            action='store_true',
                            default=None,
                            help=('Make the OpenStack Authentication'
                                  ' Verbose'))

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit('Give me something to do and I will do it')

    # Parse the Arguments that have been provided
    args = parser.parse_args()

    # Change Arguments in to a Dictionary
    args = vars(args)

    # Parse Config File
    if args['system_config']:
        args = (systemconfig.ConfigureationSetup(args).config_args())

    # Check to see if the user Running the application is allowed to do so.
    user = os.getuid()
    if user != 0:
        sys.exit('This program requires root privileges."')

    # Return My Arguments and begin Monitoring
    return args
