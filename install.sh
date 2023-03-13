#!/usr/bin/env bash

module load python              # 3.9-anaconda-2021.11

python -m venv pkt_venv
source pkt_venv/bin/activate

pip install --upgrade pip setuptools wheel

pip install git+https://github.com/mjkramer/zeroworker.git
pip install git+https://github.com/mjkramer/larpix-control.git@direct-convert
