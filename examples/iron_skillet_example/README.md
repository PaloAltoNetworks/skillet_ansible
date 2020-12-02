# panos_ansible_iron_skillet

A playbook to load IronSkillet on a freshly deployed PAN-OS VM-Series. For more information about IronSkillet, see
the [IronSkillet documentation](https://iron-skillet.readthedocs.io/en/docs_master/overview.html).  

You will need the paloaltonetworks.panos and paloaltonetworks.skillet collections installed

## Requirements

To run this skillet create a virtual environment, install pip, ansible and download the pan_community.skillet collection:
 
```bash

apt install python3-venv
python3 -m venv .venv
. ./venv/bin/activate
pip install ansible

ansible-galaxy collection install pan_community.skillet

```  
### Python Library Requirements
* skilletlib
* pandevice
* pan-python

## Example Tasks
Because each skillet will specify it's own set of required and optional variables, a handy short-cut is to just pass in all hostvars as the 'vars' parameters. This will allow you to construct a vars file elsewhere with the desired variable values. 
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

## Example vars file:
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

## Example of Validation:

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

## Running the playbook

Edit the variables file to customize IronSkillet for your environment, then run the following command:

```bash

ansible-playbook -i inventory.yml -e 'username=admin' -e 'password=Super! Secret!' -e 'ip_address=10.0.1.55' load_iron_skillet.yml 

```

* Note - Any variables passed in via a `-e` switch will override values in the vars/main.yml file.

### Other Useful Playbooks
 * [Skillet Ansible](https://github.com/PaloAltoNetworks/skillet_ansible) - Collection for working with skillets
 * [CDL Global Config](https://github.com/PaloAltoNetworks/panos-logging-skillets/tree/master/cdl_global_config_playbook) - Enables, configures, and validates Cortex Data Lake in a NGFW
 
 ### Useful Ansible Collections
* [PAN-OS Ansible Collection](https://github.com/PaloAltoNetworks/pan-os-ansible)
