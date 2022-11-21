#!/usr/bin/env bash
#SBATCH -N 1 -n 256 -C cpu -L cfs
#SBATCH -t 02:00:00 -A dune -q regular

infile=$1; shift

module load python
source pkt_venv/bin/activate

sockdir=$(mktemp -d)
zw_fan.py -c "$SLURM_NTASKS" "$sockdir" "$infile" &

logdir=$PSCRATCH/logs.packetizer/$SLURM_JOBID
mkdir -p "$logdir"
srun --no-kill --kill-on-bad-exit=0 -o "$logdir"/output-%j.%t.txt -- ./packetizer_worker.py "$sockdir"

zw_shutdown.py "$sockdir"
