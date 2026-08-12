import logging

logger = logging.getLogger("AeroDrift.AutoRemediator")

class AutoRemediator:
    def __init__(self, alerts, safe_mode=True):
        self.alerts = alerts\n        self.safe_mode = safe_mode
        self.remediation_commands = []\n        if self.safe_mode:\n            self.remediation_commands.append('# SAFE MODE ENABLED: Review commands before execution')

    def remediate_subnet(self, subnet_id):
        logger.info(f"Generating fix for {subnet_id}...")
        command = f"aws ec2 disassociate-route-table --subnet-id {subnet_id} --route-table-id rtb-public"
        self.remediation_commands.append(command)

    def remediate_security_group(self, sg_id, port):
        logger.info(f"Generating fix for {sg_id} on port {port}...")
        command = f"aws ec2 revoke-security-group-ingress --group-id {sg_id} --protocol tcp --port {port} --cidr 0.0.0.0/0"
        self.remediation_commands.append(command)
