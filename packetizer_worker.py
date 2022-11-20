#!/usr/bin/env python3

import argparse
from pathlib import Path
from subprocess import call
import sys

from zeroworker import LockfileListReader, LockfileListWriter

BASEDIR = '/global/cfs/cdirs/dune/www/data/Module2'
SUBDIR = 'packetized'


def get_outpath(path: str):
    relpath = Path(path).relative_to(BASEDIR)
    return Path(BASEDIR).joinpath('packetized', relpath).as_posix()


def process(path: str):
    outpath = get_outpath(path)
    Path(outpath).parent.mkdir(parents=True, exist_ok=True)

    # HACK: convert_rawhdf5_to_hdf5.py doesn't have a #! line
    # so we have to pass its path to python
    script = Path(sys.prefix).joinpath('bin/convert_rawhdf5_to_hdf5.py') \
                             .as_posix()
    cmd = f'time python3 {script} -i {path} -o {outpath}'
    call(cmd, shell=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('infile')
    args = ap.parse_args()

    reader = LockfileListReader(args.infile)
    logger = LockfileListWriter(args.infile + '.done')

    with logger:
        for path in reader:
            process(path)
            logger.log(path)


if __name__ == '__main__':
    main()
