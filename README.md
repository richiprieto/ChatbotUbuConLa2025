# ChatbotUbuConLa2025

## ¿El chatbot inventa cosas? Logra Respuestas Confiables con tus Datos y Software Libre
**Taller UbuConLA 2025 – Cuenca, Ecuador**

Este proyecto demuestra cómo crear un **chatbot confiable con tus propios datos** usando tecnologías libres:
- **Ollama** para ejecutar un modelo LLM local.
- **LangChain + FAISS** para búsqueda semántica y contextualización.
- **Python + uv** como entorno de ejecución portátil.

---

## 🚀 Objetivo

Disminuir las *alucinaciones* en los chatbots mediante un enfoque **RAG (Retrieval-Augmented Generation)**,  
donde el modelo responde con base en tu propia información (archivos locales o textos específicos).

---

## 🧩 Tecnologías utilizadas

| Tecnología | Descripción |
|-------------|-------------|
| **Ollama** | Ejecuta localmente modelos de lenguaje (LLM) como Mistral o DeepSeek |
| **LangChain** | Orquesta el flujo de búsqueda y generación |
| **FAISS** | Base de datos vectorial para búsqueda semántica eficiente |
| **Sentence-Transformers** | Genera embeddings multilingües para los textos |
| **uv** | Gestor de paquetes y entorno virtual rápido para Python |

---

## ⚙️ Requisitos previos

1. **Python 3.11+**
2. **UV**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. **Ollama** instalado y corriendo localmente:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama serve &
   ```
4. Iniciar **UV**, en la carpeta descargada
   ```bash
   uv init
   uv sync
   ```
5 Ejecutar
   ```bash
   uv run main.py
   uv run main2.py
   ``


