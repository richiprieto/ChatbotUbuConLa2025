---
marp: true
theme: gradient
paginate: true
header: | 
  '![width:50px](images/UbuntuCoF.png) | **UbuCon Latinoamérica 2025 - Cuenca**
footer: 'Eón Corp | Universidad del Azuay | Octubre 2025'
style: |
  section {
    font-family: "Inter", sans-serif;
  }
  header {
    text-align: left;
    font-size: 0.9em;
    color: #444;
    border-bottom: 2px solid #4a90e2;
    padding-bottom: 5px;
  }
  footer {
    text-align: right;
    font-size: 0.8em;
    color: #777;
    border-top: 1px solid #ccc;
    padding-top: 5px;
  }
---

# ¿El chatbot inventa cosas? Logra Respuestas Confiables con tus Datos y Software Libre

### Ricardo Prieto-Galarza
---

# Objetivo del Taller

Aprender a usar **modelos locales y herramientas libres** para:
- Integrar **chatbots con tus propios datos**
- Evitar *alucinaciones* o respuestas inventadas
- Comprender el flujo: **preprocesamiento → embeddings → búsqueda → respuesta**

---
## Clona el repositorio oficial

```bash
git clone https://github.com/richiprieto/ChatbotUbuConLa2025.git
cd ChatbotUbuConLa2025
uv sync
```
---

# ¿Qué es una LLM?

Una **LLM (Large Language Model)** es un modelo de inteligencia artificial entrenado con **billones de palabras** para aprender:

- Cómo se estructura el lenguaje 

Ejemplos:  
GPT, Mistral, Llama 3, DeepSeek, Gemma, etc.

---

## ¿Qué es Ollama?

> Ollama permite ejecutar **modelos de lenguaje (LLM)** directamente en tu computadora, sin depender de la nube, de forma **privada, libre y eficiente**.
## Instalación en Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama run deepseek-r1:latest
ollama run mistral:latest

```
---
# Que significa 20b
El número **20b** significa que el modelo tiene  
**20 mil millones de parámetros** (*B = billion = 10⁹*).

Cada parámetro es un número que el modelo ajusta durante su entrenamiento.  
Más parámetros = más conocimiento, pero también más recursos.

---

## Comparativa de tamaños comunes

| Modelo | Parámetros | Tamaño en disco | RAM mínima | GPU recomendada |
|--------|-------------|----------------|-------------|------------------|
| **Mistral 7B** | 7 mil millones | ~13 GB | 16 GB | 1 GPU 12–16 GB VRAM |
| **Llama 3 8B** | 8 mil millones | ~15 GB | 16–24 GB | 1 GPU 16 GB |
| **Llama 3 70B** | 70 mil millones | ~130 GB | 64–128 GB | 4 GPU 24 GB c/u |

> A mayor número de parámetros, mayor tamaño en disco, RAM y GPU.

---
# Como funcionan los LLM - Derribando mitos
> Las LLMs son como ese amigo al que decimos: "Tu que lo sabes todo y si no sabes **te lo inventas**"
![width:60%](images/meme1.jpg)

---
# Mito 1: "Piensan"

Una **LLM** no piensa:  
aprende patrones del lenguaje y **predice la próxima palabra**.

## Ejemplo simple

> Prompt: “El cielo es”

El modelo calcula probabilidades:
- azul → 90%  
- gris → 10% 

Escoge la palabra más probable y continúa prediciendo hasta completar la frase.

---
# Mito 2: "Son imparciales"
> Todo parte del dataset de entrenamiento, depende de su conjunto de datos

![width:20%](images/racismo.png)

---
# Mito 3: “Mientras más grande el modelo, mejor.”
> DeepSeek demostró lo que ya se sabia, un mejor conjunto de datos genera mejores resultados.

![width:20%](images/chatvsdeep.png)

---
# Mito 4: “Una LLM puede reemplazar a expertos.”
> Las IA es una herramienta, no es un experto.

![width:20%](images/noexperto.png)

---
# Mito 5: "La IA va a destruir el mundo"
> **LA IA ES UNA HERRAMIENTA**

![width:20%](images/kaboom.png)

---
# Mito 6: "Son deterministas"

> Frases como: "Le pregunté a chatgpt", "Usé este prompt", "El chat me dijo"
![width:20%](images/chatgpt.png)

---
# ¿Qué es RAG?

RAG (Retrieval-Augmented Generation) es una técnica que combina la búsqueda de información relevante en **tus propios datos** con la generación de texto por un llm, para producir respuestas **más precisas** y basadas informacion que poseemos.

---
# RAG
![width:20%](images/rag.png)

---
## Verifica si Ollama está ejecutándose

Cuando instalas Ollama, el servicio corre localmente  
en el puerto **11434** (por defecto).  
Este comando permite comprobarlo fácilmente

```bash
└─$ ss -tunapl | grep 11434
tcp   LISTEN 0      4096    127.0.0.1:11434      0.0.0.0:*  
```
---

# Componentes del sistema RAG

---

## Modelo LLM (Ollama)

Es la base que **interpreta y redacta** la respuesta.  
Todo funciona **sin conexión y con privacidad total**.
Se puede utilizar modelos comerciales haciendo minimos cambios en el script

---

## Fuente de datos propia

Son tus documentos, leyes, reportes o textos.  
Aportan información que no se conocia previamente. 
El chatbot deja de “inventar” y responde con **tus datos** (parcialmente).

---

## Embedding

Convierte el texto en **vectores** que capturan su sentido.  
Palabras con significados parecidos → vectores cercanos.  
Base de la búsqueda semántica en Faiss.

---

## Base de datos vectorial

Guarda textos convertidos en **vectores numéricos**.  
Permite buscar **por significado**, no por palabras exactas.  
Ejemplo: “multa” ≈ “sanción”.

---

# Ejemplo
![width:20%](images/vectorial.png)

---

# Tech Faiss

Faiss (Facebook AI Similarity Search) es una biblioteca desarrollada por **Meta AI**.  
Permite **almacenar y buscar vectores** de forma eficiente, incluso cuando se manejan millones de registros.

## Ventajas de Faiss

- Permite búsquedas semánticas rápidas sobre grandes volúmenes de texto.  
- Está optimizado para CPU y GPU.  
- Se integra fácilmente con Python, LangChain y herramientas de IA.  
- Es de código abierto y gratuito.  

---

# LangChain

LangChain es un framework de desarrollo en Python que permite **construir aplicaciones impulsadas por modelos de lenguaje (LLM)**.

Facilita conectar el modelo con:
- Bases de datos  
- APIs  
- Archivos locales  

---

# Ejecutemos main.py (Solo LLM)
El primer archivo main es un script de python que permite conectar un cli a nuestro LLM y hacerle preguntas

```bash
uv run main.py
```

---
# Probemos
```bash
Prompt: como se define las operadoras de transporte terrestre en ecuador? 
```
```bash
Respuesta: En Ecuador, las **operadoras de transporte terrestre** 
se definen principalmente en 
el marco legal del 
**Sistema Nacional de Transporte Terreste (SNAT)**, 
regido por la **Ley Reguladora del Transporte Terrestre de Pasajeros (LRTTE)**.
Una **operadora de transporte terrestre** es una **persona física 
o jurídica**, ya sea ecuatoriana o extranjera, que presta servicios 
de transporte por carretera a nivel nacional 
```
---
# Lo anterior FALSO

El ecuador se rige por **LEY ORGÁNICA DE TRANSPORTE TERRESTRE TRÁNSITO Y SEGURIDAD VIAL**
NOTA GENERAL:
En todas las normas legales y en la presente Ley cuando se mencione La Comisión Nacional de Transporte Terrestre, Tránsito y Seguridad Vial, se entenderá que se refiere a La Agencia Nacional de Regulación y Control del Transporte Terrestre, Tránsito y Seguridad Vial (ANRCTTTSV), que también podrá ser conocida como Agencia Nacional de Tránsito A.N.T.

---
# Ejecutemos main2.py (Incluye RAG)
El primer archivo main es un script de python que permite conectar un cli a nuestro LLM y hacerle preguntas

```bash
uv run main2.py
```
---
# Probemos
```bash
Prompt: como se define las operadoras de transporte terrestre en ecuador? 
```
```bash
Respuesta de Ollama:
Según el contexto proporcionado:
Art. 77.- Definición de operadoras de transporte 
terrestre: Constituye una operadora de transporte 
terrestre a toda persona jurídica 
(sea cooperativa o compañía) que, habiendo cumplido...
```
---
# Informacion real del documento
```bash
Art. 77.- Definición de operadoras de transporte 
terrestre.- Constituye una operadora de 
transporte terrestre, toda persona jurídica, 
sea cooperativa o compañía, que, habiendo...
```

---
# Configuraciones clave
> Chunk size se refiere al tamaño de la porcion de texto 1000 letras
Chunk overlap se refiere al solapamiento entre porciones.
Aunque chunks grandes parecen ser mejores hay que respetar la ventana contextual
```bash
def extract_text_from_txt(txt_path: str, 
                          chunk_size: int = 1000, 
                          chunk_overlap: int = 200)
```
---
# Configuraciones clave
> top_k: Elegir sabiamente el top de valores que vamos a tomar en cuenta para enviar al contexto

```bash
def retrieve_context(query: str, vectorstore, top_k: int = 3)
```

---
# Configuraciones clave

```bash
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
print(answer)
```