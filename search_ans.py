from flask import Flask, request, jsonify
from googlesearch import search

app = Flask(__name__)

# In-memory log for all searches
search_logs = []

# ========== Google Search API ==========
@app.route("/api/search/google", methods=["POST"])
def perform_google_search():
    try:
        data = request.get_json()
        query = data.get("query")

        if not query:
            return jsonify({"error": "Missing search query"}), 400

        results = [url for url in search(query, num_results=5)]

        # Log the search
        search_logs.append({
            "query": query,
            "results": results
        })

        return jsonify({
            "query": query,
            "results": results
        })

    except Exception as e:
        return jsonify({"error": f"Search failed: {str(e)}"}), 500

# ========== Search Logs ==========
@app.route("/api/search/logs", methods=["GET"])
def get_search_logs():
    return jsonify(search_logs)

# ========== Demo GET Route ==========
@app.route("/api/demodb", methods=["GET"])
def fetch_demo_data():
    return jsonify({"status": "Demo DB endpoint active."})

# ========== Demo POST Route ==========
@app.route("/api/demolog", methods=["POST"])
def post_demo_data():
    data = request.get_json()
    phone = data.get("phone")
    message = data.get("message")

    if not phone or not message:
        return jsonify({"error": "Phone and message are required"}), 400

    return jsonify({
        "received": {
            "phone": phone,
            "message": message
        }
    })

# ========== Run the App ==========
if __name__ == "__main__":
    app.run(debug=True)
