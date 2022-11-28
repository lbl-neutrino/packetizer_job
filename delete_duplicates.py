#!/usr/bin/env python3

import argparse
from collections import defaultdict
from pathlib import Path
import shutil


BASEDIR = '/global/cfs/cdirs/dune/www/data/Module2'
TRASHDIR = '_trash'


def hash_dir(dirpath):
    d = defaultdict(lambda: [])
    for p in Path(dirpath).rglob('*.h5'):
        d[p.name].append(p)
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dir1', help='the one we delete from')
    ap.add_argument('dir2')
    ap.add_argument('--really', action='store_true')
    args = ap.parse_args()

    d1 = hash_dir(args.dir1)
    d2 = hash_dir(args.dir2)

    for name in d1:
        if name in d2:
            # print(' '.join(map(str, d1[name])))

            for p1 in d1[name]:
                for p2 in d2[name]:
                    try:
                        assert p1.stat().st_size <= p2.stat().st_size
                    except:
                        print(f'WTF {p1} {p2}')
                        continue
                    # reldir = p1.relative_to(BASEDIR)
                    reldir = p1.parent
                    destdir = Path(BASEDIR).joinpath(TRASHDIR, reldir)
                    dest = destdir.joinpath(name)
                    if args.really:
                        destdir.mkdir(parents=True, exist_ok=True)
                        shutil.move(p1, dest)
                    else:
                        print(f'mkdir -p {destdir}')
                        print(f'mv {p1} {dest}')
                        print()


if __name__ == '__main__':
    main()
