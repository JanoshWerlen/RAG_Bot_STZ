from flask import Flask, render_template, request
from bots_code.bots import initialise_AI, get_response
from bots_code.chat import do_chat

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response_route():
    query = request.form.get('query')
    category = request.form.get('category')
    response = get_response(query, category)
    return render_template('index.html', response=response, category=category)


@app.route('/show_log')
def show_logs():
    with open('responses.txt', 'r', encoding='utf-8') as log_file:
        log_content = log_file.readlines()

    return render_template('log.html', log_content=log_content)



def get_log_content():
    with open('responses.txt', 'r', encoding='utf-8') as log_file:
        log_content = log_file.readlines()
    return log_content

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    log_content = get_log_content()
    
    if request.method == 'POST':
        query = request.form.get('query')
        response = do_chat(query)
        
        # Append the new response to the log file
        with open('responses.txt', 'a', encoding='utf-8') as log_file:
            log_file.write(response + '\n')

        return render_template('chat.html', response=response, log_content=log_content)
    else:
        return render_template('chat.html', response="", log_content=log_content)



if __name__ == '__main__':
    initialise_AI()
    app.run(debug=True)





