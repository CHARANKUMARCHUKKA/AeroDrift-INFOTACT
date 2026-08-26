def fetch_azure_vnet():
    return [
        {"id": "vnet-eastus-1", "cidr": "10.1.0.0/16"},
        {"id": "vnet-westus-1", "cidr": "10.2.0.0/16"}
    ]

def fetch_azure_nsg():
    return [
        {"id": "nsg-public-web", "rules": [{"port": 80, "source": "0.0.0.0/0"}, {"port": 443, "source": "0.0.0.0/0"}]},
        {"id": "nsg-internal-db", "rules": [{"port": 1433, "source": "10.1.0.0/16"}]}
    ]
