# skillet-ansible

Collection for working with Skillets


See: [Skillet District](https://live.paloaltonetworks.com/t5/skillet-district/ct-p/Skillets) for more information.

## Example Tasks

Test

The general usage is to first clone / update the desired skillet repository into a specific directory. Then call
`panos_skillet` passing in the directory in which to search for Skillets, and the name of the skillet you want to 
execute.

Because each skillet will specify it's own set of required and optional variables, a handy short-cut is to just pass
in all hostvars as the 'vars' parameters. This will allow you to construct a vars file elsewhere with the desired
variable values. 


```yaml

- hosts: localhost
  connection: local
  gather_facts: false
  collections:
    - paloaltonetworks.panos
    - pan_commnunity.skillet

  vars:
    provider:
      ip_address: '{{ ip_address }}'
      username: '{{ username }}'
      password: '{{ password }}'

  tasks:
    - name: Download the latest templates
      git:
        repo: 'https://github.com/PaloAltoNetworks/iron-skillet.git'
        dest: '{{ playbook_dir }}/files'
        version: '{{ branch }}'

    - name: Include User Variables
      include_vars: vars/main.yml

    - name: Execute Skillet
      pan_community.skillet.panos_skillet:
        skillet_path: '{{ playbook_dir }}/files'
        skillet: '{{ skillet }}'
        provider: '{{ provider }}'
        vars: '{{ hostvars["localhost"] }}'
      register: skillet_output

```


Example of Validation:

```yaml

- hosts: localhost
  connection: local
  gather_facts: false
  collections:
    - paloaltonetworks.panos
    - pan_commnunity.skillet
  vars:
    provider:
      ip_address: '{{ ip_address }}'
      username: '{{ username }}'
      password: '{{ password }}'
  tasks:
    - name: Include User Variables
      include_vars: vars/main.yml
    - name: Show System State
      panos_op:
        provider: '{{ provider }}'
        cmd: 'show system state'
      register: system_state
    - name: execute stig validation skillet
      pan_community.skillet.panos_validate:
        skillet_path: '{{ playbook_dir }}/stig/stig_validation'
        skillet: 'stig_validation'
        provider: '{{ provider }}'
        vars: '{{ skillet_vars }}'
      register: skillet_output
    - name: validation output
      debug: msg="{{ (skillet_output.stdout | from_json).pan_validation }}"

```

Example vars file:

```yaml

---
# provider information for PAN-OS NGFW
ip_address: '10.10.10.10'
username: 'admin'
password: 'super_secret !'
# Variables to pass to the Validation / Configuration Skillet
# These are used to render configuration templates and/or control
# logic flow
skillet_vars:
  some_variable: some_value
  another_variable: another_value

```

A more complete example can be found [here](https://github.com/nembery/panos_ansible_iron_skillet).

## Python Library Requirements:
* skilletlib
* pandevice
* pan-python


## Installation

This collection is currently installable as 'pan_community.skillet'

```bash

apt install python3-venv
python3 -m venv .venv
. ./.venv/bin/activate
pip install ansible

ansible-galaxy collection install pan_community.skillet

```

## Running

Edit the variables file to customize IronSkillet for your environment, then run the following command:

```bash

ansible-playbook -i inventory.yml -e 'username=admin' -e 'password=Super! Secret!' -e 'ip_address=10.0.1.55' load_iron_skillet.yml 

```

* Note - Any variables passed in via a `-e` switch will override values in the vars/main.yml file.