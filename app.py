import os
import json
from flask import Flask, render_template, request, jsonify
from google import genai  # Official Google GenAI SDK

# Initialize Flask app to look for template & static files in the root directory
app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')

# Initialize Gemini Client (Automatically looks for GEMINI_API_KEY environment variable)
try:
    client = genai.Client()
except Exception as e:
    client = None
    print(f"Gemini Client Initialization Failed: {e}")

@app.route('/')
def index():
    # রুট ফোল্ডার থেকে সরাসরি index.html রেন্ডার করবে
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_msg = data.get("message", "")
    
    if not user_msg:
        return jsonify({"error": "No message provided"}), 400

    # If Gemini API Key is available, fetch real AI response
    if client:
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_msg,
            )
            response_msg = response.text
        except Exception as e:
            print(f"Gemini API Error: {e}")
            response_msg = "দুঃখিত, এই মুহূর্তে এআই রেসপন্স তৈরি করা সম্ভব হচ্ছে না।"
    else:
        # Fallback if API Key is not set
        response_msg = f"MedBuddy AI (ডেমো মোড) আপনার মেসেজ পেয়েছে: '{user_msg}'।"
        
    return jsonify({"response": response_msg})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
