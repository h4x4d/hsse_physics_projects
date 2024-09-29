import os
import time

dt = [
    0.1, 1, 2, 5, 10, 50, 100
]
MAX = 10000

if not os.path.exists("logs"):
    os.mkdir("logs")

for i in dt:
    os.system(f"python ../main.py --trail=10000 -r {int(MAX / i / 5)} -m {MAX} -l logs/logs{i}.csv -s {i} --stop")
    time.sleep(5)