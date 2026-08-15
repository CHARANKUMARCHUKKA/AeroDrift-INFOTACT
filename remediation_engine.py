import logging
from enterprise_logger import setup_enterprise_logger

logger = setup_enterprise_logger("AeroDrift.AutoRemediator")

class AutoRemediator:
    def __init__(self, alerts, safe_mode=True):
        self.alerts = alerts
        self.safe_mode = safe_mode
        self.remediation_commands = []
        if self.safe_mode:
            self.remediation_commands.append('# SAFE MODE ENABLED: Review commands before execution')

    def remediate_subnet(self, subnet_id):
        logger.info(f"Generating fix for {subnet_id}...")
        command = f"aws ec2 disassociate-route-table --subnet-id {subnet_id} --route-table-id rtb-public"
        self.remediation_commands.append(command)

    def remediate_security_group(self, sg_id, port):
        logger.info(f"Generating fix for {sg_id} on port {port}...")
        command = f"aws ec2 revoke-security-group-ingress --group-id {sg_id} --protocol tcp --port {port} --cidr 0.0.0.0/0"
        self.remediation_commands.append(command)

    def process_alerts(self):
        for alert in self.alerts:
            if "Subnet" in alert and "CRITICAL" in alert:
                # Extract subnet ID (e.g. "Subnet subnet-111 is public...")
                parts = alert.split()
                if "Subnet" in parts:
                    idx = parts.index("Subnet")
                    self.remediate_subnet(parts[idx+1])
            elif "Security Group" in alert and "HIGH" in alert:
                # Extract SG ID and port
                parts = alert.split()
                if "Group" in parts:
                    idx = parts.index("Group")
                    sg_id = parts[idx+1]
                    port = parts[-1].strip('.')
                    self.remediate_security_group(sg_id, port)
                    
    def generate_script(self, filename="remediate_drift.sh"):
        self.process_alerts()
        if not self.remediation_commands:
            return None
        with open(filename, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("\n".join(self.remediation_commands) + "\n")
        return filename
