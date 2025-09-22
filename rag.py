import chromadb
import os
import pandas as pd
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]

client = Mistral(api_key=api_key)

llmPrueba = "mistral-small-2503"

first_agent = client.beta.agents.create(
    model=llmPrueba,
    description="Fake news detector",
    name="FakeN"
)

class MistralEmbedder:
    def __init__(self,api_key):
        self.api_key = api_key
        self.client = Mistral(api_key=api_key)

    def name(self):
        return "embedder"
    def _embed_documents(self, texts):
        embeddings = self.client.embeddings.create(model="mistral-embed", inputs=texts)
        return [embeddings.data[i].embedding for i in range(len(texts))]
        
    def __call__(self, input):
        return self._embed_documents(input)

chroma_client = chromadb.HttpClient(host='vectordb',port=8000)

collection = chroma_client.get_or_create_collection(
    name="newsRepository",
    embedding_function=MistralEmbedder(api_key=os.environ["MISTRAL_API_KEY"])
    )

if collection.count() == 0:

    verdaderas = pd.read_csv("data/True.csv")
    falsas = pd.read_csv("data/Fake.csv")

    verdaderas["state"] = "True " * 10
    falsas["state"] = "Fake " * 10

    falsas = falsas["subject" != "Other"]
    union = pd.concat([verdaderas, falsas])

    documentos = union.apply(lambda row: ', '.join(row.astype(str)), axis=1).tolist()

    batch_size = 100
    iter = (len(documentos) // batch_size) if len(documentos) % batch_size == 0 else (len(documentos) // batch_size + 1)

    for b in range(iter):
        l = b*batch_size
        u = min(len(documentos), (b + 1)*batch_size)
        batch = documentos[l:u]
        batchids = ["id" + str(i) for i in range(l, u)]
        collection.add(
            documents=batch,
            ids=batchids
        )

plantilla_prompt = lambda input, contexto : f"""You are an assistant of a journalist 
working in fake news detection, who wants to keep track of the currently fakes catched. 
Given his question: {input}, you must answer according to 
the following information located in the database: {contexto}. If you received any information not related
"""

def generar_prompt(consulta):
    contexto = collection.query(
    query_texts=[consulta], 
    n_results=5)
    return plantilla_prompt(consulta, contexto['documents'])

print(len(documentos))

