# Google SERP API Scraper and Keyword Data Processor

This repository contains two Python scripts for scraping Google SERP data and processing keyword-related data. The first script fetches organic search results based on a search query and location, while the second script processes those results to extract keyword data and store it in an Excel file.

## Scripts

1. **serp.py**: Makes an API call to the Google SERP API to fetch organic search results for a given search query and location. It saves the API response to a JSON file.
2. **keyword.py**: Loads the SERP API response from a JSON file, processes URLs from the results, and fetches additional keyword data for each URL. The processed data is saved in an Excel file.

## Setup

Before running the scripts, ensure you have the following:

- A valid API account with credentials (username and password).
- A Python environment with the required dependencies installed.

### Configuration

1. **For `serp.py`**:
   - Replace `"Your Username"` and `"Your Password"` with your API credentials.
   - Modify the `searchQuery` and `location` variables as needed.

2. **For `keyword.py`**:
   - Replace `"Your Username"` and `"Your Password"` with your API credentials.
   - Modify the `searchquery` variable to specify the search term.
   - Ensure that the JSON file exists in the same directory.

### Usage

1. **Run the first script** (`serp.py`):
   
    ```bash
    python serp.py
    ```

   This will call the Google SERP API with the search query and location, and save the response in a JSON file.

2. **Run the second script** (`keyword.py`):

    ```bash
    python keyword.py
    ```

   This script loads the URLs from the JSON file, processes them, and stores the extracted keyword data in an Excel file.

### Example Output

- **serp.py**: Generates a JSON file with search results.
- **keyword.py**: Creates an Excel file (`combined_output_with_searchquery.xlsx`) with the extracted keyword data.

### Notes

- Ensure your credentials are securely stored.
- The API responses are saved in individual JSON files for each domain.
- The `keyword.py` script assumes the `serp.py` output file exists in the same directory.
