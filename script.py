from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Serve the index.html page
@app.route('/')
def index():
    return render_template('index.html')

# Sample data endpoint
@app.route('/submitPrompt', methods=['POST'])
def get_data():
    data = {
        "message": "Hello from the backend!",
        "status": "success"
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
