#!/usr/bin/env python3

from collections import defaultdict
from pathlib import Path
import sys


def main():
    dups = defaultdict(lambda: [])
    dirgroups = set()

    for line in sys.stdin:
        p = Path(line.strip())
        dups[p.name].append(p)

    for name in dups:
        if len(dups[name]) > 1:
            print(name)
            for p in dups[name]:
                print(p)
            print()

            dirgroups.add(tuple(sorted(p.parent.as_posix()
                                       for p in dups[name])))

    print('\n### GROUPS')
    print(dirgroups)


if __name__ == '__main__':
    main()
