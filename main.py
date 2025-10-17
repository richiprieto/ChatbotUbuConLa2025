#!/usr/bin/env python3
import requests
import json
import os

# Configuración de conexión
OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "deepseek-r1:latest"

# Colores para consola (opcional)
BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def query_ollama(prompt, model=DEFAULT_MODEL):
    """Envía el prompt a Ollama y muestra la respuesta en tiempo real."""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": model, "prompt": prompt},
            stream=True,
            timeout=60,
        )
        response.raise_for_status()
        print(f"\n{GREEN}Respuesta:{RESET}\n")

        full_text = ""
        for line in response.iter_lines():
            if not line:
                continue
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                print(data["response"], end="", flush=True)
                full_text += data["response"]
            if data.get("done"):
                print("\n")
                break
        return full_text
    except Exception as e:
        print(f"\n{RED} Error al conectar con Ollama: {e}{RESET}\n")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    clear_screen()
    print("=" * 60)
    print(f"{BLUE} Cliente CLI para Ollama ({DEFAULT_MODEL}){RESET}")
    print("=" * 60)
    print(f"Escribe {RED}exit{RESET} o {RED}salir{RESET} para cerrar.\n")

    while True:
        prompt = input(f"{BLUE} Prompt:{RESET} ").strip()
        if prompt.lower() in ["exit", "salir", "q"]:
            print(f"\n{GREEN} Saliendo...{RESET}")
            break
        if not prompt:
            continue
        query_ollama(prompt)

if __name__ == "__main__":
    main()

