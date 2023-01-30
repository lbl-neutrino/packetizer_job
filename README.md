# Installing

Run `install.sh`, which will locally create the `pkt_venv` venv and install a
few dependencies.


# Grabbing a node


Perlmutter:

``` bash
salloc -q interactive -A dune -C cpu -t 240 --ntasks-per-node=256
```

Cori Haswell:

``` bash
salloc -q interactive -A dune -C haswell -t 240 --ntasks-per-node=64
```

Cori KNL:

``` bash
salloc -q interactive -A dune -C knl -t 240 --ntasks-per-node=272
```


# Environment setup

``` bash
source load.sh
```

Not necessary if you're just submitting batch jobs.


# Interactive launching on a compute node

From a compute node provided by `salloc`:

``` bash
./packetizer_job.sh /path/to/input.txt
```

where `input.txt` contains a list of binary files to convert. The output
directory is configured at the top of `packetizer_worker.py`.


# Interactive launching on a login node

This is convenient when there are only a few files to process and/or no urgent
time constraints.

``` bash
./packetizer_job_local.sh /path/to/input.txt
```

By default, up to 16 parallel processes will run. This can be increased by
exporting `NPROCS` to something larger, but be considerate.


# Submitting batch jobs

``` bash
./submit_packetizer.sh /path/to/input.txt [extra sbatch args...]
```

This calls `sbatch` to submit `packetizer_job.sh`. The latter has some
Perlmutter-specific `SBATCH` directives, so if running on Cori, you will want to
override them when calling `submit_packetizer.sh`.

You can increase the amount of parallelism by submitting a job array
(`--array`).


# Preparing batch inputs

See the various scripts whose names begin with `dump_input`.

# Continuous running

SSH into Cori or Perlmutter, start a `screen` session (noting which node you are
logged into), and start up the `watch_folder.py` script in the background:

``` bash
./watch_folder.py -i /directory/to/monitor -o /path/to/input.txt &
```

This will write the paths of all h5 files within `/directory/to/monitor` to
`input.txt`, and will update `input.txt` as new files arrive over rsync. Then
follow the instructions above for interactive launching on a login node.
