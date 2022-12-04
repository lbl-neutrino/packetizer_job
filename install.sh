#!/usr/bin/env bash

module load python              # 3.9-anaconda-2021.11

python -m venv pkt_venv
source pkt_venv/bin/activate

pip install git+https://github.com/mjkramer/zeroworker.git#egg=zeroworker
pip install larpix-control
