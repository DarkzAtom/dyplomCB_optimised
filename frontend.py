import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import openai
from pinecone import Pinecone





def embedding_openai(article):
    response = openai.embeddings.create(
        model='text-embedding-3-small',
        input=article,
    )

    embeddings = [data.embedding for data in response.data]

    return embeddings[0]

def similarity_search(text_input):
    vectorized_request = embedding_openai('Article about: ' + text_input)

    response = dense_index.query(
        namespace="sosomuzika",
        vector=vectorized_request,
        top_k=5,
        include_metadata=True,
        include_values=False
    )

    response = response.matches
    string = ''
    for article in response:
        string += 'Score: ' + str(round(article.score, 2)) + '\n'
        string += 'Date: ' + article.metadata['creationDate'] + '\n'
        string += 'Article Title: ' + article.metadata['articleTitle'] + '\n'
        string += 'Article Summary: ' + article.metadata['summary'] + '\n'
        string += '\n'
    return string






def run_search():
    """
    This function is called when the 'Search' button is pressed.
    It gets the text from the input, runs the search, and updates the output.
    """
    input_text = text_input.get("1.0", tk.END).strip()

    # Check if the input is empty and provide a user-friendly message
    if not input_text:
        messagebox.showwarning("Input Error", "Please enter some text to search.")
        return

    results = similarity_search(input_text)

    # Clear previous results and insert new ones
    text_output.configure(state='normal')  # Enable editing temporarily
    text_output.delete("1.0", tk.END)
    text_output.insert("1.0", results)
    text_output.configure(state='disabled')  # Disable to prevent user editing



# Initialize a Pinecone client with your API key
apikey_pinecone = "pcsk_39Mp2M_NkLfhLHSzXxW4iddF7iAx6H6EkYGVaRyzMDawYncd3nLQatp6G2bcoJhMVoBuqL"
openai_apikey = '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'
pc = Pinecone(api_key=apikey_pinecone)

# Create a dense index with integrated embedding
index_name = "dyplomcb-storedarticles"
dense_index = pc.Index(index_name)

openai.api_key = openai_apikey



# Create the main application window
root = tk.Tk()
root.title("Simple Similarity Search App")
root.geometry("600x500")

# Create and configure the main frame
main_frame = ttk.Frame(root, padding="15")
main_frame.pack(fill=tk.BOTH, expand=True)

# ---- Input Section ----

# Label for the input text area
input_label = ttk.Label(main_frame, text="Enter text for similarity search:")
input_label.pack(fill=tk.X, pady=(0, 5))

# Text widget for input
text_input = tk.Text(main_frame, height=8, width=60, wrap=tk.WORD, borderwidth=1, relief="solid")
text_input.pack(fill=tk.X, expand=True)

# ---- Button Section ----

# Frame for the button to keep it centered
button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=15)

# Button to trigger the search
search_button = ttk.Button(button_frame, text="Run Search", command=run_search)
search_button.pack()

# ---- Output Section ----

# Label for the output text area
output_label = ttk.Label(main_frame, text="Search Results:")
output_label.pack(fill=tk.X, pady=(5, 5))

# Text widget for output (results)
# The state is set to 'disabled' to prevent the user from typing into the results area.
# It will be temporarily enabled inside the run_search() function to update the text.
text_output = tk.Text(main_frame, height=12, width=60, wrap=tk.WORD, state='disabled', borderwidth=1, relief="solid")
text_output.pack(fill=tk.BOTH, expand=True)

# Start the Tkinter event loop
root.mainloop()