from googlesearch import search

def google_search(query: str, num_results: int = 5) -> list:
    try:
        results = []
        for url in search(query, num_results=num_results):
            results.append(url)
        return results
    except Exception as e:
        print("Error during search:", e)
        return []



from flask import Flask, request, jsonify
from googlesearch import search

app = Flask(__name__)

# Temporary in-memory database for storing user search logs
search_logs = []

# Route to perform Google search via form input
@app.route("/api/search/google", methods=["POST"])
def perform_google_search():
    try:
        query = request.form['query']
        results = []

        for url in search(query, num_results=5):
            results.append(url)

        # Log search activity
        search_logs.append({"query": query, "results": results})

        return jsonify({
            "query": query,
            "results": results
        })

    except Exception as e:
        return jsonify({"error": f"Search failed: {str(e)}"})

# Route to get all past search logs
@app.route("/api/search/logs", methods=["GET"])
def get_search_logs():
    return jsonify(search_logs)

# Example route for demonstration (acts like /studentdb)
@app.route("/api/demodb", methods=["GET"])
def fetch_demo_data():
    return jsonify({"status": "Demo DB endpoint active."})

# POST data logging (acts like /studentcreate)
@app.route("/api/demolog", methods=["POST"])
def post_demo_data():
    phone = request.form.get("phone")
    message = request.form.get("message")
    return f"Received demo data: {phone} - {message}"

if __name__ == "__main__":
    app.run(debug=True)
