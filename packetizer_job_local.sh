#!/usr/bin/env bash

infile=$1; shift

NPROCS=${NPROCS:-16}

source load.sh

module load parallel

sockdir=$(mktemp -d)
zw_fan.py --immortal --input-chunksize 8 --output-chunksize 1 "$sockdir" "$infile" &

# logdir=$SCRATCH/logs.packetizer/local.$(date -Iseconds)
# mkdir -p "$logdir"
seq "$NPROCS" | parallel -n0 ./packetizer_worker.py "$sockdir"

zw_shutdown.py "$sockdir"
