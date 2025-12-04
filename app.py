from flask import Flask, request, jsonify
from supabase import create_client
import os

app = Flask(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def index():
    return {"status": "ok", "message": "Flask + Supabase running on Render!"}

@app.route("/add", methods=["POST"])
def add_record():
    data = request.json
    result = supabase.table("items").insert(data).execute()
    return jsonify(result.data)

@app.route("/list", methods=["GET"])
def list_records():
    result = supabase.table("items").select("*").execute()
    return jsonify(result.data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
