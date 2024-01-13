import os
from openai import OpenAI

class OpenAIInterface:
    def __init__(self):
        self.client = OpenAI(api_key='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')

    def generate(self, text, JSON=False):
        return self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"You are a helpful assistant{' designed to output JSON' if JSON else ''}."},
                {
                    "role": "user",
                    "content": text,
                }
            ],
            model="gpt-3.5-turbo-1106",
        )
    
    def get_positive(self, text):
        response = self.generate("Please create a positive version of the following text:\n\n" + text)
        return response.choices[0].message.content

    def get_embedding(self, text, model="text-embedding-ada-002"):
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input=[text], model=model).data[0].embedding


import pinecone

# initialize connection to pinecone (get API key at app.pinecone.io)

class PineconeInterface:
    def __init__(self):
        pinecone.init(
            api_key="91507b84-da37-4f1d-b193-ae945aabca2e",
            environment="gcp-starter"  # find next to API key in console
        )
        self.index = pinecone.Index('journals')

    def indexing(self, embeddings, ids):
        #self.index.upsert(vectors=embeddings, ids=ids)
        self.index.upsert(embeddings)

    def query(self, embeddings, top_k=10):
        return self.index.query(queries=embeddings, top_k=top_k)
    
# openai = OpenAIInterface()
# pinecone = PineconeInterface()

# text = "Today was a mixed day. It started on a positive note as I received a heartfelt compliment from my colleague for my hard work on a recent project. It felt great to be recognized for my efforts, and it boosted my confidence. However, the day took a turn for the worse when I got stuck in heavy traffic during my commute back home. What should have been a 30-minute drive turned into a frustrating ordeal that lasted over an hour. The gloomy weather outside didn't help either. Despite the traffic and the weather, I'm trying to focus on the positive moment earlier in the day."

# embedding_test = openai.get_embedding(text)
# to_upsert = zip("1", embedding_test, text)
# pinecone.indexing(list(to_upsert), "1")





# print(get_embedding("What is the best way to cook a steak?"))
