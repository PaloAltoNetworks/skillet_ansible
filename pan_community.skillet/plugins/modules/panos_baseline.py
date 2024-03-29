#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

#  Copyright 2019 Palo Alto Networks, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

ANSIBLE_METADATA = {'metadata_version': '0.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: panos_baseline
short_description: Load a baseline config
description:
    - This module executes a panos baseline skillet on the target host
    - The baseline configuration is an auto-generated configuration file 
      that contains ONLY the authentication information used to connect 
      to the device and the current network connectivity information, 
      including: IPv4 Address, netmask, default gateway, and DNS servers.
    - This module does not provide guards of any sort, so USE AT YOUR OWN RISK.
    - Refer to the Skillet documentation for more details
    - https://docs.paloaltonetworks.com/pan-os.html

author: "Anna Barone (@abarone)"
version_added: "0.1"

requirements:
    - skilletlib >= 1.0.1

notes:
    - A commit is needed after this module to set the generated baseline
      configuration as the running config.
    - Check mode is not supported.
'''

EXAMPLES = '''
- name: Grab configuration variables
  include_vars: 'vars.yml'
  no_log: 'yes'

- name: Ensure deps are available
  # Ensure we have all the right requirements installed in this environment
  pip:
    name:
      - pan-python
      - pandevice
      - xmltodict
      - requests
      - requests_toolbelt
      - skilletlib

- name: Baselines the FW
  panos_baseline:
    provider: '{{ provider }}'
'''

RETURN = '''
stdout:
    description: output (if any) of the given skillet load's success
    returned: success
    type: string
    sample: "{"changed": true}"
'''

from ansible.module_utils.basic import AnsibleModule

try:
    from skilletlib import Panos
    from skilletlib.exceptions import PanoplyException
except ImportError:
    pass


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        provider=dict(type='dict', required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )

    # create our Panoply device and load baseline config
    try:
        device = Panos(api_username=module.params['provider']['username'],
                       api_password=module.params['provider']['password'],
                       hostname=module.params['provider']['ip_address']
                       )
        if not device.load_baseline():
            module.fail_json(msg='Could not load baseline config')

        module.exit_json(changed=True)

    except PanoplyException as p:
        module.fail_json(msg='{0}'.format(p))


if __name__ == '__main__':
    main()
