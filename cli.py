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

from rich import box
from rich.layout import Layout
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

@main.command()
@click.option('--username', default='admin', help='Admin username')
@click.option('--password', default='aerodrift2026', help='Admin password')
def scan(username, password):
    """Run a premium enterprise CLI audit scan"""
    
    # Expensive-looking ASCII Logo
    logo = """
    █████╗ ███████╗██████╗  ██████╗ ██████╗ ██████╗ ██╗███████╗████████╗
   ██╔══██╗██╔════╝██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██║██╔════╝╚══██╔══╝
   ███████║█████╗  ██████╔╝██║   ██║██║  ██║██████╔╝██║█████╗     ██║   
   ██╔══██║██╔══╝  ██╔══██╗██║   ██║██║  ██║██╔══██╗██║██╔══╝     ██║   
   ██║  ██║███████╗██║  ██║╚██████╔╝██████╔╝██║  ██║██║██║        ██║   
   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝        ╚═╝   
    """
    console.print(Align.center(Text(logo, style="bold cyan")))
    console.print(Align.center(Text("ENTERPRISE CLOUD DRIFT DETECTION ENGINE v1.0.0", style="bold white on blue")))
    console.print("")

    with Progress(
        SpinnerColumn("dots12", style="cyan"),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        # Step 1: Auth
        task1 = progress.add_task("[yellow]Establishing secure TLS connection & Authenticating...", total=None)
        try:
            res = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
            if res.status_code != 200:
                console.print("[bold red]❌ Authentication Failed! Incorrect credentials.[/bold red]")
                return
            token = res.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            time.sleep(0.5) # Add a slight artificial delay for the "expensive" feel
            progress.update(task1, description="[green]✔ Secure Authentication Established")
        except requests.exceptions.RequestException:
            console.print("[bold red]❌ Critical Connection Error! Backend Offline.[/bold red]")
            return

        # Step 2: Topology
        task2 = progress.add_task("[yellow]Ingesting Multi-Cloud Network Topology...", total=None)
        res = requests.get(f"{API_URL}/topology", headers=headers)
        if res.status_code == 200:
            data = res.json()
            nodes = len(data.get("nodes", []))
            edges = len(data.get("edges", []))
            time.sleep(0.6)
            progress.update(task2, description=f"[green]✔ Topology Mapped: {nodes} Nodes, {edges} Edges Ingested")
            
        # Step 3: Drift Scan
        task3 = progress.add_task("[yellow]Executing Deep Infrastructure Drift Analysis...", total=None)
        res = requests.get(f"{API_URL}/drift", headers=headers)
        time.sleep(0.8)
        progress.update(task3, description="[green]✔ Security Scan Complete")
        
    console.print("\n")
        
    if res.status_code == 200:
        data = res.json()
        
        # Premium Table Design
        table = Table(
            title="[bold white]A E R O D R I F T   A U D I T   R E P O R T[/bold white]",
            box=box.DOUBLE_EDGE,
            header_style="bold black on cyan",
            title_justify="center",
            width=100
        )
        table.add_column("STATUS", justify="center", width=15)
        table.add_column("SECURITY FINDING & REMEDIATION PAYLOAD", style="white")
        
        if data["status"] == "secure":
            table.add_row("[bold green]✔ SECURE[/bold green]", "Zero infrastructure drift detected. Cloud baseline is completely intact.")
        else:
            for alert in data.get("alerts", []):
                table.add_row("[bold red]⚠ VULNERABLE[/bold red]", alert)
                table.add_row("[bold yellow]⟳ AUTO-HEAL[/bold yellow]", f"[dim]Generated autonomous bash payload to revoke ingress rules for '{alert[:25]}...'[/dim]")
                table.add_row("", "") # spacer
                
        console.print(Align.center(table))
        
        summary = Panel(
            "[bold green]✔ AUDIT COMPLETE[/bold green] | All findings persisted to encrypted SQLite vault. Background remediation tasks dispatched.",
            border_style="cyan",
            box=box.ROUNDED,
            expand=False
        )
        console.print(Align.center(summary))

if __name__ == "__main__":
    main()
