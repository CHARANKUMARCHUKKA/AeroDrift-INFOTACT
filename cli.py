import click
import subprocess
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()

API_URL = "http://localhost:8000/api/v1"

@click.group()
def main():
    """AeroDrift Enterprise Cloud Security CLI"""
    pass

@main.command()
def serve():
    """Start the FastAPI backend server"""
    console.print("[bold green]Starting AeroDrift backend server...[/bold green]")
    subprocess.run(["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"])

@main.command()
def dashboard():
    """Launch the Streamlit Web UI"""
    console.print("[bold blue]Starting AeroDrift frontend dashboard...[/bold blue]")
    subprocess.run(["streamlit", "run", "dashboard.py"])

@main.command()
@click.option('--username', default='admin', help='Admin username')
@click.option('--password', default='aerodrift2026', help='Admin password')
def scan(username, password):
    """Run a beautiful CLI audit scan in the terminal"""
    console.print(Panel.fit("[bold cyan]🛡️ AeroDrift Terminal Audit Engine[/bold cyan]"))
    
    with console.status("[bold yellow]Authenticating with API...[/bold yellow]"):
        res = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
        if res.status_code != 200:
            console.print("[bold red]❌ Authentication Failed! Is the API running? ([i]python -m uvicorn api:app[/i])[/bold red]")
            return
        token = res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
    
    console.print("[bold green]✅ Authentication Successful![/bold green]")
    
    with console.status("[bold yellow]Fetching Cloud Topology...[/bold yellow]"):
        res = requests.get(f"{API_URL}/topology", headers=headers)
        if res.status_code == 200:
            data = res.json()
            nodes = len(data.get("nodes", []))
            edges = len(data.get("edges", []))
            console.print(f"🗺️  [bold]Topology mapped:[/bold] {nodes} Nodes, {edges} Edges")
            
    with console.status("[bold yellow]Running infrastructure drift detection...[/bold yellow]"):
        res = requests.get(f"{API_URL}/drift", headers=headers)
        
    if res.status_code == 200:
        data = res.json()
        
        table = Table(title="🚨 Drift Detection Audit Report 🚨", show_header=True, header_style="bold magenta")
        table.add_column("Status", style="cyan", width=12)
        table.add_column("Security Finding / Remediation Action", style="white")
        
        if data["status"] == "secure":
            table.add_row("[bold green]SECURE[/bold green]", "No infrastructure drift detected. Cloud baseline is intact.")
        else:
            for alert in data.get("alerts", []):
                table.add_row("[bold red]VULNERABLE[/bold red]", alert)
                table.add_row("[bold yellow]AUTO-FIX[/bold yellow]", f"Generated remediation script to self-heal '{alert[:20]}...'")
                
        console.print(table)
        console.print(Panel("[bold green]Audit complete. Remediation actions logged to database.[/bold green]", border_style="green"))

if __name__ == "__main__":
    main()
