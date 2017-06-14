#! /usr/bin/python
#! coding=utf-8

import re
import demjson
import json
import sys

def jsonp_to_json(jsonp_str):
    tuple = replace('\({', jsonp_str)

    if tuple != None:
        start = tuple[1] - 1
        end = len(jsonp_str) - 1
        jsonp_str = jsonp_str[start:end]

    return demjson.decode(jsonp_str)

def replace(pattern, str):
    result = re.search(pattern, str)
    if result != None:
        return result.span()
    return result