#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2018, Adam Miller (admiller@redhat.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: splunk_data_input_network
short_description: Manage Splunk Data Inputs of type TCP or UDP
description:
  - This module allows for addition or deletion of TCP and UDP Data Inputs in Splunk.
version_added: "2.8"
options:
  protocol:
    description:
      - Choose between tcp or udp
    required: true
    choices: ['tcp', 'udp']
  connection_host
    description:
      - Set the host for the remote server that is sending data.
      - dns Valid values: (ip | dns | none)
      - ip sets the host to the IP address of the remote server sending data.
      - dns sets the host to the reverse DNS entry for the IP address of the remote server sending data.
      - none leaves the host as specified in inputs.conf, which is typically the Splunk system hostname.
    default: "ip"
    required: false
  state:
    description:
      - Enable, disable, create, or destroy
    choices: [ "present", "absent", "enabled", "disable" ]
    required: false
    default: "present"
  datatype:
    description:
      - Forwarders can transmit three types of data: raw, unparsed, or parsed. "Cooked" data refers to parsed and unparsed formats.
    choices: [ "cooked", "raw" ]
    default: "raw"
    required: false
  host:
    description:
      - Host from which the indexer gets data.
    required: false
  index:
    description:
      - default Index to store generated events.
  name:
    description:
      - The input port which receives raw data.
    required: true
  queue:
    description:
      - Specifies where the input processor should deposit the events it reads. Defaults to parsingQueue.
      - Set queue to parsingQueue to apply props.conf and other parsing rules to your data. For more
        information about props.conf and rules for timestamping and linebreaking, refer to props.conf and
        the online documentation at "Monitor files and directories with inputs.conf"
      - Set queue to indexQueue to send your data directly into the index.
    choices: [ "parsingQueue", "indexQueue" ]
    required: false
  rawTcpDoneTimeout:
    description:
      - Specifies in seconds the timeout value for adding a Done-key.
      - If a connection over the port specified by name remains idle after receiving data for specified
        number of seconds, it adds a Done-key. This implies the last event is completely received.
    default: 10
    type: int
    required: false
  restrictToHost:
    description:
      - Allows for restricting this input to only accept data from the host specified here.
    required: false
  ssl:
    description:
      - Enable or disble ssl for the data stream
    required: false
    type: bool
  source:
    description:
      - Sets the source key/field for events from this input. Defaults to the input file path.
      - Sets the source key initial value. The key is used during parsing/indexing, in particular to set
        the source field during indexing. It is also the source field used at search time. As a convenience,
        the chosen string is prepended with 'source::'.
      - Note: Overriding the source key is generally not recommended. Typically, the input layer provides a
        more accurate string to aid in problem analysis and investigation, accurately recording the file from
        which the data was retrieved. Consider use of source types, tagging, and search wildcards before
        overriding this value.
  sourcetype:
    description:
      - Set the source type for events from this input.
      - "sourcetype=" is automatically prepended to <string>.
      - Defaults to audittrail (if signedaudit=true) or fschange (if signedaudit=false).

author: "Ansible Security Automation Team (https://github.com/ansible-security)
'''

EXAMPLES = '''
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_text

from ansible.module_utils.urls import Request
from ansible.module_utils.six.moves.urllib.parse import urlencode, quote_plus
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible.module_utils.splunk import SplunkRequest, parse_splunk_args

import copy

def main():

    argspec = dict(
        state=dict(required=False, choices=[ 'present', 'absent', 'enabled', 'disable' ], default='present', type='str'),
        connection_host=dict(required=False, choices=['ip', 'dns', 'none'], default='none', type='str'),
        host=dict(required=False, type='str', default=None),
        index=dict(required=False, type='str', default=None),
        name=dict(required=True, type='str'),
        protocol=dict(required=True, type='str', choices=['tcp', 'udp']),
        queue=dict(required=False, type='str', choices=['parsingQueue', 'indexQueue'], default='parsingQueue'),
        rawTcpDoneTimeout=dict(required=False, type='int', default=10),
        restrictToHost=dict(required=False, type='str', default=None),
        ssl=dict(required=False, type='bool', default=None),
        source=dict(required=False, type='str', default=None),
        sourcetype=dict(required=False, type='str', default=None),
        datatype=dict(required=False, choices=[ "cooked", "raw" ], default="raw")
    )

    module = AnsibleModule(
        argument_spec=argspec,
        supports_check_mode=True
    )

    splunk_request = SplunkRequest(
        module,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        not_rest_data_keys = [ 'state', 'datatype', 'protocol' ]
    )
    # This is where the splunk_* args are processed
    request_data = splunk_request.get_data()

    query_dict = splunk_request.get_by_path(
        'servicesNS/nobody/search/data/inputs/{0}/{1}/{2}'.format(
            quote_plus(module.params['protocol']),
            quote_plus(module.params['datatype']),
            quote_plus(module.params['name']),
        )
    )

    if module.params['state'] in ['present', 'enabled', 'disabled']:
        _data = splunk_request.get_data()
        if module.params['state'] in ['present', 'enabled']:
            _data['disabled'] = False
        else:
            _data['disabled'] = True
        if query_dict:
            needs_change = False
            for arg in request_data:
                if arg in query_dict['entry'][0]['content']:
                    if to_text(query_dict['entry'][0]['content'][arg]) != to_text(request_data[arg]):
                        needs_change = True
            if not needs_change:
                module.exit_json(changed=False, msg="Nothing to do.", splunk_data=query_dict)
            if module.check_mode and needs_change:
                module.exit_json(changed=True, msg="A change would have been made if not in check mode.", splunk_data=query_dict)
            if needs_change:
                splunk_data = splunk_request.create_update(
                    'servicesNS/nobody/search/data/inputs/{0}/{1}/{2}'.format(
                        quote_plus(module.params['protocol']),
                        quote_plus(module.params['datatype']),
                        quote_plus(module.params['name']),
                        data=urlencode(_data)
                    )
                )
            if module.params['state'] in ['present', 'enabled']:
                module.exit_json(changed=True, msg="{0} updated.", splunk_data=splunk_data)
            else:
                module.exit_json(changed=True, msg="{0} disabled.", splunk_data=splunk_data)
        else:
            # Create it
            splunk_data = splunk_request.create_update(
                'servicesNS/nobody/search/data/inputs/{0}/{1}'.format(
                    quote_plus(module.params['protocol']),
                    quote_plus(module.params['datatype']),
                ),
                data=urlencode(_data)
            )
            module.exit_json(changed=True, msg="{0} created.", splunk_data=splunk_data)
    elif module.params['state'] == 'absent':
        if query_dict:
            splunk_data = splunk_request.delete_by_path(
                'servicesNS/nobody/search/data/inputs/{0}/{1}/{2}'.format(
                    quote_plus(module.params['protocol']),
                    quote_plus(module.params['datatype']),
                    quote_plus(module.params['name']),
                )
            )
            module.exit_json(changed=True, msg="Deleted {0}.".format(module.params['name']), splunk_data=splunk_data)

    module.exit_json(changed=False, msg="Nothing to do.", splunk_data={})


if __name__ == '__main__':
    main()

