#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cmk.gui.plugins.metrics import (
    perfometer_info
)

perfometer_info.append({
    'type': 'dual',
    'perfometers': [
        {
            'type': 'linear',
            'segments': ['prefixes_sent'],
            'total': 1_000_000,
#            'total': 'prefixes_sent:max',
        },
        {
            'type': 'linear',
            'segments': ['prefixes_received'],
            'total': 1_000_000,
#            'total': 'prefixes_received:max',
        },
    ],
})
