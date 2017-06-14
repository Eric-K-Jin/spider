#! /usr/bin/python
#! coding=utf-8

import sys

def get_bank_data(bankId, rows, fields):
    switcher = {
        "zgzsyh": "list",
        "shpfyh": "rows",
        "zgjsyh": "ProdList",
        "zgmsyh": "list",
        "zgnyyh": "Table"
    }

    return data_from_bank(rows[switcher[bankId]], fields)

def data_from_bank(rows, fields):
    if len(fields) == 0:
        return rows
    result = []
    for values in rows:
        data = {}
        for k, v in values.items():
            if k in fields:
                data[k] = v
        result.append(data)

    return result