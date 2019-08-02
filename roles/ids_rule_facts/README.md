ids_rule_facts
===============

# This content is currently under development and should not be considered production ready

An [Ansible](https://www.ansible.com/) role to collect facts about rules and
signatures for many different Intrusion Detection Systems, these are defined as
"providers" to the Role, as
[facts](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variables-discovered-from-systems-facts).

Current supported list of providers:
* snort

Requirements
------------

Red Hat Enterprise Linux 7.x, or derived Linux distribution such as CentOS 7,
Scientific Linux 7, etc

Role Variables
--------------

* `ids_provider` - This defines what IDS provider (Default Value: "snort")

## snort

For the Snort provider you will need to set the `ids_provider` variable
as such:

    vars:
      ids_provider: snort

### snort variables

* `ids_provider` - Default value: `"snort"`
* `ids_rule_facts_path` - File or directory containing rules to collect facts
  on. Default value: `/etc/snort/rules/`
* `ids_rule_facts_filter` - Search string filter. Default value: `None`


Example Playbook
----------------

    ---
    - name: test ids_rule_facts
      hosts: idshosts
      vars:
        ids_provider: "snort"
        ids_rule_facts_filter: 'content:"|21 4A 6B B9 B2 3D 76 D5 D8 79 DB 08 48 65 41 1F 9E 25 13 4E CB C2 A4 F5 95 ED 54 66 B8 22 75 FE|'
      tasks:
        - name: import ids_rule_facts
          import_role:
            name: 'ids_rule_facts'

        - debug:
            var: ansible_facts.ids_rules

License
-------

GPLv3

Author Information
------------------

[Ansible Security Automation Team](https://github.com/ansible-security)
