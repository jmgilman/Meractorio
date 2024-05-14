BASE_NAME = "Raw Data"
TABLE_DATA = {
    "Sync": {
        "description": "Sync log",
        "fields": [
            {
                "name": "turn",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
            {
                "name": "timestamp",
                "type": "dateTime",
                "options": {
                    "timeZone": "client",
                    "dateFormat": {
                        "format": "l",
                        "name": "local",
                    },
                    "timeFormat": {
                        "format": "h:mma",
                        "name": "12hour",
                    },
                }
            },
            {
                "name": "records",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
        ]
    },
    "Regions": {
        "description": "Regions of the world",
        "fields": [
            {
                "name": "id",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
            {
                "name": "name",
                "type": "singleLineText",
            },
            {
                "name": "center_x",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
            {
                "name": "center_y",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
            {
                "name": "size",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
        ],
    },
    "Towns": {
        "description": "Towns of the world",
        "fields": [
            {
                "name": "id",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
            {
                "name": "name",
                "type": "singleLineText",
            },
            {
                "name": "location_x",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
            {
                "name": "location_y",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
            {
                "name": "region",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
            {
                "name": "capital",
                "type": "checkbox",
                "options": {
                    "color": "greenBright",
                    "icon": "check",
                },
            },
            {
                "name": "commoners",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
            {
                "name": "gentry",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
            {
                "name": "district",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
            {
                "name": "structures",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
            {
                "name": "total_taxes",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
        ],
    },
    "Town Market Data": {
        "description": "Market data for towns",
        "fields": [
            {
                "name": "id",
                "type": "singleLineText",
            },
            {
                "name": "town",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
            {
                "name": "item_name",
                "type": "singleLineText",
            },
            {
                "name": "price",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
            {
                "name": "last_price",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
            {
                "name": "average_price",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
            {
                "name": "moving_average",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
            {
                "name": "highest_bid",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
            {
                "name": "lowest_ask",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
            {
                "name": "volume",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
            {
                "name": "volume_prev_12",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
            {
                "name": "bid_volume_10",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
            {
                "name": "ask_volume_10",
                "type": "number",
                "options": {
                    "precision": 0,
                },
            },
        ],
    }
}
