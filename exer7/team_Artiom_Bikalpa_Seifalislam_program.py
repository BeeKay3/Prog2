# -------------------   Developers   --------------------

# Artiom Triboi        - artiom.triboi@stud.th-deg.de
# Bikalpa Khachhibhoya - bikalpa.khachhibhoya@stud.th-deg.de
# Seifalislam Sebak    - seifalislam.sebak@stud.th-deg.de


import requests
from bs4 import BeautifulSoup
import json
import csv
import time

with open('team_Artiom_Bikalpa_Seifalislam_source_websites.json') as file:
        websites = json.load(file)

def Scraping():
    all_headers = []

    for website in websites:
        try:
            response = requests.get(website['link'], timeout=2)
        except requests.exceptions.ReadTimeout:
            print("Read timeout occurred for ", website['name'])
        except requests.exceptions.RequestException as e:
            print("An error occurred for ", website['name'], ": ", e)

        match response.status_code:
            case 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                raw_headers = soup.find_all(website['html_element'], class_=website['element_class'])

                current_headers = []
                for header in raw_headers:
                    current_headers.append(header.text.strip())

                all_headers.append(current_headers)

            case 403:
                all_headers.append([f"Access denied: failed to retrieve data from {website['name']}"])
            case 408:
                all_headers.append([f"Timeout: failed to retrieve data from {website['name']}"])
            case 429:
                all_headers.append([f"Too many requests: failed to retrieve data from {website['name']}"])
            case 500:
                all_headers.append([f"Internal server error {response.status_code}: failed to retrieve data from {website['name']}"])
            case _:
                all_headers.append([f"Failed to retrieve data from {website['name']}: {response.status_code}"])

    return all_headers


def CsvSaving(all_headers):
    headers_list = [[] for _ in range(len(all_headers))]
    for counter in range(len(all_headers)):
        headers_list[counter].extend(all_headers[counter])

    with open('team_Artiom_Bikalpa_Seifalislam_scraping_results.csv', 'w', newline='') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow([website['name'] for website in websites])
        csvwriter.writerow(["Current information was collected on: " + time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())])
        csvwriter.writerow([website['link'] for website in websites])
        max_length = 0
        for counter in range(len(headers_list)):
            if len(headers_list[counter]) > max_length:
                max_length = len(headers_list[counter])
        
        for counter in range(len(headers_list)):
            if len(headers_list[counter]) < max_length:
                headers_list[counter] += [""] * (max_length - len(headers_list[counter]))

        for counter in range(len(headers_list[0])):
            csvwriter.writerow([header[counter] for header in headers_list])
    
    print("\n---------------------------------------------------------------")
    print("|Headers extraction results were saved to scraping_results.csv|")
    print("---------------------------------------------------------------\n")


def Searching(all_headers):
    headers_list = [[] for _ in range(len(all_headers))]
    for counter in range(len(all_headers)):
        headers_list[counter].extend(all_headers[counter])

    user_input = input("Enter the keywords to search for devided by a comma:\n")
    print("\nSeaching results:")
    print(f"{'Website':<20} | {'Keyword':<20} | Article")
    print("-----------------------------------------------------")
    search_list = [element.strip() for element in user_input.split(",")]
    search_result = []

    for keyword in search_list:
        keyword_result = {}
        keyword_result["Keyword"] = keyword
        for counter in range(len(headers_list)):
            keyword_result[websites[counter]['name']] = []
            for header in headers_list[counter]:
                if keyword.lower() in header.lower():
                    keyword_result[websites[counter]['name']].append(header)
                    print(f"{websites[counter]['name']:<20} | {keyword:<20} | {header}")
        search_result.append(keyword_result)
    
    with open('team_Artiom_Bikalpa_Seifalislam_searching_results.json', 'w') as file:
            json.dump(search_result, file, indent=4)

    print("\n--------------------------------------------------------")
    print("|Searching results were saved to searching_results.json|")
    print("--------------------------------------------------------\n")

            

results = Scraping()
CsvSaving(results)
Searching(results)



