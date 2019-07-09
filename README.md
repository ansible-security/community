# Ansible Security Collection

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
