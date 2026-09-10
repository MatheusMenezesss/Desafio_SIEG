import requests
from Desafio_SIEG.config import SUBMIT_URL, TEAM_TOKEN

def submeter_gabarito(notas: list[dict]):
    """
        Envia as notas para o endpoint de submissão.
        formato : {"chave": "44 dig", "valor": float}
    """
    headers = {
        "Content-Type": "application/json",
    }
    
    payload = {
        "teamToken": TEAM_TOKEN,
        "itens": notas
    }

    print(f"\n[API] Enviando {len(notas)} notas para {SUBMIT_URL}...")
    response = requests.post(SUBMIT_URL, json=payload, headers=headers)
    try:
        print(f"[API] Retorno: {response.json()}")
    except Exception:
        print(f"[API] Texto: {response.text}")
    return response