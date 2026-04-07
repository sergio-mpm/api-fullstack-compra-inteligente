from flask import Flask, jsonify, request, redirect
from flask_cors import CORS

from urllib.parse import unquote
from app.schemas import *
from app import create_app

app = create_app()


if __name__ == "__main__":
    app.run(debug=True)