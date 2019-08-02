#!/usr/bin/python
# (c) 2018, Ansible Security Automation Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

#FIXME
DOCUMENTATION = '''
---
module: ids_rule_facts
short_description: Return snort rule information as fact data
description:
     - Return snort rule information as fact data as a backend implementation
       for the ids_rule_facts role that provides a consistent UX abstraction to
       various IDS providers.
version_added: "2.7"
requirements: []

notes:
  - When accessing the C(ansible_facts.ids_rule_facts) facts collected by this module,
    it is recommended to not use "dot notation" because rules can have a C(-)
    character in their name which would result in invalid "dot notation", such as
    C(ansible_facts.ids_rule_facts.zuul-gateway). It is instead recommended to
    using the string value of the service name as the key in order to obtain
    the fact data value like C(ansible_facts.services['zuul-gateway'])


author:
  - Adam Miller (@maxamillion)
'''

EXAMPLES = '''
- name: populate ids facts with all rules containing the string '192.168.1.1'
  snort_rule_facts:
    filter: "192.168.1.1

- debug:
    var: ansible_facts.services

'''

#FIXME
RETURN = '''
ansible_facts:
  description: Facts to add to ansible_facts about the rules found on the system
  returned: always
  type: complex
  contains:
    ids_rules:
      description: Rules found to match the provided filters
      returned: always
      type: list
'''


from ansible.module_utils.basic import AnsibleModule
import os
import glob

# FIXME - not sure if I want to actually process any rules just for fact collection
#HAS_IDSTOOLS = True
#try:
#    from idstools import rule
#    from idstools import maps
#except ImportError:
#    HAS_IDSTOOLS = False



def traverse_rules_file_dirs(somepath):
    dirs_in_somepath = [
        x for x in os.listdir(somepath)
            if os.path.isdir(os.path.join(somepath, x))
    ]

    for d in dirs_in_somepath:
        return glob.glob(os.path.join(somepath, "*.rules")) + traverse_rules_file_dirs(os.path.join(somepath,d))
    else:
        return glob.glob(os.path.join(somepath, "*.rules"))

def main():
    module = AnsibleModule(
        argument_spec=dict(
            filter=dict(required=False, default=None),
            rules_path=dict(required=False, default='/etc/snort/rules'),
        ),
        supports_check_mode=True
    )

    # FIXME - not sure if I want to actually process any rules just for fact collection
    #if not HAS_IDSTOOLS:
    #    module.fail_json(msg="Python module idstools not found on host, but is required for snort_rule_facts Ansible module")


    if os.path.isdir(module.params['rules_path']):
        rules_files = traverse_rules_file_dirs(module.params['rules_path'])
    else:
        rules_files = [module.params['rules_path']]

    ids_rules_matched = []

    for rule_file in rules_files:
        with open(rule_file, 'r') as rfd:
            if module.params['filter']:
                ids_rules_matched.extend(
                    [rule for rule in rfd.readlines()
                        if not rule.startswith('#') and module.params['filter'] in rule]
                )
            else:
                ids_rules_matched.extend(
                    [rule for rule in rfd.readlines() if not rule.startswith('#')]
                )

    results = dict(ansible_facts=dict(ids_rules=ids_rules_matched))
    module.exit_json(**results)


if __name__ == '__main__':
    main()
