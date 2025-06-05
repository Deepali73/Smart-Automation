from googlesearch import search

query = "your search query"
results = []
for url in search(query, num_results=5):  # Adjust num_results as needed
	results.append(url)

print(results)