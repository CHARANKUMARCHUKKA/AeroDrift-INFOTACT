import requests
import json
import os

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")
TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL", "")

def send_slack_alert(alerts: list):
    if not SLACK_WEBHOOK_URL:
        return
    payload = {
        "text": f"🚨 *AeroDrift Alert* 🚨\n{len(alerts)} vulnerabilities detected!",
        "attachments": [{"text": str(a)} for a in alerts]
    }
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
    except Exception:
        pass

def send_teams_alert(alerts: list):
    if not TEAMS_WEBHOOK_URL:
        return
    payload = {
        "@type": "MessageCard",
        "themeColor": "FF0000",
        "title": "AeroDrift Security Vulnerability Detected",
        "text": "\n".join([f"- {a}" for a in alerts])
    }
    try:
        requests.post(TEAMS_WEBHOOK_URL, json=payload, timeout=5)
    except Exception:
        pass

def broadcast_alert(alerts: list):
    send_slack_alert(alerts)
    send_teams_alert(alerts)
