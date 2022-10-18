#!/usr/bin/env python3

from .agent_based_api.v1 import *

try:
    import orjson as json
except ImportError:
    import json


def __switch_states(num1, num2):
    s = State.OK
    if num1 == 0 and num2 == 0:
        s = State.CRIT
    elif num1 == 0 or num2 == 0:
        s = State.WARN
    return s

def __merge_dicts(x, y):
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z

def __peers(parsed):
    if 'ipv4Unicast' in parsed:
        if 'ipv6Unicast' in parsed:
            return __merge_dicts(
                parsed['ipv4Unicast']['peers'],
                parsed['ipv6Unicast']['peers']
            )

        return parsed['ipv4Unicast']['peers']

    if 'ipv6Unicast' in parsed:
        return parsed['ipv6Unicast']['peers']

    return []


def parse_frr_neighbors(string_table):
    return json.loads(''.join(x[0] for x in string_table))


def discover_frr_neighbor(section):
    for service in __peers(section):
        yield Service(item=service)


def discover_bgp_status(section):
    yield Service()


def check_frr_neighbor(item, section):
    peers = __peers(section)
    if item not in peers:
        yield Result(state=State.CRIT, summary="Session down - %s" % (item))
    else:
        descr = None

        if 'desc' in peers[item]:
            descr = peers[item]['desc']

        if descr is None:
            descr = item

        sent = 0
        received = 0
        if 'pfxSnt' in peers[item]:
            sent = int(peers[item]['pfxSnt'])

        if 'pfxRcd' in peers[item]:
            received = int(peers[item]['pfxRcd'])

        yield Metric("prefixes_sent", value = sent)
        yield Metric("prefixes_received", value = int(received))
        yield Result(
            state=__switch_states(sent, received),
            summary = "Peer %s - Sent: %d / Received: %d" % (descr, sent, received)
        )


def check_bgp_status(section):
    router_id = ''
    if 'ipv4Unicast' in section:
        count4 = int(section['ipv4Unicast']['peerCount'])
        router_id = section['ipv4Unicast']['routerId']
        yield Metric("ipv4_peers", value=count4)
    else:
        count4 = 0

    if 'ipv6Unicast' in section:
        count6 = int(section['ipv6Unicast']['peerCount'])
        router_id = section['ipv6Unicast']['routerId']
        yield Metric("ipv6_peers", value=count6)
    else:
        count6 = 0


    yield Result(
        state=__switch_states(count4, count6),
        summary = "RouterID %s; Sessions - IPv4: %d / IPv6: %d" % (router_id, count4, count6)
    )


register.agent_section(
    name="frr_bgp_summary",
    parse_function=parse_frr_neighbors,
)

register.check_plugin(
    name="frr_bgp_status",
    service_name="BGP Status",
    sections=['frr_bgp_summary'],
    discovery_function= discover_bgp_status,
    check_function = check_bgp_status
)

register.check_plugin(
    name="frr_bgp_neighbors",
    service_name="BGP Peer %s",
    discovery_function = discover_frr_neighbor,
    sections=['frr_bgp_summary'],
    check_function = check_frr_neighbor,
)
