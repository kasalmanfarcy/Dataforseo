import json
from client import RestClient

username = "sahiram@qubit.capital"
password = "c652b85bbbec56b9"
apiEndpoint = '/v3/serp/google/organic/live/regular'

# Manually provide the search query, location, and any other details
searchQuery = "legal compliance in financial documentation startups"
location = "United States"  # You can modify this as needed

def callApiAndStoreResponse(searchQuery, location):
    client = RestClient(username, password)

    # Prepare data to send to the API
    postData = [{
        'keyword': searchQuery,
        'location_name': location,  
        'language_code': 'en'  
    }]

    # Call the API and get the response
    response = client.post(apiEndpoint, postData)

    # Handle the response
    if response["status_code"] == 20000:
        # Save the response as a JSON file
        json_filename = f"{searchQuery.replace(' ', '_')}_response.json"
        with open(json_filename, 'w') as json_file:
            json.dump(response, json_file, indent=4)
        print(f"API response saved to '{json_filename}'")
    else:
        print(f"API Error for search query '{searchQuery}': {response.get('status_message', 'Unknown error')}")

# Call the function with your provided search query and location
callApiAndStoreResponse(searchQuery, location)
