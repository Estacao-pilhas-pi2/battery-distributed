import os
import requests

from dataclasses import asdict

from battery_distributed.model import Machine


LOG = "Central"
SERVER_API_TOKEN = os.environ.get("TELEMETRY_API_TOKEN", "")
SERVER_HOST = os.environ.get("TELEMETRY_SERVER_HOST", "http://localhost:8000")
SERVER_BASE_URL = f"{SERVER_HOST}/api/maquina"

client = requests.Session()
# TODO: add authentication


def send_machine_empty(maquina: Machine):
    # TODO: 
    ...
    # client.post(f"{SERVER_BASE_URL}/{maquina.id}/telemetry", json=asdict(maquina))


def send_payment(maquina: Machine):
    ...