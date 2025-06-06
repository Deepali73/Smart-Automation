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
