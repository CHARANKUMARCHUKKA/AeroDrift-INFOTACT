import click
import subprocess

@click.group()
def main():
    """AeroDrift Enterprise Cloud Security CLI"""
    pass

@main.command()
def serve():
    """Start the FastAPI backend server"""
    click.echo("Starting backend server...")
    subprocess.run(["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"])

@main.command()
def dashboard():
    """Launch the Streamlit Web UI"""
    click.echo("Starting frontend dashboard...")
    subprocess.run(["streamlit", "run", "dashboard.py"])

if __name__ == "__main__":
    main()
