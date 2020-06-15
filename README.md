# skillet-ansible

Collection for working with Skillets


See: [Skillet District](https://live.paloaltonetworks.com/t5/skillet-district/ct-p/Skillets) for more information.

## Example Tasks

The general usage is to first clone / update the desired skillet repository into a specific directory. Then call
`panos_skillet` passing in the directory in which to search for Skillets, and the name of the skillet you want to 
execute.

Because each skillet will specify it's own set of required and optional variables, a handy short-cut is to just pass
in all hostvars as the 'vars' parameters. This will allow you to construct a vars file elsewhere with the desired
variable values. 


```yaml

    - name: Download the latest templates
      git:
        repo: 'https://github.com/PaloAltoNetworks/iron-skillet.git'
        dest: '{{ playbook_dir }}/files'
        version: '{{ branch }}'

    - name: Include User Variables
      include_vars: vars/main.yml

    - name: Execute Skillet
      panos_skillet:
        skillet_path: '{{ playbook_dir }}/files'
        skillet: '{{ skillet }}'
        provider: '{{ provider }}'
        vars: '{{ hostvars["localhost"] }}'
      register: skillet_output

```

A more complete example can be found [here](https://github.com/nembery/panos_ansible_iron_skillet).

## Python Library Requirements:
* skilletlib
* pandevice
* pan-python