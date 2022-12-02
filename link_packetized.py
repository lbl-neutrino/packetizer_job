#!/usr/bin/env python3

# Run me from within e.g. /global/cfs/cdirs/dune/www/data/Module2

import argparse
import os
from pathlib import Path
import shutil

import h5py


BASEDIR = '/global/cfs/cdirs/dune/www/data/Module2'
PACKETDIR = 'packetized'


def is_packetized(path):
    # try:
    f = h5py.File(path)
    return ('packets' in f) and (len(f['packets']) > 0)
    # except:
    #     return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('srcdir')
    ap.add_argument('--really', action='store_true')
    ap.add_argument('-g', '--glob', default='*.h5')
    args = ap.parse_args()

    for p in Path(args.srcdir).rglob(args.glob):
        if is_packetized(p):
            reldir = p.parent
            destdir = Path(BASEDIR).joinpath(PACKETDIR, reldir)
            dest = destdir.joinpath(p.name)
            if not dest.exists():
                relpath = os.path.relpath(p.absolute(), destdir)
                if args.really:
                    destdir.mkdir(parents=True, exist_ok=True)
                    # I can't figure out how to get a "../../blahblah"-like path
                    # with pathlib
                    #
                    os.symlink(relpath, destdir)
                else:
                    print(f'mkdir -p {destdir}')
                    print(f'ln -s {relpath} {dest}')
                    print()


if __name__ == '__main__':
    main()
