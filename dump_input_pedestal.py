#!/usr/bin/env python3

# import argparse
from collections import defaultdict
from pathlib import Path
import sys

import h5py


BASEDIR = '/global/cfs/cdirs/dune/www/data/Module2'
PACKETDIRNAME = 'packetized'

def is_packetized(path):
    try:
        f = h5py.File(path)
        return ('packets' in f) and (len(f['packets']) > 0)
    except OSError:
        print(f'OSError... ', file=sys.stderr, end='')
        return False


def should_skip(path):
    packetdir = Path(BASEDIR).joinpath(PACKETDIRNAME)

    # path to the symlink if the file was recorded in packet format:
    outpath1 = packetdir.joinpath(path.relative_to(BASEDIR))
    # output from converting to packet at NERSC:
    outpath2 = packetdir.joinpath(path.parent, path.name[:-3]+'.packet.h5')

    return (path.is_relative_to(packetdir) or
            'pedestal' not in path.name.lower() or
            outpath1.exists() or
            outpath2.exists() or
            is_packetized(path))


def main():
    files = defaultdict(lambda: [])

    for p in Path(BASEDIR).rglob('*.h5'):
        print(f'CHECKING {p}... ', file=sys.stderr, end='')
        if should_skip(p):
            print('SKIPPING', file=sys.stderr)
            continue
        print('DUMPING', file=sys.stderr)
        # print(p)
        files[p.name].append(p)

    for fname, paths in files.items():
        if len(paths) == 1:
            print(paths[0])
        else:
            assert(len(paths) == 2)
            goodpaths = [p for p in paths
                         if 'TPC12' in p.as_posix()
                         or '/Nov16/' in p.as_posix()]
            # assert(len(goodpaths) == 1)
            if len(goodpaths) != 1:
                print(paths, file=sys.stderr)
                raise
            print(goodpaths[0])


if __name__ == '__main__':
    main()
