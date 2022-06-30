#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cmk.utils.render

from cmk.gui.i18n import _
from cmk.gui.plugins.metrics.utils import (
    graph_info,
    indexed_color,
    MAX_NUMBER_HOPS,
    metric_info,
    parse_color_into_hexrgb,
)


metric_info["prefixes_sent"] = {
    "title": _("Prefixes Sent"),
    "unit": "count",
    "color": "11/b",
}

metric_info["prefixes_received"] = {
    "title": _("Prefixes Received"),
    "unit": "count",
    "color": "12/b",
}

graph_info["bgp_prefixes"] = {
    "title": _("BGP Prefixes"),
    "metrics": [
        ("prefixes_sent", "area"),
        ("prefixes_received", "-area"),
    ]
}
