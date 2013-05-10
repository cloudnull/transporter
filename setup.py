#!/usr/bin/env python
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
import setuptools
import sys
import os
import tarfile
import time
from subprocess import Popen, PIPE

# Local Packages
from imager import strings, info


# Check the version of Python that we have been told to use
if sys.version_info < (2, 6, 0):
    sys.stderr.write('The Ameba System Presently requires'
                     ' Python 2.6.0 or greater\n')
    sys.exit('\nUpgrade python because your version of it is VERY deprecated\n')

with open('README') as r_file:
    long_description = r_file.read()

setuptools.setup(
    name=info.__appname__,
    version=info.__version__,
    author=info.__author__,
    author_email=info.__email__,
    description=info.__description__,
    install_requires=['bookofnova', 'python-dateutil==1.3.0', 'argparse'],
    packages=['imager'],
    long_description=long_description,
    license=info.__license__,
    url=info.__urlinformation__,
    classifiers=[
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    entry_points={
        "console_scripts":
            ["%s = imager.executable:run_imager" % info.__appname__]
    }
)


def config_files_setup(conf=strings.configfile):
    print('Moving the the System Config file in place')
    # setup will copy the config file in place.
    name = 'config.cfg'
    path = '/etc/%s' % info.__appname__
    full = '%s%s%s' % (path, os.sep, name)

    str_v = {'full_path': full}

    xen_s = commander(cmd='which xenstore')
    dom_id = commander(cmd='%s read domid' % xen_s)
    region = commander(cmd=('%s read /local/domain/%s/vm-data'
                            '/provider_data/region'
                            % (xen_s, dom_id)))
    if region:
        str_v['region'] = region.upper()
    else:
        str_v['region'] = 'WhereIsThisInstance'

    conf_file = strings.configfile % str_v

    if not os.path.isdir(path):
        os.mkdir(path)
        with open(full, 'w+') as conf_f:
            conf_f.write(conf_file)
    else:
        if not os.path.isfile(full):
            with open(full, 'w+') as conf_f:
                conf_f.write(conf_file)
        else:
            print('Their was a configuration file found, I am compressing the '
                  'old version and will place the new one on the system.')
            not_time = time.time()
            backupfile = '%s.%s.backup.tgz' % (full, not_time)
            tar = tarfile.open(backupfile, 'w:gz')
            tar.add(full)
            tar.close()
            with open(full, 'w+') as conf_f:
                conf_f.write(conf_file)
    if os.path.isfile(full):
        os.chmod(full, 0600)
    print('Configuration file is ready.  Please set your credentials in : %s'
          % full)


def commander(cmd):
    """
    Run sub-process (SHELL) commands.
    """
    output = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
    stdout, stderr = output.communicate()
    stdout = stdout.strip()
    if stderr:
        stdout = None
    return stdout


if len(sys.argv) > 1:
    if sys.argv[1] == 'install':
        # Run addtional Setup things
        config_files_setup()
