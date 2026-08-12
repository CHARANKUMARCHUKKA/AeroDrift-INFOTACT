import logging

logger = logging.getLogger("AeroDrift.AutoRemediator")

class AutoRemediator:
    def __init__(self, alerts):
        self.alerts = alerts
        self.remediation_commands = []
