# -------------------   Developers   --------------------

# Artiom Triboi        - artiom.triboi@stud.th-deg.de
# Bikalpa Khachhibhoya - bikalpa.khachhibhoya@stud.th-deg.de
# Seifalislam Sebak    - seifalislam.sebak@stud.th-deg.de

# -------------------   Remarks   --------------------

# To use the program, run it using the command: uvicorn team_Artiom_Bikalpa_Seifalislam_program:app --reload
# Then just open the team_Artiom_Bikalpa_Seifalislam_view.html in your browser



import requests
from bs4 import BeautifulSoup
import json
import time
import os
from multiprocessing import Pool
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware



class NewsScraper:
    def __init__(self):
        with open('team_Artiom_Bikalpa_Seifalislam_source_websites.json') as file:
            self.websites = json.load(file)
        with open('team_Artiom_Bikalpa_Seifalislam_scraping_results.json') as file:
            self.scrape_time, self.scrape_results = json.load(file)
        with open('team_Artiom_Bikalpa_Seifalislam_searching_results.json') as file:
            self.search_time, self.searching_results = json.load(file)


    def json_save(self, file_name, time, data):
        with open(file_name, 'w') as file:
            json.dump([time, data], file, indent=4)


    def scrape_single_website(self, website):
            try:
                response = requests.get(website['link'], timeout=2)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    raw_headers = soup.find_all(website['html_element'], class_=website['element_class'])
                    processed_headers = [header.text.strip() for header in raw_headers]
                    return (website['name'], processed_headers, None)
                else:
                    return (website['name'], [], f"{website['name']} - Failed to retrieve data: Error code {response.status_code}")
            except requests.exceptions.ReadTimeout:
                return (website['name'], [], f"{website['name']} - Read timeout")
            except requests.exceptions.RequestException as e:
                return (website['name'], [], f"{website['name']} - Error encountered: {str(e)}")


    def scrape(self):
        self.scrape_time = time.strftime("%H:%M:%S %Y-%m-%d", time.localtime())
        self.scrape_results = []
        outcome = []
        stack_size = 5

        for start in range(0, len(self.websites), stack_size):
            end = start + stack_size
            current_stack = self.websites[start:end]

            with Pool(processes=min(stack_size, len(current_stack))) as pool:
                results = pool.map(self.scrape_single_website, current_stack)

            for _, headers, error in results:
                self.scrape_results.append(headers)
                if error:
                    outcome.append(error)

        self.json_save('team_Artiom_Bikalpa_Seifalislam_scraping_results.json', self.scrape_time, self.scrape_results)
        if outcome:
            output = "Retrieving data finished!\n\nRemarks:\n"
            for error in outcome:
                output += error + "\n"
            return output
        else:
            return "Successfully retrieved data from all websites!"


    def search(self, keywords: list[str]):
        self.search_time = time.strftime("%H:%M:%S %Y-%m-%d", time.localtime())
        self.searching_results = []

        for phrase in keywords:
            phrase_result = [phrase]
            for headers_list in self.scrape_results:
                matches = []
                for header in headers_list:
                    if phrase.lower() in header.lower():
                        matches.append(header)
                phrase_result.append(matches)
            self.searching_results.append(phrase_result)
            
        self.json_save('team_Artiom_Bikalpa_Seifalislam_searching_results.json', self.search_time, self.searching_results)
        
        output = self.return_searching_results()
        return "Search finished successfully!\n\n" + output["results"]

    
    def return_scraping_results(self, encountered_errors):
        output = ""

        if encountered_errors:
            for error in encountered_errors:
                output += error + "\n"
        for website, scrape_result in zip(self.websites, self.scrape_results):
            output += "          " + website['name'] + ":\n"
            if len(scrape_result) == 0:
                output += "No headers were exctracted!\n"
            for element in scrape_result:
                output += element + "\n"
            output += "\n"

        return {"timestamp": self.scrape_time, "results": output}


    def return_searching_results(self):
        output = "Search results for the keywords:\n"
        for result in self.searching_results:
            output += result[0] + "\n"

        output += f"\n{'Website':<30} | {'Keyword':<30} | Article\n"
        output += "-" * 200 + "\n"

        for result in self.searching_results:
            keyword = result[0]
            for counter in range(1, len(result)):
                website_name = self.websites[counter - 1]['name']
                for article in result[counter]:
                    output += f"{website_name:<30} | {keyword:<30} | {article}\n"
            output += "-" * 200 + "\n"

        return {"timestamp": self.search_time, "results": output}



scraper = NewsScraper()
app = FastAPI(title="News Headers Extractor")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to the News Headers API"}

@app.post("/scrape")
def run_scraper():
    results = scraper.scrape()
    return {"status": "success", "timestamp": scraper.scrape_time, "results": results}

@app.post("/search")
def search_keywords(keywords: list[str] = Query(...)):
    results = scraper.search(keywords)
    return {"status": "success", "timestamp": scraper.search_time, "results": results}

@app.get("/scrape-results")
def get_scrape_results():
    return scraper.return_scraping_results("")

@app.get("/search-results")
def get_search_results():
    return scraper.return_searching_results()

