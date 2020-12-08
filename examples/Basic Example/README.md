# Basic Example | Show System Info

A playbook to showcase a basic scenario of how you can use Ansible with a Palo Alto Networks Next-Gen Firewall.

You will need the paloaltonetworks.panos collection. 

## Requirements

To run this skillet create a virtual environment, install pip, ansible and download the pan_community.skillet collection:
 
```bash

apt install python3-venv
python3 -m venv .venv
. ./venv/bin/activate
pip install ansible

ansible-galaxy collection install pan_community.skillet

```  

*Note: If you are having certificate issues with Ansible, locate/create the file (.ansible.cfg) and add the following contents:
```bash

[galaxy]
ignore_certs=yes
```
### Python Library Requirements
* skilletlib
* pandevice
* pan-python

## Running the playbook

Edit the variables file to customize the playbook for your environment, then run the following command:

```bash

ansible-playbook -i inventory.yml -e 'username=admin' -e 'password=Super! Secret!' -e 'ip_address=10.0.1.55' show_system_info.yml 

```

* Note - Any variables passed in via a `-e` switch will override values in the vars/main.yml file.

### Other Useful Playbooks
 * [CDL Global Config](https://github.com/PaloAltoNetworks/panos-logging-skillets/tree/master/cdl_global_config_playbook) - Enables, configures, and validates Cortex Data Lake in a NGFW
 
 ### Useful Ansible Collections
* [PAN-OS Ansible Collection](https://github.com/PaloAltoNetworks/pan-os-ansible)
