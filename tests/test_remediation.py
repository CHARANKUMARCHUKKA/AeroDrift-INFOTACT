import pytest
from remediation_engine import AutoRemediator
import os

def test_remediator_initialization():
    rem = AutoRemediator([], safe_mode=True)
    assert rem.safe_mode == True

def test_remediator_script_generation():
    alerts = ["CRITICAL: Subnet subnet-999 is public and exposed."]
    rem = AutoRemediator(alerts)
    script = rem.generate_script("test_remediate.sh")
    assert script == "test_remediate.sh"
    assert os.path.exists(script)
    with open(script, 'r') as f:
        content = f.read()
    assert "subnet-999" in content
    os.remove(script)
