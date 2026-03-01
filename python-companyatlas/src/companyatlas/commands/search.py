"""Company search command."""

from __future__ import annotations

from clicommands.commands.args import parse_args_from_config
from clicommands.commands.base import Command
from clicommands.utils import print_header, print_separator
from providerkit.commands.provider import _PROVIDER_COMMAND_CONFIG

from companyatlas.helpers import search_company

_ARG_CONFIG = {
    **_PROVIDER_COMMAND_CONFIG,
    'query': {'type': str, 'default': ''},
    'readable': {'type': 'store_true'},
}


def _search_command(args: list[str]) -> bool:
    parsed = parse_args_from_config(args, _ARG_CONFIG, prog='search')
    kwargs = {}
    attr_value = parsed.get('attr', {})
    if isinstance(attr_value, dict):
        kwargs['attribute_search'] = attr_value.get('kwargs', {})
    output_format = parsed.get('format', 'terminal')
    raw = parsed.get('raw', False)
    query = parsed.pop('query')
    first = parsed.pop('first', False)
    readable = parsed.get('readable', False)
    pvs_companies = search_company(query, first=first, **kwargs)
    for pv in pvs_companies:
        name = pv['provider'].name
        time = pv['response_time']
        print_separator()
        print_header(f"{name} - {time}s")
        print_separator()
        print(pv['provider'].response('search_company', raw, output_format, readable=readable))
    return True


search_command = Command(_search_command, "Search companies (use --query query_string)")

