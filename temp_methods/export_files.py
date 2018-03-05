#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


def diff_export_file(list1, list2, path, results, export_filename):
    file_result = open(path + '{}.json'.format(export_filename.split('.')[0]), 'a+')
    for req in list1:
        if req not in list2:
            file_result.write(json.dumps(req) + '\n')
    results[export_filename].append('have already create file')
    file_result.close()


# export result json file
def export_file(box1, box2, path, results, file_info=False):
    if file_info:
        # print(path.format('common.json'))
        file_result = open(path + '{}'.format('common.json'), 'a+')
        for req in box1:
            if req in box2:
                file_result.write(json.dumps(req) + '\n')
        results["common_item"].append('have already create file')
        file_result.close()
    else:
        name_list = list(results.keys())
        diff_export_file(box2, box1, path, results, name_list[0])
        diff_export_file(box1, box2, path, results, name_list[1])
