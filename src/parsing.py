

# TRUSTED_SITES = {
#     'betfair_ex_eu', 'betsson', 'matchbook', 'coolbet',
#     'nordicbet', 'williamhill', 'sport888', 'marathonbet', 
#     'pinnacle'
# }
TRUSTED_SITES = {'betsson', 'coolbet', 'nordicbet', 'betfair_ex_eu'}
# TRUSTED_SITES = {
#     'betfair_ex_eu', 'betsson', 'coolbet',
#     'nordicbet', 'marathonbet' 
# }
# TRUSTED_SITES = {
#     'betfair_ex_eu', 'betsson', 'coolbet',
#     'nordicbet', 'williamhill', 'sport888', 'marathonbet', 
# }




# Parses events
# TRUSTED_SITES can be upgraded. 
# pinnacle taken out because gives data later than others.
# Returns: name, home, away, time, odds_count and betting_sites
# odds_count is how many odds the first site countered had. usually 2 or 3. 
# betting_sites has site and list of odds. Length of the list is same as odds_count.
def parse_event(event): 

    event_name = event.get('sport_title') + ' ' + event.get('home_team') + ' vs ' + event.get('away_team')
    event_home = event.get('home_team') 
    event_away = event.get('away_team')
    event_time = event.get('commence_time')
    odds_count = 0
    betting_sites = []

    if event.get('bookmakers'):
            first_bookmaker = event['bookmakers'][0]
            markets = first_bookmaker.get('markets', [])
            if markets:
                outcomes = markets[0].get('outcomes', [])
                odds_count = len(outcomes)
    for bookmaker in event.get('bookmakers', []):
        site_name = bookmaker.get('key')
        if site_name not in TRUSTED_SITES:
            continue

        markets = bookmaker.get('markets', [])
        odds = {}
        for market in markets: 
            key = market.get('key')
            outcomes = markets[0].get('outcomes', [])
            if key == 'h2h':
                for outcome in outcomes:
                    odds[outcome['name']] = outcome['price']

        betting_sites.append({
            'site': site_name,
            'odds': odds
        })

    return {
        'name': event_name,
        'home': event_home,
        'away': event_away,
        'time': event_time,
        'odds_count': odds_count,
        'betting_sites': betting_sites
    }

# Parses events
# TRUSTED_SITES can be upgraded. 
# pinnacle taken out because gives data later than others.
# Returns: name, home, away, time, odds_count and betting_sites
# odds_count is always 2 or 0 if no event
# betting_sites has site and list of prices and points. Price is same as Odd.

def parse_totals_event(event):
    
    event_name = event.get('sport_title') + ' ' + event.get('home_team') + ' vs ' + event.get('away_team')
    event_home = event.get('home_team')
    event_away = event.get('away_team')
    event_time = event.get('commence_time')
    
    odds_count = 0
    betting_sites = []
    
    for bookmaker in event.get('bookmakers', []):
        site_name = bookmaker.get('key').lower()
        if site_name not in TRUSTED_SITES:
            continue
        
        # Debug print to see what markets are available
        # print(f"Bookmaker: {site_name}")
        for market in bookmaker.get('markets', []):
            # print(f"  Market key: {market.get('key')}")
            if market.get('key') == 'totals':
                outcomes = market.get('outcomes', [])
                odds_count = len(outcomes)
                
                odds = {}
                for outcome in outcomes:
                    odds[outcome['name']] = {
                        'price': outcome['price'],
                        'point': outcome.get('point')
                    }
                
                betting_sites.append({
                    'site': site_name,
                    'odds': odds
                })
    
    return {
        'name': event_name,
        'home': event_home,
        'away': event_away,
        'time': event_time,
        'odds_count': odds_count,
        'betting_sites': betting_sites
    }
