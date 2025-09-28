import openai
# Import the Pinecone library
from pinecone import Pinecone
from dotenv import load_dotenv
import os

# load env. vars
load_dotenv(dotenv_path='.env')


# Initialize a Pinecone client with your API key
apikey_pinecone = os.getenv('APIKEY_PINECONE')
openai_apikey = os.getenv('OPENAI_APIKEY')
pc = Pinecone(api_key=apikey_pinecone)

# Create a dense index with integrated embedding
index_name = os.getenv('PINECONE_INDEX_NAME')
dense_index = pc.Index(index_name)

openai.api_key = openai_apikey


def embedding_openai(article):
    response = openai.embeddings.create(
        model='text-embedding-3-small',
        input=article,
    )

    # Extract embeddings from response
    embeddings = [data.embedding for data in response.data]

    return embeddings[0]


request = input('o chem nuzna statya: ')
vectorized_request = embedding_openai('Article about: ' + request)

response = dense_index.query(
    namespace="sosomuzika",
    vector=vectorized_request,
    top_k=2,
    include_metadata=True,
    include_values=False
)

print(response.matches)