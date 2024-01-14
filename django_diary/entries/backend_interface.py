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
        ).choices[0].message.content
    
    def get_positive(self, text):
        response = self.generate("Please create a positive version of the following text:\n\n" + text)
        return response
    

    def find_pattern(self, texts):
        general_prompt = "Tell me how to change my time allocation of my activities so that I can make life better. Be concise and make a 3 bullet point list:\n\n"
        if len(texts) == 1:
            return self.generate(general_prompt + texts[0]) 
        # + "\n\n ---------------- \n\n I didn't find any other journal similar to this one."
        
        response = self.generate(general_prompt + "\n\n".join(texts))
        return response 
    # + "\n\n -- \n\n I viewed these journal entries: " + " ---------------------------".join(texts)

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
        self.openai = OpenAIInterface()

    def indexing(self, text, id):
        embeddings = self.openai.get_embedding(text)
        embed_dict = {"id": id, 'values': embeddings}
        self.index.upsert(vectors=[embed_dict], namespace="ns2")

    def query(self, text, date, top_k=3):
        embedding = self.openai.get_embedding(text)
        # find the strings that are most similar to the input string that have cosine similarity > 0.6
        final_query = self.index.query(namespace="ns2", vector=embedding, top_k=top_k, include_values=True)

        results = []
        for entry in final_query['matches']:
            # if the entry id is the same as the date, skip it
            print(entry['id'])
            if entry['id'] == date or abs(entry['score']) < 0.5:
                continue
            results.append(entry['id'])
        
        return results
    
    def delete_id(self, id):
        self.index.delete(ids=[id], namespace="ns")

    
# openai = OpenAIInterface()
# pinecone = PineconeInterface()

# text = "Today was a mixed day. It started on a positive note as I received a heartfelt compliment from my colleague for my hard work on a recent project. It felt great to be recognized for my efforts, and it boosted my confidence. However, the day took a turn for the worse when I got stuck in heavy traffic during my commute back home. What should have been a 30-minute drive turned into a frustrating ordeal that lasted over an hour. The gloomy weather outside didn't help either. Despite the traffic and the weather, I'm trying to focus on the positive moment earlier in the day."

# embedding_test = openai.get_embedding(text)
# to_upsert = zip("1", embedding_test, text)
# pinecone.indexing(list(to_upsert), "1")





# print(get_embedding("What is the best way to cook a steak?"))
