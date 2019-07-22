# Ansible Security Community Collection

## NOTE: THIS COLLECTION IS UNDER ACTIVE DEVELOPMENT AND SHOULD NOT BE CONSIDERED STABLE AT THIS TIME

This is the [Ansible
Collection](https://docs.ansible.com/ansible/devel/collections_tech_preview.html)
provided by the [Ansible Security Automation
Team](https://github.com/ansible-security) that aims to be the automation glue
between disjoint systems and security appliances that have little to no
integrations. Security Operators can utilize this Collection to be more
productive, adapt to the growing demand of the modern IT landscape, ensure
consistency in their IT environments, and respond to security incidents faster.

This Collection is meant for distribution via
[Ansible Galaxy](https://galaxy.ansible.com/) as is available for all
[Ansible](https://github.com/ansible/ansible) users to utilize, contribute to,
and provide feedback about.

### Using Ansible Security Community Collection

An example for using the Ansible Security Community Collection to manage a log source with [IBM QRadar](https://www.ibm.com/security/security-intelligence/qradar) is as follows.

`inventory.ini` (Note the password should be managed by a [Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html) for a production environment.
```
[qradar]
qradar.example.com

[qradar:vars]
ansible_network_os=ansible_security.community.qradar
ansible_user=admin
ansible_httpapi_pass=SuperSekretPassword
ansible_httpapi_use_ssl=yes
ansible_httpapi_validate_certs=yes
ansible_connection=httpapi
```

Below we use the [`block`](https://docs.ansible.com/ansible/latest/user_guide/playbooks_blocks.html) level keyword, we are able to use the `qradar_log_source_management` without the need for the Ansible Collection Namespace.

`qradar_with_collections_example.yml`
```
---
- name: Testing URI manipulation of QRadar
  hosts: qradar
  gather_facts: false
  tasks:
    - name: collection namespace block
      block:
        - name: create log source
          qradar_log_source_management:
            name: "Ansible Collections Example Log Source"
            type_name: "Linux OS"
            state: present
            description: "Ansible Collections Example Log Source Description"
      collections:
        - ansible_security.community
```

### Directory Structure

* `docs/`: local documentation for the collection
* `license.txt`: optional copy of license(s) for this collection
* `galaxy.yml`: source data for the MANIFEST.json that will be part of the collection package
* `playbooks/`: playbooks reside here
  * `tasks/`: this holds 'task list files' for `include_tasks`/`import_tasks` usage
* `plugins/`: all ansible plugins and modules go here, each in its own subdir
  * `modules/`: ansible modules
  * `lookups/`: lookup plugins
  * `filters/`: Jinja2 filter plugins
  * ... rest of plugins
* `README.md`: information file (this file)
* `roles/`: directory for ansible roles
* `tests/`: tests for the collection's content
