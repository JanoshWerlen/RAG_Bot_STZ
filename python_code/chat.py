import os
from dotenv import load_dotenv
import openai


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def do_chat(query: str):
    from python_code.bots import get_response
    response_file_path = "responses.txt"

    # Implement logic to check if the file exists and handle file read/write errors
    last_five = get_last_five_entries(response_file_path)
    last_five.append(query)  # Append the new query to the list
    history = "\n".join(last_five)  # Join everything into a single string

    context = get_response(query, "Alle")

    article_query = f"Auf welchem Artikel basiert folgende Anfrage?: + {context}. "
    article_based = get_response(article_query, "Alle")
    artikel_itself_query = f"Gib alle relevanten Artikel und die dazugehörigen Ursprünge im Format 'Artikel XYZ aus XYZ'an aus dem Text: {article_based}"

  
    artikel_itself = get_response(artikel_itself_query, "Alle")

    # reduced_history = reduce_history(history)

    print(f"\nArticle_Based: {article_based} \n")
    print(f"\nQuery: {query} \n")
    print(f"\nContext: {context} \n")

    print(f"\noriginal length {len(history)}\n")
    # print(f"\nreduced length {len(reduced_history)}\n")
    # print(f"\nreduced History {reduced_history}\n")

    initial_query = f"Du bist ein HR Assistent und gibst Anworten auf Deutsch, basierend auf den Informationen: {context}. Gib alle erwähnten Inhalte zurück. Verändere nicht die Bedeutung und interpretiere nie. "

    print(f"Initial Query: {initial_query} \n")
    try:
        chat = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"{initial_query}"
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
        )
        response = chat.choices[0].message.content
        content = chat.choices[0].message.content
        print(f"\nResponse: {response}\n")
    except Exception as e:
        print(f"\nAn error occurred: {e}\n")
        response = "Sorry, I couldn't process your request."

    print(f"\nInitial Quarry Length: {len(initial_query)}\n")
    print(f"\Response Length: {len(response)}\n")

    
    response = context
    artikel_itself = article_based

    return response, artikel_itself


def reduce_history(history):

    try:
        chat = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"Fasse folgendes zusammen: {history}, sorge dafür das alle Informationen und die Struktur bestehen bleibt"
                },
            ]
        )
        response = chat.choices[0].message.content

        print(
            f"\nQuerry for Summarization: Summarize {history} but keep all information, use bulletpoints to summarize so it is understandabl\n")
        print(f"\nSummarization:{response}\n")
    except Exception as e:
        print(f"An error occurred: {e}")
        response = "Sorry, I couldn't process your request."

    return response


def get_last_five_entries(response_file_path):
    with open(response_file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Find all entries for "Frage" and "Antwort"
    entries = []
    for line in lines:
        if line.startswith("Frage: ") or line.startswith("Antwort: "):
            entries.append(line.strip())

    # Ensure we have an even number of entries (pairs of Frage and Antwort)
    if len(entries) % 2 != 0:
        entries = entries[:-1]

    # Each pair has two lines (Frage and Antwort)
    last_five_entries = entries[-10:]

    # print("\n".join(last_five_entries))
    return last_five_entries
