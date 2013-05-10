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
configfile = """
# ================================= NOTES ======================================
# Use this configuration file to store sensitive information
# The config file REQUIRES at least ONE section for functionality
# Section names don't matter, however they are nice for oganizing data
# This is a sample file not all variables are needed. Use what you want too.
# The basic Healing system requires a database to store checks and instance
# information.

# Place me in "%(full_path)s" with permissions "0600" or "0400"

# Note: Not all variables are needed, simply use what you need to. If you give
# the system mail relay information you will get notices when images are
# created, or issues happen. DO NOT USE "os_password" and "os_apikey" together,
# choose one or the other.

# Available System variables :
# ------------------------------------------------------------------------------
# log_level = [info,error,warn,debug]  +  mail-main-contact = WhoReadsEmail
# os_user = YOU                        +  mail_debug = True | False
# os_apikey = SuperSecretInformation   +  mail_url = AURL
# os_auth_url = Authentication URL     +  mail_user = Username
# os_rax_auth = A-LOCATION             +  mail_password = Password
# os_verbose = True | False            +  mail_cert = /location/cert
# os_password = SuperSecretInformation +  mail_key = KeyForCert
# os_tenant = UsernameGenerally        +  mail_tls = True | False
# os_version = v2.0                    +  mail_port = Port Number
# os_region = %(region)s
# ================================= NOTES ======================================

[basic]
log_level = info

[openstack]
os_user = YOU
os_apikey = RANDOM-NUMBERS-AND-THINGS
os_rax_auth = %(region)s

#[Mail]
#mail_user =
#mail_password =
#mail_cert =
#mail_key =
#mail_tls =
#mail_port =
#mail_url =
"""
