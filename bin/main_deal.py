#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Usage:
   main-deal  (--show_different | --show_common)  <file1> <file2>  [--export <file_path> <item_field1> <item_field2> ]
   main-deal (-h | --help)

Options:
   -h --help  Show this screen.
   --show_different    Show the two files differences
   --show_common    Show the two files commons
"""
import os
from docopt import docopt
from temp_methods.utils import deal_name
from temp_methods.open_file import check_type
from temp_methods.export_files import export_file




class Morning(object):
    def __init__(self, file, field=None):
        super(Morning, self).__init__()
        self.path = file
        self.field = field
        self.box = []
        
        if file:
            self.load(file, field)
    
    def load(self, file, field):
        if not os.path.exists(file):
            raise ValueError('The given file does not exist')
        items = check_type(file, field)
        # print(items)
        self.box.extend(items)
    
    def compare(self, requirements, ignore=False, show_com=False, export=False, file_path=None):
        r1 = self
        r2 = requirements
        # print(r2.field)
        if show_com:
            results = {"common_item": []}
            other_reqs = (
                [r for r in r1.box]
                if ignore else r1.box
            )
            if export:
                export_file(r2.box, other_reqs, file_path, results, file_info=show_com)
            else:
                for req in r2.box:
                    if req in other_reqs:
                        results["common_item"].append(req)
        else:
            # print(r2)
            r1_name = deal_name(r1.path)
            r2_name = deal_name(r2.path)
            
            results = {r1_name: [], r2_name: []}
            
            other_reqs = (
                [r for r in r1.box]
                if ignore else r1.box
            )
            if export:
                export_file(r2.box, other_reqs, file_path, results, file_info=show_com)
            else:
                for req in r2.box:
                    if req not in other_reqs:
                        results[r2_name].append(req)
                
                other_reqs = (
                    [r for r in r2.box]
                    if ignore else r2.box
                )
                
                for req in r1.box:
                    if req not in other_reqs:
                        results[r1_name].append(req)
        return results


def compare(r1, r2, show_diff=False, show_com=False, excludes1=None, excludes2=None, export=False, file_path=None):
    field = {r1: excludes1, r2: excludes2}
    # print(field)
    if list(field.keys()).count(None) == 1:
        raise ValueError('item must have two values or nothing')
    try:
        r1 = Morning(r1, field[r1])
        # print(r1.path)
        # print(r2)
        # print(field[r2])
        r2 = Morning(r2, field[r2])
        # print(r2.path)
    except ValueError as e:
        print(e)
        print('There was a problem loading the given files')
    
    results = r1.compare(r2, ignore=True, show_com=show_com, export=export, file_path=file_path)
    if show_diff:
        print(results)
    if show_com:
        print(results)


def main():
    args = docopt(__doc__, version='main_deal')
    print(args)
    kwargs = {
        'r1': args['<file1>'],
        'r2': args['<file2>'],
        'show_diff': args['--show_different'],
        'show_com': args['--show_common'],
        'excludes1': args['<item_field1>'],
        'excludes2': args['<item_field2>'],
        'export': args['--export'],
        'file_path': args['<file_path>']
    }
    print(kwargs)
    compare(**kwargs)
