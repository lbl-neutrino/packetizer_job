#!/usr/bin/env python3

import argparse
from pathlib import Path
import shutil
from subprocess import call
import sys

# from zeroworker import LockfileListReader, LockfileListWriter
from zeroworker import ZmqListReader, ZmqListWriter

BASEDIR = '/global/cfs/cdirs/dune/www/data/Module3/run3'
OUTDIR = 'packet'
# GROUP = 'dune'

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)


def get_outpath_(path, subdir: str) -> Path:
    relpath = Path(path).relative_to(BASEDIR)
    if relpath.name.find('-binary-') != -1:
        out_relpath = relpath.parent.joinpath(relpath.name.replace('-binary-', '-packet-'))
    else:
        out_relpath = relpath.with_suffix('.packet.h5')
    return Path(BASEDIR).joinpath(subdir, out_relpath)


def get_outpath(path) -> Path:
    return get_outpath_(path, OUTDIR)


def get_tmppath(path) -> Path:
    return get_outpath_(path, OUTDIR+'.tmp')


def process(path):
    tmppath = get_tmppath(path)
    tmppath.parent.mkdir(parents=True, exist_ok=True)
    tmppath.unlink(missing_ok=True) # don't want to append!

    print(f'PROCESSING {path} TO {tmppath}')

    # HACK: convert_rawhdf5_to_hdf5.py doesn't have a #! line
    # so we have to pass its path to python
    # script = Path(sys.prefix).joinpath('bin/convert_rawhdf5_to_hdf5.py')
    # cmd = f'time python3 {script} -i {path} -o {tmppath}'
    cmd = f'time convert_rawhdf5_to_hdf5.py --direct -i {path} -o {tmppath}'
    retcode = call(cmd, shell=True)

    if retcode == 0:
        outpath = get_outpath(path)
        outpath.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(tmppath, outpath)

    return retcode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('sockdir')
    # ap.add_argument('--immortal', action='store_true')
    args = ap.parse_args()

    reader = ZmqListReader(args.sockdir)
    logger = ZmqListWriter(args.sockdir)

    with logger:
        for path in reader:
            retcode = process(path)
            logger.log(f'{path} {retcode}')

    # Commenting below because "immortality" is actually determined by the
    # arguments to zw_fan.py (see packetizer_job_continuous.sh)

    # with logger:
    #     while True:
    #         try:
    #             path = next(reader)
    #             retcode = process(path)
    #             logger.log(f'{path} {retcode}')
    #         except StopIteration:
    #             if args.immortal:
    #                 time.sleep(60)
    #             else:
    #                 break


if __name__ == '__main__':
    main()
