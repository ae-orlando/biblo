#!/usr/bin/env python3
"""Serve one HTML/CSS workspace, never the whole vault. Ctrl-C stops it."""
import argparse
import time
import practice
from browser_support import serve_directory

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('lab',choices=['web-html','web-css'])
parser.add_argument('--reference',action='store_true')
parser.add_argument('--port',type=int,default=8000)
args=parser.parse_args()
target=practice.ROOT/'07-solutions'/args.lab if args.reference else practice.ROOT/practice.LABS[args.lab]['path']/'work'
if not target.is_dir(): parser.error('workspace missing; run practice.py start first')
with serve_directory(target,args.port) as origin:
    print(f'Serving only {target.relative_to(practice.ROOT)} at {origin}; fake preview only.',flush=True)
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt: pass
