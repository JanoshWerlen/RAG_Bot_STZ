from flask import Flask, render_template, request
from bots_code.bots import initialise_AI, get_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response_route():
    query = request.form.get('query')
    response = get_response(query)
    return render_template('index.html', response=response)





if __name__ == '__main__':
    initialise_AI()
    app.run(debug=True)


