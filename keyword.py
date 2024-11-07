import json
import re
from client import RestClient
import pandas as pd



apiUrl = "/v3/dataforseo_labs/google/ranked_keywords/live"
username = "Your username"
password = "Your Password"
client = RestClient(username, password)
jsonOutputPrefix = 'response_'

searchquery = "Your search query"
files = []
url = []
positions = []

def loadUrlsFromJsonFile(filePath):
    with open(filePath, 'r') as f:
        data = json.load(f)
    urls = []
    for task in data.get('tasks', []):
        for result in task.get('result', []):
            if result.get('type') == 'organic':
                for item in result.get('items', []):
                    rank_group = item.get('rank_group', 0)
                    if rank_group <= 5:
                        positions.append(rank_group)
                        url.append(item.get('url',''))
                        urls.append((item.get('url', ''), item.get('domain', '')))
    return urls

def cleanUrl(url):
    return re.sub(r"https?://(www\.)?", "", url)

def cleanDomain(domain):
    return re.sub(r"www\.", "", domain)

def cleanDomainForFilename(domain):
    return re.sub(r"(www\.|\.com)", "", domain)

def callApiWithUrlAndStoreResponse(cleanedUrl, cleanedDomain):
    postData = [{
        'target': cleanedDomain,
        'location_name': "United States",
        'language_name': "English",
        'filters': [
            ["ranked_serp_element.serp_item.relative_url", "=", f"/{cleanedUrl.split('/', 1)[1]}"]
        ]
    }]

    response = client.post(apiUrl, postData)

    if response["status_code"] == 20000:
        domainForFilename = cleanDomainForFilename(cleanedDomain)
        responseFile = f"{domainForFilename}.json"
        with open(responseFile, 'w') as f:
            json.dump(response, f, indent=4)
        print(f'Response saved to {responseFile}')
        files.append(responseFile)

    else:
        print(f"Error. Code: {response['status_code']} Message: {response['status_message']}")

def processUrls(urls):
    for url, domain in urls:
        cleanedUrl = cleanUrl(url)
        cleanedDomain = cleanDomain(domain)
        callApiWithUrlAndStoreResponse(cleanedUrl, cleanedDomain)

# Load URLs from the api_response.json file
filePath = 'file path'
urls = loadUrlsFromJsonFile(filePath)

if urls:
    processUrls(urls)
else:
    print("No URLs found in the JSON file.")

all_data = []

# Loop through each file, position, and URL
for i, file in enumerate(files):
    # Load JSON data from the file
    with open(file, 'r') as f:
        response = json.load(f)

    # Extract data from JSON
    for task in response.get('tasks', []):
        if 'result' in task and task['result'] is not None:
            for result in task['result']:
                if 'items' in result and result['items'] is not None:
                    for item in result['items']:
                        keywordData = item.get('keyword_data', {})
                        keyword = keywordData.get('keyword', None)
                        competitionLevel = keywordData.get('keyword_info', {}).get('competition_level', None)
                        searchVolume = keywordData.get('keyword_info', {}).get('search_volume', None)
                        coreKeyword = keywordData.get('keyword_properties', {}).get('core_keyword', None)
                        keywordDifficulty = keywordData.get('keyword_properties', {}).get('keyword_difficulty', None)
                        mainIntent = keywordData.get('search_intent_info', {}).get('main_intent', None)
                        foreignIntentList = keywordData.get('search_intent_info', {}).get('foreign_intent', [])
                        foreignIntent = ", ".join(foreignIntentList) if foreignIntentList else None
                        
                        # Append the extracted data to the list with additional columns
                        all_data.append({
                            'Search Query': searchquery,
                            'Position': positions[i],  # Use the position from the list
                            'URL': url[i],            # Use the URL from the list
                            'Keyword': keyword,
                            'Competition Level': competitionLevel,
                            'Search Volume': searchVolume,
                            'Core Keyword': coreKeyword,
                            'Keyword Difficulty': keywordDifficulty,
                            'Main Intent': mainIntent,
                            'Foreign Intent': foreignIntent,
                        })

# Create a DataFrame from the combined data
df = pd.DataFrame(all_data)

# Store DataFrame in Excel
excel_file_path = 'combined_output_with_searchquery.xlsx'
df.to_excel(excel_file_path, index=False)

print(f"Data from all files successfully written to {excel_file_path}")

