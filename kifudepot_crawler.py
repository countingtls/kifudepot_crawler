import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_games_list(url):
    # Send a request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # print(response.text)
        # Find the game list table
        game_list_table = soup.find('table', {'class': 'dataTable'})

        # Check if the table was found
        if game_list_table is not None:
            # Extract the game rows
            game_rows = game_list_table.find_all('tr')[1:]  # Skip the header row

            # Iterate over the game rows and extract the data
            games = []
            for row in game_rows:
                cells = row.find_all('td')
                game = {
                    'td_ev': cells[0].text.strip(),
                    'td_pb': cells[1].text.strip(),
                    'td_pw': cells[2].text.strip(),
                    'td_re': cells[3].text.strip(),
                    'td_dt': cells[4].text.strip(),
                }
                games.append(game)
            
            return games
        else:
            print(f'Error: Game list table not found on {url}')
            return []
    else:
        print(f'Error: Unable to fetch data from {url} (Status Code: {response.status_code})')
        return []

def save_games_to_excel(games, output_file):
    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(games)

    # Save the DataFrame to an Excel file
    df.to_excel(output_file, index=False, engine='openpyxl')
    print(f'Saved games list to {output_file}')

if __name__ == '__main__':
    base_url = 'https://kifudepot.net/index.php?page={page}&move=&player=&event=&sort='
    all_games = []

    # start_page = 1
    start_page = 1
    # last_page = 2399 #the last page number at 2023-05-02, update everyday, 
    last_page = 2400

    # Iterate through the pages
    for page in range(start_page, last_page+1):
        url = base_url.format(page=page)
        print(f'Crawling page {page}')
        games = get_games_list(url)
        all_games.extend(games)

        # Add a delay between requests
        time.sleep(1)

    # Save all the games to an Excel file
    output_file = 'all_games_list.xlsx'
    save_games_to_excel(all_games, output_file)
