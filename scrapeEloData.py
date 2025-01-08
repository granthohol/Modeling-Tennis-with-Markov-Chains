import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_elo(player_name: str, surface: str):
    response = requests.get('https://tennisabstract.com/reports/atp_elo_ratings.html')

    # check for successful request
    if response.status_code == 200:
        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table(s) in the HTML (assuming the first table)
        table = soup.find('table', {'id': 'reportable'})
        
        # Extract data from the table and store it in a list of lists
        data = []
        for row in table.find_all('tr'):
            row_data = []
            for cell in row.find_all(['th', 'td']):
                row_data.append(cell.text.strip())
            data.append(row_data)

        # Convert the list of lists into a DataFrame
        df = pd.DataFrame(data)
        
        ########## Cleaning Data Frame #############

        # Rearrange the df so that we have the right headers
        df.columns = df.iloc[0]  # Set the first row as the column headers
        df = df.drop(0)  # Drop the first row, which is now redundant
        df = df.reset_index(drop=True)  # Reset the index

        df = df.drop(df.columns[4], axis=1)  # Drop empty column by index
        df = df.drop(df.columns[10], axis=1)  # Drop another empty column by index

        # Convert appropriate columns to float
        cols_to_float = ['Elo', 'hElo', 'cElo', 'gElo']
        df[cols_to_float] = df[cols_to_float].astype(float)

        # Strip and standardize case for the Player column
        df['Player'] = df['Player'].str.strip().str.title()  # Strips whitespace and ensures proper casing
        df['Player'] = df['Player'].str.replace('\xa0', ' ', regex=True)

        ####### Extract the elo data we are looking for #################
        player_row = df[df['Player'] == player_name]

        if surface == 'Hard':
            return player_row['hElo']
        elif surface == 'Clay':
            return player_row['cElo']
        elif surface == 'Grass':
            return player_row['gElo']
        else:
            raise ValueError("Invalid Playing Surface Parameter")
        
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None    
    

def main():

    df = scrape_elo("Jannik Sinner", "Hard")
    df

if __name__ == "__main__":
    main()    
