#!/usr/bin/env python
# -*- coding: utf-8 -*-

# deal file path to only file name
def deal_name(path):
    return path.split('/')[-1] if '/' in path else path
    