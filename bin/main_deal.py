#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Usage:
   main-deal (--fresh | --stale) <file1> <file2> [--exclude <package>...]
   main-deal (-h | --help)

Options:
   -h --help  Show this screen.
   --fresh    List newly added file
   --stale    List removed file
"""
import os
from docopt import docopt


class Morning(object):
    def __init__(self, file):
        super(Morning, self).__init__()
        self.path = file
        self.box = []
        
        if file:
            self.load(file)
    
    def load(self, file):
        if not os.path.exists(file):
            raise ValueError('The given file does not exitst')
        with open(file) as f:
            try:
                while True:
                    line = next(f)
                    if len(line) > 0:
                        self.box.append(line)
            except StopIteration:
                pass
    
    def compare(self, requirements, ignore=False, excludes=None):
        r1 = self
        r2 = requirements
        results = {'fresh': [], 'stale': []}
        
        other_reqs = (
            [r for r in r1.box]
            if ignore else r1.box
        )
        
        for req in r2.box:
            if req not in other_reqs:
                results['fresh'].append(req)
        
        other_reqs = (
            [r for r in r2.box]
            if ignore else r2.box
        )
        
        for req in r1.box:
            if req not in other_reqs:
                results['stale'].append(req)
        return results

def compare(r1, r2, include_fresh=False, include_stale=False, excludes=None):
    include_versions = True if include_stale else False
    excludes = excludes if len(excludes) else []
    try:
        r1 = Morning(r1)
        r2 = Morning(r2)
    except ValueError:
        print('There was a problem loading the given files')
    
    results = r1.compare(r2, ignore=True, excludes=excludes)
    print(results)

def main():
    args = docopt(__doc__, version='main_deal')
    
    kwargs = {
        'r1': args['<file1>'],
        'r2': args['<file2>'],
        'include_fresh': args['--fresh'],
        'include_stale': args['--stale'],
        'excludes': args['<package>']
    }
    compare(**kwargs)

if __name__ == "__main__":
    main()
