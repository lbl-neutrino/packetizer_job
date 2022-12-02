#!/usr/bin/env python3

import argparse
from collections import defaultdict
from pathlib import Path
import sys

import h5py

from packetizer_worker import get_outpath, BASEDIR, SUBDIR


def is_packetized(path):
    try:
        f = h5py.File(path)
        return ('packets' in f) and (len(f['packets']) > 0)
    except OSError:
        print(f'OSError... ', file=sys.stderr, end='')
        return False


def should_skip(path):
    packetdir = Path(BASEDIR).joinpath(SUBDIR)
    return (path.is_relative_to(packetdir) or
            get_outpath(path).exists() or
            is_packetized(path))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('srcdir')
    ap.add_argument('-g', '--glob', default='self*-binary-*.h5')
    args = ap.parse_args()

    files = defaultdict(lambda: [])

    for p in Path(args.srcdir).rglob(args.glob):
        print(f'CHECKING {p}... ', file=sys.stderr, end='')
        if should_skip(p):
            print('SKIPPING', file=sys.stderr)
            continue
        print('DUMPING', file=sys.stderr)
        print(p)


if __name__ == '__main__':
    main()
