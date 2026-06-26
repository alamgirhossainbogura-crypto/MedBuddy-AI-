import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'medbuddy-secret-key-12345'
    GEMINI_API_KEY = os.environ.get('.env') # পরে .env থেকে লোড হবে
    DEBUG = True
