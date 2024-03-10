import openai
from bots_code.bots import get_response

openai.api_key = "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"



def do_chat(query: str):
    response_file_path = "responses.txt"

    # Implement logic to check if the file exists and handle file read/write errors
    last_five = get_last_five_entries(response_file_path)
    last_five.append(query)  # Append the new query to the list
    history = "\n".join(last_five)  # Join everything into a single string

    context = get_response(query, "Alle")
    print(f"Query: {query} \n" )
    print(f"Context: {context} \n")
    print(f"History: {history} \n")

    try:
        chat = openai.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {
                    "role": "system",
                    "content": f"You are a HR assistant and base your answers this chat history: {history}, and if nessesary take this context into account: {context} "
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
        )
        response = chat.choices[0].message.content
        content = chat.choices[0].message.content
        print(f"Response: {response}")
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

    last_five_entries = entries[-10:]  # Each pair has two lines (Frage and Antwort)

    
    #print("\n".join(last_five_entries))
    return last_five_entries

