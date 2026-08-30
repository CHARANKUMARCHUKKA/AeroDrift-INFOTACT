import csv
import io
import json

def generate_csv_report(logs):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Scan ID", "Timestamp", "Status", "Remediated", "Vulnerabilities Detected"])
    
    for log in logs:
        alerts = []
        try:
            alerts = json.loads(log.alerts_detected)
        except Exception:
            pass
        
        writer.writerow([
            log.id,
            log.timestamp,
            log.status,
            "Yes" if log.remediated else "No",
            len(alerts)
        ])
    
    return output.getvalue()
