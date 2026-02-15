import csv
import random
from datetime import datetime, timedelta

# Read existing header
with open('Network_Availability_Report-2026-02-12.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)

# Generate data
rows = []
base_date = datetime(2026, 2, 11, 0, 0)

for hour in range(24):
    current_time = base_date + timedelta(hours=hour)
    time_str = current_time.strftime('%Y-%m-%d %H:%M')
    
    for response_code in range(33):  # 00-32
        code_str = f'{response_code:02d}'
        
        # Generate realistic counts with some variation
        # Base count around 287936 with +/- 20% variation
        base_count = 287936
        total_count = int(base_count * random.uniform(0.8, 1.2))
        
        # Bad count - mostly 0, occasionally small numbers
        if random.random() < 0.9:  # 90% chance of 0
            bad_count = 0
        else:
            bad_count = random.randint(1, 50)
        
        rows.append([time_str, code_str, total_count, bad_count])

# Write to file
with open('Network_Availability_Report-2026-02-12.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f'Generated {len(rows)} rows of data (33 response codes × 24 hours)')
