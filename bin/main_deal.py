#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Usage:
   main-deal  (--show_different | --show_common)  <file1> <file2> [--csv_item <csv1_item> <csv2_item>]
   main-deal (-h | --help)

Options:
   -h --help  Show this screen.
   --show_different    Show the two files differences
   --show_common    Show the two files commons
"""
import os, csv
from collections import namedtuple
from docopt import docopt
from temp_methods.utils import deal_name


# check file type and deal file depend on it is type
def check_type(filename, field):
    print(field)
    temp_box = []
    if filename.endswith('.txt') or filename.endswith('.json'):
        with open(filename) as f:
            try:
                while True:
                    line = next(f).strip()
                    if len(line) != 0:
                        temp_box.append(line)
            except StopIteration:
                pass
    elif filename.endswith('.csv'):
        with open(filename) as f:
            f_csv = csv.reader(f)
            headings = next(f_csv)
            Row = namedtuple('Row', headings)
            # field = field[0]
            for line in f_csv:
                item = Row(*line)
                item = getattr(item, field)
                # print(item)
                # field1 = "item.{}".format(field)
                temp_box.append(item)
    else:
        raise ValueError('not support this file type')
    return temp_box



class Morning(object):
    def __init__(self, file, field=None):
        super(Morning, self).__init__()
        self.path = file
        self.field = field
        self.box = []
        
        if file:
            self.load(file,field)
    
    def load(self, file, field):
        if not os.path.exists(file):
            raise ValueError('The given file does not exitst')
        # if len(set(field)) == 1:
        items = check_type(file, field)
        self.box.extend(items)
        
        # with open(file) as f:
        #     try:
        #         while True:
        #             line = next(f).strip()
        #             if len(line) != 0:
        #                 self.box.append(line)
        #     except StopIteration:
        #         pass
    
    def compare(self, requirements, ignore=False, show_com=False):
        r1 = self
        r2 = requirements
        
        if show_com:
            results = {"common_item": []}
            other_reqs = (
                [r for r in r1.box]
                if ignore else r1.box
            )
            
            for req in r2.box:
                if req in other_reqs:
                    results["common_item"].append(req)
        else:
            r1_name = deal_name(r1.path)
            r2_name = deal_name(r2.path)
            results = {r1_name: [], r2_name: []}
            other_reqs = (
                [r for r in r1.box]
                if ignore else r1.box
            )
            
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


def compare(r1, r2, show_diff=False, show_com=False, excludes1=None, excludes2=None):
    field = {r1:excludes1, r2:excludes2}
    if list(field.keys()).count(None) == 1:
        raise ValueError('--csv_item must have two values or nothing')
    try:
        r1 = Morning(r1, field[r1])
        # print(r1)
        r2 = Morning(r2, field[r2])
    except ValueError as e:
        print(e)
        print('There was a problem loading the given files')
    
    results = r1.compare(r2, ignore=True, show_com=show_com)
    if show_diff:
        print(results)
    if show_com:
        print(results)


def main():
    args = docopt(__doc__, version='main_deal')
    
    kwargs = {
        'r1': args['<file1>'],
        'r2': args['<file2>'],
        'show_diff': args['--show_different'],
        'show_com': args['--show_common'],
        'excludes1': args['<csv1_item>'],
        'excludes2': args['<csv2_item>']
    }
    print(kwargs)
    compare(**kwargs)

# if __name__ == "__main__":
#     main()
