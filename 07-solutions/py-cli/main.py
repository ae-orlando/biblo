import argparse
import csv
import json
from pathlib import Path
import sys
from reporting import load_rows, summarize, save


def main(argv=None):
    parser=argparse.ArgumentParser(description='Validate CSV expenses and create a category report.')
    parser.add_argument('source',type=Path)
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args(argv)
    try:
        if args.source.resolve()==args.output.resolve(): raise ValueError('input and output must differ')
        report=summarize(load_rows(args.source))
        if args.dry_run:
            print(json.dumps({'would_write':str(args.output),'report':report},ensure_ascii=False))
        else:
            save(args.output,report)
    except (OSError,UnicodeError,ValueError,csv.Error) as error:
        print(f'report failed: {error}',file=sys.stderr)
        return 1
    return 0


if __name__=='__main__':
    raise SystemExit(main())
