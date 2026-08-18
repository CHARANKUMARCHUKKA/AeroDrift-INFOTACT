#!/bin/bash
# SAFE MODE ENABLED: Review commands before execution
aws ec2 disassociate-route-table --subnet-id subnet-111 --route-table-id rtb-public
aws ec2 revoke-security-group-ingress --group-id sg-web --protocol tcp --port 443 --cidr 0.0.0.0/0