from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl

def scrape_data(url):    
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, "html.parser")
    
    rows = soup.find_all("tr")
    data = []
    for row in rows:
        word = row.find(class_="column-1").text
        data.append(word)
    return data[1:] # Remove title row

def export_data(data, col):
    df = pd.DataFrame(data)
    try:
        with pd.ExcelWriter("esp_dictionary.xlsx",engine="openpyxl",mode="a",if_sheet_exists="overlay") as writer:
            df.to_excel(writer, sheet_name="Sheet1", header=False, index=False, encoding="utf-8", startcol=col)
    except FileNotFoundError:   # Create excel file if not exists
        df.to_excel("esp_dictionary.xlsx", sheet_name="Sheet1", header=False, index=False, encoding="utf-8", startcol=col)

def next_letter(letter):
    return chr(ord(letter) + 1)

def main():
    col = 0
    letter = 'a'
    # Scrape data
    while(letter != next_letter('z')):
        letter_words = scrape_data("https://howismyspanish.com/spanish-words-start-with-" + letter + "/")
        letter = next_letter(letter)
        # Export data (to excel)
        export_data(letter_words, col)
        col += 1

if __name__ == "__main__":
    main()