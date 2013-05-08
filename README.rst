Transporter
###########
:Date: 2012-03-08 16:22
:Tags: Openstack, Nova Compute, Nova, Glance, Imaging, XenServer
:Category: \*nix
:Author: Kevin Carter


Create an Image from within an Instance
=======================================

General Overview
----------------

This application has been created to work with Openstack if using the XenServer Hypervisor. At this time the code base supports Openstack as a whole, whoever the application has only been tested on Rackspace Cloud Servers. 

Overview:
---------

*XenOsImager* will create an image from information obtained from within the instance. The application will look at the "*xenstore*" data to determine the UUID of the instance, and the region. The user is only required input their OpenStack API Credentials into a simple configuration file. These credentials are only used to make API calls for image creation.

Simply the application will allow you to create images of instances as a simple automation task; CRON job, on demand, or anythine else you can think of.


Prerequisites :
  * Python => 2.6 but < 3.0
  * python-setuptools


Installation is simple :

  from Python.org, IE "pip"


    .. code-block:: bash

        pip install xenosimager


  from Github, which is Trunk.


    .. code-block:: bash

        git clone git://github.com/cloudnull/transporter.git
        cd transporter
        python setup.py install


Setup is Simple too edit the file "/etc/xenosimager/config.cfg" :

    .. code-block:: bash

        vi /etc/xenosimager/config.cfg


In the previous file, add your credentials. If you feel so inclined, you can also add your mail relay information and the system will send you a message when the images are created or if there are overall issues. 


Available Options in the config file or on the CLI : 


Required Variables from CLI
---------------------------

 - ``system-config`` | Where your config file exists
 - ``image-name`` | the name of the image


OpenStack Variables
-------------------

 - ``os_user`` | YOU
 - ``os_apikey`` | SuperSecretInformation
 - ``os_auth_url`` | Authentication URL
 - ``os_rax_auth`` | A-LOCATION
 - ``os_verbose`` | True or False
 - ``os_password`` | SuperSecretInformation
 - ``os_tenant`` | UsernameGenerally
 - ``os_region`` | WhereIsThisInstance
 - ``os_version`` | v2.0


Mail Variables
--------------

 - ``mail-main-contact`` | WhoReadsEmail
 - ``mail_debug`` | True or False
 - ``mail_url`` | AURL
 - ``mail_user`` | Username
 - ``mail_password`` | Password
 - ``mail_cert`` | /location/cert
 - ``mail_key`` | KeyForCert
 - ``mail_tls`` | True or False
 - ``mail_port`` | Port Number


How to use this tool
--------------------

Application is simple to use. Simply follow this command and add your own custom name to the end.

    .. code-block:: bash

        xenosimager --system-config /etc/xenosimager/config.cfg --image-name $NAME_OF_THE_IMAGE


Logs are created for all interaction of the imager, and can be found here :

    .. code-block:: bash

        /var/log/xenosimager.log


For automated image create please have a look at the example.cron.txt file, which is where you can find cron job examples, but with little to no ingenuity I am sure you could figure out other methods for automated command execution.


Get Social
----------

* Downloadable on PyPi_
* Downloadable on GitHub_
* See My `GitHub Issues Page`_ for any and all Issues or Feature requests

.. _PyPi: https://pypi.python.org/pypi/transporter
.. _GitHub: https://github.com/cloudnull/transporter
.. _GitHub Issues Page: https://github.com/cloudnull/transporter/issues

See ``https://github.com/cloudnull/transporter/issues`` for Issues or Feature requests


License
_______

Copyright [2013] [Kevin Carter]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.