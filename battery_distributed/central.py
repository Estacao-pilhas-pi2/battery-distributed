import os
import requests

from dataclasses import asdict

from battery_distributed.model import Machine


LOG = "Central"
SERVER_API_TOKEN = os.environ.get("TELEMETRY_API_TOKEN", "")
SERVER_HOST = os.environ.get("TELEMETRY_SERVER_HOST", "https://battery-service.vercel.app")
SERVER_BASE_URL = f"{SERVER_HOST}/api"


def send_machine_empty(maquina: Machine, type):
    requests.post(f"{SERVER_BASE_URL}/maquina/esvaziar/", data={
        "id": maquina.id,
        "tipos": [type]
    })

def send_payment(maquina: Machine):
    print(maquina.id)
    response = requests.post(f"{SERVER_BASE_URL}/pagamento/", data={
        "quantidade_pilha_AA": maquina.aa_count,
        "quantidade_pilha_AAA": maquina.aaa_count,
        "quantidade_pilha_C": maquina.c_count,
        "quantidade_pilha_D": maquina.d_count,
        "quantidade_pilha_V9": maquina.v9_count,
        "maquina": maquina.id
    })

    print(response.json())
    payment_id = response.json()['id']
    return f'{{"id_pagamento": "{payment_id}"}}'
