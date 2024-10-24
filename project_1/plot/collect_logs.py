import os
import time

dt = [
    0.1, 0.3, 0.5, 0.7, 1
]
MAX = 30000

if not os.path.exists("logs"):
    os.mkdir("logs")

for i in dt:
    os.system(f"python ../main.py --trail=10000 -r {int(MAX / i)} -m {MAX} -l logs/logs{i}.csv -s {i} --stop")
    time.sleep(5)