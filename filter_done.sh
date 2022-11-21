#!/usr/bin/env bash

infile=$1; shift

# keep the full original list around, just in case
if [ ! -f $infile.orig ]; then
    cp $infile $infile.orig
fi

cp $infile $infile.prev
cut -d' ' -f2 $infile.done > $infile.omit
comm -23 <(sort $infile.prev) <(sort $infile.omit) | shuf > $infile
rm -f $infile.offset $infile.lock $infile.done.lock
