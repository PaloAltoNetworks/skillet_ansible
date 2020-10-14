#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

#  Copyright 2020 Palo Alto Networks, Inc
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
module: panos_validate 
short_description: Execute 'pan_validation' type skillet 
description:
    - This module executes a panos skillet on the target host
    - This module does not provide guards of any sort, so USE AT YOUR OWN RISK.
    - Refer to the Skillet documentation for more details
    - https://docs.paloaltonetworks.com/pan-os.html
    
author: "Andrew Mallory (@andrewmallory)"
version_added: "0.1"

requirements:
    - skilletlib >= 0.3.9.6

notes:
    - Check mode is not supported.

options:
    skillet:
        description:
            - The id of the skillet to execute
        required: True
    
    skillet_path:
        description:
            - The path where one or more skillets will be loaded from
        required: True

    vars:
        description:
            - a dict of variables as required by the skillet to be executed
            - If no vars are given then the default values from the skillet are used
        required: False
        type: complex
        
'''

EXAMPLES = '''
- name: Grab configuration variables
  include_vars: 'vars.yml'
  no_log: 'yes'

- name: Executes IronSkillet Validation
  panos_validate::
    provider: '{{ provider }}'
    skillet: validate-IronSkillet-v10_0-panos-bae945bc-c667-4e56-a3fc-73bbb5afbe0d
    skillet_path: /var/tmp/skillets/iron-skillet
    vars: '{{ skillet_vars }}'
'''

RETURN = '''
stdout:
    description: output (if any) of the given skillet as JSON formatted string
    returned: success
    type: string
    sample: "{entry: {@name: dmz-block, ip-netmask: 192.168.55.0/24, description: Address CIDR for sales org}}"
'''


from ansible.module_utils.basic import AnsibleModule

try:
    from skilletlib import SkilletLoader
    from skilletlib.exceptions import PanoplyException
    import json

except ImportError:
    pass


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        skillet=dict(type='str', required=True),
        skillet_path=dict(type='str', required=True),
        vars=dict(type='dict'),
        provider=dict(type='dict', required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )

    # create our context dict. Every skillet requires a context that contains connection information
    # as well as any vars required for that particular skillet

    skillet_context = dict()
    skillet_context.update(module.params['vars'])
    skillet_context.update(module.params['provider'])

    skillet_loader = SkilletLoader(module.params['skillet_path'])

    skillet = skillet_loader.get_skillet_with_name(module.params['skillet'])

    if skillet is None:
        module.fail_json(msg='Could not find Skillet with name {0}'.format(module.params['skillet']))

    # refuse to run any non panos / panorama skillet types
    if not skillet.type == 'pan_validation':
        module.fail_json(msg='Invalid Skillet Type')

    try:
        output = skillet.execute(skillet_context)
        output_str = json.dumps(output)

        for snippet in output['pan_validation']:
            if not output['pan_validation'][snippet]['results']:
                module.fail_json(msg=output_str)

        module.exit_json(changed=False, stdout=output_str)

    except PanoplyException as p:
        module.fail_json(msg='{0}'.format(p))


if __name__ == '__main__':
    main()

