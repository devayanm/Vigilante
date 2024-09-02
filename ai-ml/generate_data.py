import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

num_rows = 1000

start_time = datetime.now()
timestamps = [start_time - timedelta(seconds=i * 10) for i in range(num_rows)]

data = {
    'timestamp': timestamps,
    'src_ip': [f'192.168.1.{random.randint(1, 255)}' for _ in range(num_rows)],
    'dest_ip': [f'10.0.0.{random.randint(1, 255)}' for _ in range(num_rows)],
    'protocol': [random.choice(['TCP', 'UDP']) for _ in range(num_rows)],
    'packet_size': [random.randint(40, 1500) for _ in range(num_rows)],
    'port_number': [random.randint(1, 65535) for _ in range(num_rows)],
}

df = pd.DataFrame(data)

df.to_csv('data/network_logs.csv', index=False)

print("Sample network_logs.csv generated successfully.")
