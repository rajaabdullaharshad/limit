from __future__ import unicode_literals
from frappe import _


def get_data():
    config = [
        {'label': _('Subscription Information'), 
        'items': [
                {
                    "type": "page",
                    "name": "usage-info",
                    "label": _("Usage Info")
                }
            ]
        }
    ]
    return config    