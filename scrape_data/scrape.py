from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrape_data(url):    
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, "html.parser")
    
    rows = soup.find_all("tr")
    data = []
    for row in rows:
        word = row.find(class_="column-1").text
        data.append(word)
    return data[1:] # remove title row

def export_data(data):
    df = pd.DataFrame(data)
    df.to_excel("esp_dictionary.xlsx", header=False, index=False, encoding="utf-8")

def next_letter(letter):
    return chr(ord(letter) + 1)

def main():
    letter = 'a'
    words = []
    # Scrape data
    while(letter != next_letter('z')):
        letter_words = scrape_data("https://howismyspanish.com/spanish-words-start-with-" + letter + "/")
        words += letter_words
        letter = next_letter(letter)
    # Export data (to excel)
    export_data(words)

if __name__ == "__main__":
    main()