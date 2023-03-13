#!/usr/bin/env python3

import argparse
from pathlib import Path
import shutil
from subprocess import call
import sys
import time

INDIR = '/global/cfs/cdirs/dune/www/data/Module3/ramp_up'
OUTDIR =  '/global/cfs/cdirs/dune/www/data/Module3/packet/ramp_up'
TEMPDIR = 'pkt_temp'

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

class LivePacketizer:
    def __init__(indir, outdir, tempdir):
        self.indir = Path(indir)
        self.outdir = Path(outdir)
        self.tempdir = Path(tempdir)
        self.processed = set()

        self.tempdir.mkdir(parents=True, exist_ok=True)

    def run():
        while True:
            for p in self.indir.rglob('*.h5'):
                if p in self.processed:
                    continue
                if time.time() - p.stat().st_mtime < 60:
                    continue
                name = p.name
                if '-binary-' in name:
                    name = name.replace('-binary-', '-packet-')
                outpath = self.outdir.joinpath(name)
                temppath = self.tempdir.joinpath(name)
                if outpath.exists():
                    self.processed.add(p)
                    continue
                temppath.unlink(missing_ok=True) # don't want to append!
                cmd = f'convert_rawhdf5_to_hdf5.py -i {p} -o {temppath} --workers 2'
                call(cmd, shell=True)
                shutil.move(temppath, outpath)
                self.processed.add(p)
            time.sleep(10)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--indir', default=INDIR)
    ap.add_argument('--outdir', default=OUTDIR)
    ap.add_argument('--tempdir', default=TEMPDIR)
    args = ap.parse_args()

    lp = LivePacketizer(args.indir, args.outdir, args.tempdir)
    lp.run()

if __name__ == '__main__':
    main()
