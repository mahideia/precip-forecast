#!/bin/bash
source /home/opc/precip-forecast/venv/bin/activate
python /home/opc/precip-forecast/salva_precipitacao.py 2>&1 >> /tmp/logs
