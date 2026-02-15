import csv
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def main():
    if len(sys.argv) != 2:
        print("Usage: python transform_report.py <date>")
        print("  date format: yyyy-mm-dd (e.g., 2026-02-12)")
        sys.exit(1)

    date_arg = sys.argv[1]
    input_file = f"Network_Availability_Report-{date_arg}.csv"
    output_file = f"myapp_metrics_load-{date_arg}.csv"

    eastern = ZoneInfo("America/New_York")
    utc = ZoneInfo("UTC")

    # Read and aggregate by hour
    hourly_data = {}
    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            hour_key = row["Date Hour (ET)"]
            total = int(row["Total Count"])
            bad = int(row["Bad Count"])

            if hour_key not in hourly_data:
                hourly_data[hour_key] = {"total": 0, "bad": 0}

            hourly_data[hour_key]["total"] += total
            hourly_data[hour_key]["bad"] += bad

    # Transform and write output
    indicator = "asvmyapp.key-indicator-1"

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["indicator", "since", "until", "good", "bad", "total"])

        for hour_key in sorted(hourly_data.keys()):
            data = hourly_data[hour_key]
            total = data["total"]
            bad = data["bad"]
            good = total - bad

            # Parse the ET datetime and localize to Eastern
            et_dt = datetime.strptime(hour_key, "%Y-%m-%d %H:%M")
            et_aware = et_dt.replace(tzinfo=eastern)

            # Convert to UTC for the "until" field
            until_utc = et_aware.astimezone(utc)
            since_utc = until_utc - timedelta(hours=1)

            until_str = until_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            since_str = since_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z")

            writer.writerow([indicator, since_str, until_str, good, bad, total])

    print(f"Transformed {len(hourly_data)} hourly rows -> {output_file}")

if __name__ == "__main__":
    main()
