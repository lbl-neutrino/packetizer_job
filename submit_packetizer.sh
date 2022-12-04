#!/usr/bin/env bash

infile=$1; shift

logdir=$SCRATCH/logs.packetizer
mkdir -p "$logdir"

sbatch -o "$logdir"/slurm-%j.out "$@" packetizer_job.sh "$infile"
