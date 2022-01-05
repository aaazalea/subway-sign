#!/usr/bin/env python3
import time

import subprocess
def get_ip():
    a = subprocess.check_output('./ip.sh')
    b = a.decode('utf-8').strip()
    return b

if __name__ == '__main__':
    from led import draw_ip,matrix
    print("Clock mode enabled")
    while True:
        matrix.Clear()
        b = time.strftime("%l.%M")
        draw_ip(b)
        time.sleep(10)
