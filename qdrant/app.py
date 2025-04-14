from flask import Flask, request, jsonify
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

import os

app = Flask(__name__)

# Connect to Qdrant (inside Docker network)
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

COLLECTION_NAME = "my_collection"
VECTOR_SIZE = 4

# Create collection if it doesn't exist
if not qdrant.collection_exists(collection_name=COLLECTION_NAME):
    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
    )

@app.route("/insert", methods=["POST"])
def insert_point():
    data = request.json
    point_id = data.get("id")
    vector = data.get("vector")

    if not point_id or not vector:
        return jsonify({"error": "Missing 'id' or 'vector'"}), 400

    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[{"id": point_id, "vector": vector}]
    )
    return jsonify({"status": "inserted"})


@app.route("/search", methods=["POST"])
def search():
    data = request.json
    vector = data.get("vector")
    top_k = data.get("top_k", 3)

    if not vector:
        return jsonify({"error": "Missing 'vector'"}), 400

    hits = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=top_k
    )
    return jsonify([hit.dict() for hit in hits])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
