"""Company events command."""

from __future__ import annotations

from clicommands.commands.args import parse_args_from_config
from clicommands.commands.base import Command
from clicommands.utils import print_header, print_separator
from providerkit.commands.provider import _PROVIDER_COMMAND_CONFIG

from companyatlas.helpers import get_company_events

_ARG_CONFIG = {
    **_PROVIDER_COMMAND_CONFIG,
    'code': {'type': str, 'default': ''},
}


def _events_command(args: list[str]) -> bool:
    parsed = parse_args_from_config(args, _ARG_CONFIG, prog='events')
    kwargs = {}
    attr_value = parsed.get('attr', {})
    if isinstance(attr_value, dict):
        kwargs['attribute_search'] = attr_value.get('kwargs', {})
    output_format = parsed.get('format', 'terminal')
    raw = parsed.get('raw', False)
    code = parsed.pop('code')
    first = parsed.pop('first', False)
    pvs_events = get_company_events(code, first=first, **kwargs)
    for pv in pvs_events:
        name = pv['provider'].name
        time = pv['response_time']
        print_separator()
        print_header(f"{name} - {time}s")
        print_separator()
        print(pv['provider'].response('get_company_events', raw, output_format))
    return True


events_command = Command(_events_command, "Get company events (use --code company_code)")

