#!/bin/bash
source /opt/precip-forecast/venv/bin/activate
python /opt/precip-forecast/salva_precipitacao.py 2>&1 >> /tmp/logs
