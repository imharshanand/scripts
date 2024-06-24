```
# ChromeDriver Installation Guide

This guide provides instructions for installing, updating, and uninstalling ChromeDriver on Ubuntu using Conda and Selenium.

## Prerequisites

- Ubuntu 22.04
- Conda installed
- Google Chrome installed

## Installation

### Step 1: Create and Activate Conda Environment

1. Open a terminal.
2. Create a Conda environment named `selenium`:

   conda create -n selenium python=3.8

3. Activate the Conda environment:

   conda activate selenium
   ```

### Step 2: Install Required Packages

Install Selenium, BeautifulSoup, and Pandas in the Conda environment:
```bash
conda install -c conda-forge selenium beautifulsoup4 pandas
```

### Step 3: Download and Setup ChromeDriver

1. Download ChromeDriver matching your installed version of Google Chrome. For Chrome version `126.0.6478.63`:
   ```bash
   https://googlechromelabs.github.io/chrome-for-testing/

   On my system: Google Chrome Version 126.0.6478.114 (Official Build)
   ChromeDriver: (64-bit) Stable 126.0.6478.63	(r1300313)

   wget https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.63/linux64/chromedriver-linux64.zip
   ```
2. Unzip the downloaded file:
   ```bash
   unzip chromedriver-linux64.zip
   ```
3. Move ChromeDriver to `/usr/local/bin/` and set the correct permissions:
   ```bash
   sudo mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
   sudo chmod +x /usr/local/bin/chromedriver
   ```

## Update ChromeDriver

To update ChromeDriver, follow these steps:

1. Remove the old version:
   ```bash
   sudo rm /usr/local/bin/chromedriver
   ```
2. Download the new version:
   ```bash
   wget https://storage.googleapis.com/chrome-for-testing-public/<new_version>/linux64/chromedriver-linux64.zip
   ```
3. Unzip the downloaded file:
   ```bash
   unzip chromedriver-linux64.zip
   ```
4. Move the new ChromeDriver to `/usr/local/bin/` and set the correct permissions:
   ```bash
   sudo mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
   sudo chmod +x /usr/local/bin/chromedriver
   ```

## Uninstall ChromeDriver

To uninstall ChromeDriver, simply remove the executable:

```bash
sudo rm /usr/local/bin/chromedriver
```

## Example Python Script

Here is an example Python script using Selenium to scrape data from a website:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup the webdriver
driver = webdriver.Chrome()

try:
    # Step 1: Open the Wikipedia homepage
    driver.get("https://www.wikipedia.org/")
    print("Opened Wikipedia homepage")

    # Step 2: Find the search input field and enter the search term
    search_input = driver.find_element(By.ID, "searchInput")
    search_input.send_keys("Selenium (software)")
    print("Entered search term")

    # Step 3: Press Enter to perform the search
    search_input.send_keys(Keys.RETURN)
    print("Performed search")

    # Step 4: Wait for the search results page to load and display the results
    wait = WebDriverWait(driver, 20)
    search_results_loaded = wait.until(EC.presence_of_element_located((By.ID, "mw-content-text")))
    print("Search results page loaded")

    # Get the first search result link
    first_result = driver.find_element(By.XPATH, "//div[@class='mw-search-result-heading']/a")
    print("Located the first search result")

    # Click on the first search result
    first_result.click()
    print("Clicked on the first search result")

    # Step 5: Wait for the article page to load
    wait.until(EC.presence_of_element_located((By.ID, "firstHeading")))
    print("Article page loaded")

    # Print the title of the resulting page
    print("Page title is:", driver.title)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()

```

```
harsh@harsh:/usr/local/bin$ ls  
chromedriver  
harsh@harsh:/usr/local/bin$ chromedriver --version  
ChromeDriver 126.0.6478.63 (df799988fdc9c52db48650316d53800b1e9aa69e-refs/branch-heads/6478_56@{#5})  
harsh@harsh:/usr/local/bin$ 
```


## License

This project is licensed under the MIT License.
