from flask import Flask
import os

app = Flask(__name__)  # configurando app con flask
app.secret_key = os.urandom(24)  # una secret_key para la seguridad de la app

from development import main_code