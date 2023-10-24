import requests
import json

# Define your API key for the Google Search Console API.
api_key = "AIzaSyD7SQSRxZVl9Mk6LPMtnTnD35MF601cObA"

# Define a function to search Google and get the top 5 URLs for a given query.
def search_google(query):
    base_url = "https://www.googleapis.com/customsearch/v1"
    
    params = {
        "q": query,
        "key": api_key,
        "num": 5  # Get the top 5 results
    }
    
    response = requests.get(base_url, params=params)
    search_results = json.loads(response.text)
    
    # Extract and return the URLs.
    urls = [result["link"] for result in search_results.get("items", [])]
    return urls

def google_matching(visa_firm, compustat_firms, compustat_firm_urls, compustat_firm_gvkeys):
    matches = []
    for i, compustat_firm in enumerate(compustat_firms):
        compustat_firm_url = compustat_firm_urls[i]
        visa_search = search_google(visa_firm)
        compustat_firm_search = search_google(compustat_firm)

        # Compare URLs and check for matches based on your criteria.
        common_urls = list(set(visa_search).intersection(compustat_firm_search))

        if len(common_urls) >= 2 or compustat_firm_url in visa_search:
            return [compustat_firm_gvkeys[i], compustat_firm]
            # matches.append(visa_firm)
    return None