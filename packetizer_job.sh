#!/usr/bin/env bash
#SBATCH -N 1 --ntasks-per-node=256 -C cpu -L cfs
#SBATCH -t 04:00:00 -A dune -q regular

infile=$1; shift

source load.sh

sockdir=$(mktemp -d)
zw_fan.py --input-chunksize 8 --output-chunksize 1 "$sockdir" "$infile" &

logdir=$SCRATCH/logs.packetizer/$SLURM_JOBID
mkdir -p "$logdir"
srun --no-kill --kill-on-bad-exit=0 -o "$logdir"/output-%j.%t.txt -- ./packetizer_worker.py "$sockdir"

zw_shutdown.py "$sockdir"
