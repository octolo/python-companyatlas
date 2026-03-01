"""Company documents command."""

from __future__ import annotations

from clicommands.commands.args import parse_args_from_config
from clicommands.commands.base import Command
from clicommands.utils import print_header, print_separator
from providerkit.commands.provider import _PROVIDER_COMMAND_CONFIG

from companyatlas.helpers import get_company_documents

_ARG_CONFIG = {
    **_PROVIDER_COMMAND_CONFIG,
    'code': {'type': str, 'default': ''},
}


def _documents_command(args: list[str]) -> bool:
    parsed = parse_args_from_config(args, _ARG_CONFIG, prog='documents')
    kwargs = {}
    attr_value = parsed.get('attr', {})
    if isinstance(attr_value, dict):
        kwargs['attribute_search'] = attr_value.get('kwargs', {})
    output_format = parsed.get('format', 'terminal')
    raw = parsed.get('raw', False)
    code = parsed.pop('code')
    first = parsed.pop('first', False)
    pvs_documents = get_company_documents(code, first=first, **kwargs)
    for pv in pvs_documents:
        name = pv['provider'].name
        time = pv['response_time']
        print_separator()
        print_header(f"{name} - {time}s")
        print_separator()
        print(pv['provider'].response('get_company_documents', raw, output_format))
    return True


documents_command = Command(_documents_command, "Get company documents (use --code company_code)")

