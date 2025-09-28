import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import openai
from pinecone import Pinecone
from dotenv import load_dotenv
import os





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



# Create the main application window
root = tk.Tk()
root.title("Simple Similarity Search App")
root.geometry("600x500")

# listen to the "enter" button to be pressed to run the window
def handle_enter_key(event):
    SHIFT_MASK = 0x0001  # Hex value for the Shift modifier state

    if event.state & SHIFT_MASK:
        # Shift key is held down (Shift + Return)
        print("Shift + Return detected. Ignoring search execution.")
        # We also need to tell Tkinter not to process this event further
        return "break"
    else:
        # Unmodified Return key
        print("Unmodified Return detected. Executing search.")
        run_search()
        return "break"


root.bind('<Key-Return>', handle_enter_key)

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
search_button = ttk.Button(button_frame, text="Run Search", command=run_search, )
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