# -------------------   Developers   --------------------

# Artiom Triboi        - artiom.triboi@stud.th-deg.de
# Bikalpa Khachhibhoya - bikalpa.khachhibhoya@stud.th-deg.de
# Seifalislam Sebak    - seifalislam.sebak@stud.th-deg.de



import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import os
from multiprocessing import Pool



class NewsScraper:
    def __init__(self):
        with open('team_Artiom_Bikalpa_Seifalislam_source_websites.json') as file:
            self.websites = json.load(file)
        with open('team_Artiom_Bikalpa_Seifalislam_scraping_results.json') as file:
            self.scrape_results = json.load(file)
            self.last_scrape = self.scrape_results[0]
            self.scrape_results = self.scrape_results[1]
        with open('team_Artiom_Bikalpa_Seifalislam_searching_results.json') as file:
            self.searching_results = json.load(file)
            self.last_search = self.searching_results[0]
            self.searching_results = self.searching_results[1]


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
                    match response.status_code:
                        case 403:
                            return (website['name'], [], f"{website['name']} - Failed to retrieve data: Access denied (403)")
                        case 408:
                            return (website['name'], [], f"{website['name']} - Failed to retrieve data: Timeout (408)")
                        case 429:
                            return (website['name'], [], f"{website['name']} - Failed to retrieve data: Too many requests (429)")
                        case 500:
                            return (website['name'], [], f"{website['name']} - Failed to retrieve data: Internal server error (500)")
                        case _:
                            return (website['name'], [], f"{website['name']} - Failed to retrieve data: Error code {response.status_code}")
            except requests.exceptions.ReadTimeout:
                return (website['name'], [], f"{website['name']} - Read timeout")
            except requests.exceptions.RequestException as e:
                return (website['name'], [], f"{website['name']} - Request error: {str(e)}")


    def scrape(self):
        Clear()
        self.last_scrape = time.strftime("%H:%M:%S %Y-%m-%d", time.localtime())
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

        self.json_save('team_Artiom_Bikalpa_Seifalislam_scraping_results.json', self.last_scrape, self.scrape_results)
        print("Updating finished!\n\nRemarks:")
        if outcome:
            for error in outcome:
                print(error)
        else:
            print("Successfully retrieved data from all websites!")
        input("\033[93m\nPress Enter to continue\033[0m\n")


    def print_scraping_results(self):
        Clear()
        print("Last update of news headers was made at:", self.last_scrape, "\n")
        for website, scrape_result in zip(self.websites, self.scrape_results):
            print("\033[93m          ", website['name'], ":\033[0m")
            if len(scrape_result) == 0:
                print("No headers were exctracted!")
            for result in scrape_result:
                print(result)
            print()
        input("\033[93m\nPress Enter to continue\033[0m\n")


    def print_searching_results(self):
        Clear()
        print("Search results for:")
        for result in self.searching_results:
            print(result[0])
        print("\nLast search was made at:", self.last_search, "\n")        
        print(f"{'Website':<30} | {'Keyword':<30} | Article")
        print("-" * os.get_terminal_size().columns)
        for result in self.searching_results:
            keyword = result[0]
            for counter in range(1, len(result)):
                website_name = self.websites[counter-1]['name']
                for article in result[counter]:
                    print(f"{website_name:<30} | {keyword:<30} | {article}")
            print("-" * os.get_terminal_size().columns)
        input("\033[93m\nPress Enter to continue\033[0m\n")


    def search(self):
        user_input = input("Enter the keywords or phrases to search for devided by a comma:\n")
        search_phrases_list = [element.strip() for element in user_input.split(",")]
        self.last_search = time.strftime("%H:%M:%S %Y-%m-%d", time.localtime())
        self.searching_results = []
        for phrase in search_phrases_list:
            phrase_result = []
            phrase_result.append(phrase)
            for counter in range(len(self.websites)):
                phrase_result.append([]) 
                for header in self.scrape_results[counter]:
                    if phrase.lower() in header.lower():
                        phrase_result[counter+1].append(header)
            self.searching_results.append(phrase_result)
            
        self.json_save('team_Artiom_Bikalpa_Seifalislam_searching_results.json', self.last_search, self.searching_results)
        self.print_searching_results()



def Clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')



if __name__ == "__main__":
    scraper = NewsScraper()
    alive = '1'

    while alive != '0':
        Clear()
        
        print("Please enter the number of the needed operation:")
        print("1 - Update news headers")
        print("2 - Search news headers")
        print("3 - Display all saved news headers")
        print("4 - Display previous search results")
        print("0 - Close the program")
        alive = input("\nNeeded operation - ")
        alive = alive.strip()

        match alive:
            case '1': scraper.scrape()
            case '2': scraper.search()
            case '3': scraper.print_scraping_results()
            case '4': scraper.print_searching_results()
            case '0': continue
            case _: print("\nThis operation isn't valid\n")
    
    Clear()
    print("\nProgram finished successfully!\n\nHave a nice day :)\n")

