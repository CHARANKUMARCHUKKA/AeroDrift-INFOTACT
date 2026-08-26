def fetch_gcp_vpc():
    return [
        {"id": "vpc-global-1", "cidr": "172.16.0.0/16"}
    ]

def fetch_gcp_firewall():
    return [
        {"id": "fw-allow-ssh", "direction": "INGRESS", "source_ranges": ["0.0.0.0/0"], "ports": ["22"]}
    ]
