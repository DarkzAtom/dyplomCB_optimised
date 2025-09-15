import hashlib
import csv

import openai
from pinecone import Pinecone

# Initialize a Pinecone client with your API key
apikey_pinecone = "pcsk_39Mp2M_NkLfhLHSzXxW4iddF7iAx6H6EkYGVaRyzMDawYncd3nLQatp6G2bcoJhMVoBuqL"
openai_apikey = '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'
pc = Pinecone(api_key=apikey_pinecone)

# Create a dense index with integrated embedding
index_name = "dyplomcb-storedarticles"
dense_index = pc.Index(index_name)


csv_filename = 'output.csv'


client = openai.OpenAI(api_key=openai_apikey)
openai.api_key = openai_apikey



def summarize_article(combined_article):
    response = client.responses.create(
        model="gpt-4.1-nano",
        input=f"Describe what the article is about. Response without any explanations.\n{combined_article}"
    )
    return response.output_text


def embedding_openai(article):
    response = openai.embeddings.create(
        model='text-embedding-3-small',
        input=article,
    )

    # Extract embeddings from response
    embeddings = [data.embedding for data in response.data]

    return embeddings[0]





def csv_to_dict_array(filename):
    result = []
    with open(filename, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            result.append(dict(row))
    return result


def short_hash(text, length=8):
    """Create a short hash for use as ID"""
    full_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
    return full_hash[:length]


articles = csv_to_dict_array(csv_filename)

vectors = []

for i in range(len(articles)):
    print(f'i: {i}')
    id_ = short_hash(articles[i]['articleLink'])
    articles[i]['summary'] = summarize_article(articles[i]['articleTitle'] + '\n\n' + articles[i]['articleText'])
    print(articles[i]['summary'])
    vector = embedding_openai(articles[i]['summary'])
    metadata = articles[i]

    vectors.append({'id': id_, 'values': vector, 'metadata': metadata})


print(articles[0])

#target the index

dense_index.upsert(vectors=vectors, namespace='sosomuzika')













