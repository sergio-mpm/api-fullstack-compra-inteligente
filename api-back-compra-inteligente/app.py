from flask import Flask, jsonify, request, redirect, send_from_directory
from flask_cors import CORS
import os
import joblib
import pandas as pd
import numpy as np

from urllib.parse import unquote
from app import create_app

app = create_app()

FRONTEND_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__),"..","api-web-compra-inteligente")
)

@app.route("/")
def index():
    return send_from_directory(FRONTEND_PATH, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_PATH, path)

if __name__ == "__main__":
    app.run(debug=True)