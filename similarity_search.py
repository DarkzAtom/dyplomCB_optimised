import openai

# Import the Pinecone library
from pinecone import Pinecone

# Initialize a Pinecone client with your API key
apikey_pinecone = "pcsk_39Mp2M_NkLfhLHSzXxW4iddF7iAx6H6EkYGVaRyzMDawYncd3nLQatp6G2bcoJhMVoBuqL"
openai_apikey = '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'
pc = Pinecone(api_key=apikey_pinecone)

# Create a dense index with integrated embedding
index_name = "dyplomcb-storedarticles"
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