import os

class Config:
    # Секретный ключ для использования в сессиях и защиты данных
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # Настройки для базы данных
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Настройки для flask-allauth и аутентификации
    AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN', 'your-yandex-oauth-domain')    
    CLIENT_ID = os.environ.get('CLIENT_ID', 'your-client-id')  
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET', 'your-client-secret')  
    LOGIN_URL = '/login'  
    LOGIN_REDIRECT_URL = '/'  
    
    # Уровень логирования
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'DEBUG')
