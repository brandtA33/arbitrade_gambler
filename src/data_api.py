import requests
from datetime import datetime, timedelta, timezone
from api_key import API_KEY
SPORT = 'upcoming'
REGIONS = 'eu' 
MARKETS = 'h2h,totals'
# MARKETS = 'totals'
# MARKETS = 'h2h'



# url = f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds'

# Get current UTC time
now_utc = datetime.now(timezone.utc)

# Format in ISO 8601
commence_from = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

# some bullshit
def getManyData(): 
    # SPORTS = ['boxing_boxing', 
    #           'basketball_nba', 
    #           'basketball_wnba', 
    #           'icehockey_nhl', ''
    #           'soccer_uefa_champs_league_qualification']

    SPORTS = [ 'tennis_wta_cincinnati_open',
            'tennis_atp_cincinnati_open']
    
    all_events = []
    for SPORT in SPORTS: 
        url = f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds'

        params = {
            'regions': REGIONS,
            'markets': MARKETS,
            'apiKey': API_KEY,
            'commenceTimeFrom': commence_from
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")

        else:
            print("\n=== API info ===")
            # Check the usage quota
            print('Remaining requests', response.headers.get('x-requests-remaining'))
            print('Used requests', response.headers.get('x-requests-used'))

            events = response.json()
            # for e in events: 
            #     print(e.get('sport_title'), '\n')
            print('Number of events:', len(events))
            all_events.extend(events)

    return all_events

def getData(): 
    SPORT='upcoming'
    url = f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds'

    params = {
        'regions': REGIONS,
        'markets': MARKETS,
        'apiKey': API_KEY,
        'commenceTimeFrom': commence_from
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")

    else:
        print("\n=== API info ===")
        # Check the usage quota
        print('Remaining requests', response.headers.get('x-requests-remaining'))
        print('Used requests', response.headers.get('x-requests-used'))

        events = response.json()
        # for e in events: 
        #     print(e.get('sport_title'), '\n')
        print('Number of events:', len(events))



        return events


def getOnGoingSports(): 
    sports_response = requests.get(
        'https://api.the-odds-api.com/v4/sports', 
        params={
            'api_key': API_KEY
        }
    )   

    if sports_response.status_code != 200:
        print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')

    else:
        print('List of in season sports:')
        sports = sports_response.json()  # Parse JSON content
        for s in sports:
            if s['active']:
                print(s['key'], "-", s['title'], "\n")