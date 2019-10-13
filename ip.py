#!/usr/bin/env python3
import time

time.sleep(60)

from led import draw_ip
import subprocess

a = subprocess.check_output('./ip.sh')
b = a.decode('utf-8').strip()
draw_ip(b)
time.sleep(120)

from index import run_main
run_main()
