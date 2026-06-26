from flask import Flask, render_code, send_from_directory, jsonify, request
import os

app = Flask(__name__, static_folder='.', template_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('.', path)

# ভবিষ্যতে Gemini API কানেক্ট করার জন্য এন্ডপয়েন্ট তৈরি রাখা হলো
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")
    
    # আপাতত ডামি রেসপন্স, পরে এখানে Gemini API লজিক বসবে
    return jsonify({"response": f"MedBuddy AI আপনার মেসেজটি পেয়েছে: '{user_message}'"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
