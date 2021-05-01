import os

class Config:
    def __init__(self):
        self.host = os.getenv('POSTGRES_HOST', '192.168.56.101')
        self.port = os.getenv('POSTGRES_PORT', '30008')
        self.database = os.getenv('POSTGRES_DATABASE', 'qualis-db')
        self.user = os.getenv('POSTGRES_USER', 'postgres')
        self.password = os.getenv('POSTGRES_PASSWORD', 'postgres')