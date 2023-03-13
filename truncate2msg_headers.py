#!/usr/bin/env python3

# Use this to deal with binary files where the writer got killed before
# finishing to write the msg_headers

# Quoting Peter: "The msgs dataset is written before the msg_headers dataset, so
# this [length mismatch] is possible if the writer process was killed before it
# finished writing the data. It should be safe to truncate to the shorter length
# if this is the case"

import argparse
import shutil

import h5py

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input', required=True)
    ap.add_argument('-o', '--output', required=True)
    args = ap.parse_args()

    infile = h5py.File(args.input)
    nheaders = len(infile['msg_headers'])
    assert nheaders <= len(infile['msgs'])

    ## The following has trouble with groups:
    # with h5py.File(args.output, 'w') as outfile:
    #     nheaders = len(infile['msg_headers'])
    #     assert nheaders <= len(infile['msgs'])
    #     for k in infile.keys():
    #         print(k)
    #         if k == 'msgs':
    #             outfile[k] = infile[k][:nheaders]
    #         else:
    #             outfile[k] = infile[k]

    shutil.copy(args.input, args.output)

    with h5py.File(args.output, 'a') as outfile:
        del outfile['msgs']
        outfile['msgs'] = infile['msgs'][:nheaders]


if __name__ == '__main__':
    main()
