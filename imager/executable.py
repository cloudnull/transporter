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
import sys
import traceback

# Local Modules
from imager import arguments, imaging, logger


def run_imager():
    """
    Basic Method for starting the application from the launcher
    """
    # Set the Parsed Args
    args = arguments.get_all_the_values()
    try:
        log = logger.load_in(log_level=args['log_level'])
        imaging.InstanceImager(log=log, p_args=args)
    except KeyboardInterrupt:
        sys.exit('AHH FAIL! You Killed me!')
    except Exception:
        print(traceback.format_exc())
        sys.exit('Major FAILURE, please check logs')


if __name__ == '__main__':
    # Run main if the application is executed from the CLI without the launcher
    run_imager()
