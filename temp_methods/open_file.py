#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv, json
from collections import namedtuple


# check file type and deal file depend on it is type
def check_type(filename, field):
    # print(field)
    temp_box = []
    if filename.endswith('.txt') or filename.endswith('.json') or filename.endswith('.jl'):
        with open(filename) as f:
            try:
                while True:
                    line = next(f).strip()
                    if len(line) != 0:
                        # print(line)
                        item = json.loads(line)[field] if field else line
                        # print(item)
                        temp_box.append(item)
            except:
                pass
    elif filename.endswith('.csv'):
        with open(filename) as f:
            f_csv = csv.reader(f)
            headings = next(f_csv)
            Row = namedtuple('Row', headings)
            for line in f_csv:
                item = Row(*line)
                # print(field)
                item = getattr(item, field, None) if field else item
                # print(item)
                # if not item:
                #     print('='*99)
                    # raise ValueError("this file have not this field")
                temp_box.append(item)
    else:
        raise ValueError('not support this file type')
    return temp_box
