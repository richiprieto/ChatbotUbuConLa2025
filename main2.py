#!/usr/bin/env python3
"""
RAG local con LangChain + FAISS + Ollama
"""

import os
import json
import requests
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re

# ------------------ CONFIGURACIÓN ------------------
TXT_PATH = "documentos/leyTransito.txt"
DB_PATH = "faiss_index_transito"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:latest"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"  
# ---------------------------------------------------

# --- Cliente Ollama ---
class OllamaLLM:
    def __init__(self, url, model):
        self.url = url
        self.model = model

    def generate(self, prompt: str) -> str:
        """Envía un prompt a Ollama y devuelve la respuesta completa"""
        response = requests.post(self.url, json={"model": self.model, "prompt": prompt}, stream=True)
        output = ""
        for line in response.iter_lines():
            if not line:
                continue
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                output += data["response"]
            if data.get("done"):
                break
        return output.strip()


# --- Funciones de procesamiento ---

def extract_text_from_txt(txt_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[Document]:
    """
    Lee un archivo de texto (.txt) y lo divide en fragmentos largos.
    """
    if not os.path.exists(txt_path):
        raise FileNotFoundError(f" No se encontró el archivo: {txt_path}")

    with open(txt_path, "r", encoding="utf-8") as f:
        text = f.read()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    chunks = splitter.split_text(text)
    docs = [Document(page_content=chunk, metadata={"source": txt_path}) for chunk in chunks]
    print(f"Texto dividido en {len(docs)} fragmentos de ~{chunk_size} caracteres cada uno.")
    return docs


def build_faiss_index(txt_path: str, db_path: str, embedding_model: str):
    """Crea un índice FAISS local desde un archivo de texto plano"""
    docs = extract_text_from_txt(txt_path)
    embeddings = SentenceTransformerEmbeddings(model_name=embedding_model)
    print("Creando índice FAISS local (texto plano)...")
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(db_path)
    print(f"Índice FAISS guardado en '{db_path}' ({len(docs)} fragmentos indexados)")
    return vectorstore


def load_faiss_index(db_path: str, embedding_model: str):
    """Carga un índice FAISS existente"""
    if not os.path.exists(db_path):
        raise FileNotFoundError(" No existe el índice FAISS. Ejecuta primero la indexación.")
    embeddings = SentenceTransformerEmbeddings(model_name=embedding_model)
    vectorstore = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
    print(f"Índice FAISS cargado desde '{db_path}'.")
    return vectorstore


def retrieve_context(query: str, vectorstore, top_k: int = 3) -> str:
    """
    Recupera fragmentos relevantes combinando búsqueda semántica y literal.
    Priorizamos coincidencias de artículos cuando el usuario consulta 'artículo N'.
    """
    # Detectar si hay referencia a un artículo específico
    articulo_match = re.search(r"(art[ií]culo)\s*(\d+)", query.lower())
    articulo_literal = None
    if articulo_match:
        articulo_literal = articulo_match.group(2)
        print(f"Detectada referencia literal al Artículo {articulo_literal}")

    #  Búsqueda semántica
    results = vectorstore.similarity_search_with_score(query, k=top_k * 2)

    #  Filtro por coincidencia literal si aplica
    context_parts = []
    scored_results = []
    for doc, score in results:
        text = doc.page_content
        if articulo_literal and re.search(rf"[Aa]rt[ií]culo\s*{articulo_literal}\b", text):
            # Boost: aumentar score para coincidencias literales
            score *= 0.5  # mejor rank (menor score = más relevante en FAISS)
        scored_results.append((doc, score))

    #  Reordenar según score ajustado
    scored_results.sort(key=lambda x: x[1])

    print("\n Fragmentos relevantes combinados:")
    print("-" * 80)
    for doc, score in scored_results[:top_k]:
        snippet = doc.page_content.replace("\n", " ")[:250]
        print(f"(score={score:.3f}) → {snippet}...")
        context_parts.append(doc.page_content)
    print("-" * 80)

    #  Unir textos relevantes
    context = "\n\n".join(context_parts)
    return context


def rag_query(query: str, vectorstore, llm: OllamaLLM):
    """Consulta el índice y genera la respuesta con Ollama"""
    context = retrieve_context(query, vectorstore)
    if not context.strip():
        print(" No se encontró contexto relevante.")
        return

    print("\n Enviando a Ollama con el siguiente contexto:")
    print("=" * 80)
    print(context)
    print("=" * 80 + "\n")

    prompt = f"""
        Eres un asistente experto en análisis legal.
        Responde exclusivamente usando el contexto proporcionado.
        Si el contexto no contiene la respuesta, responde claramente:
        "No hay información suficiente en el documento".

        CONTEXTO:
        {context}

        PREGUNTA:
        {query}

        Responde en español con precisión y claridad.
        """
    answer = llm.generate(prompt)
    print(" Respuesta de Ollama:\n")
    print(answer)
    print("\n" + "-" * 80)


# --- Ejecución principal ---
def main():
    print("=== RAG local con LangChain + FAISS + Ollama ===\n")

    if not os.path.exists(DB_PATH):
        vectorstore = build_faiss_index(TXT_PATH, DB_PATH, EMBEDDING_MODEL)
    else:
        vectorstore = load_faiss_index(DB_PATH, EMBEDDING_MODEL)

    ollama = OllamaLLM(OLLAMA_URL, MODEL)

    print("\nSistema RAG listo. Escribe tu pregunta (o 'exit' para salir):\n")
    while True:
        query = input("🔎 Pregunta: ").strip()
        if query.lower() in ["exit", "salir", "q"]:
            print(" Saliendo...")
            break
        if not query:
            continue
        rag_query(query, vectorstore, ollama)


if __name__ == "__main__":
    main()

