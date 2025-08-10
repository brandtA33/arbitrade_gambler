

# Takes list of odds and n as the number of odds.
# calculates the probability and returns it. If result < 1 it means we have an arbitrade.
def total_propability(odds, n):
    if len(odds) != n:
        return 0

    inverse_sum = 0 
    for odd in odds: 
        inverse_sum += 1/odd

    return inverse_sum

def inverse_probs(odds, n):
    if len(odds) != n:
        return -1
    return 1 - total_propability(odds, n)

# Takes two odds and total amount of stakes
# Calculates the stakes for arbitrade game that consist of two odds. 
# Take into consideration that rounding errors may make some stakes lose.
# Returns stakes  for each odd. Stake1 for Odd1 and Stake2 for Odd2 
# or 0,0,0 if no arbitrade
def stakesFor2(odd1, odd2, amount): 
    props = total_propability([odd1, odd2], 2)
    if (props >= 1 or props < 0):
        return [0,0]
    winning_amount = amount/props
    stake1 = winning_amount/odd1
    stake2 = winning_amount/odd2
    ## if both stakes generate more than the amount we bet its a safe bet
    if (stake1*odd1 > amount and stake2*odd2 > amount):
        return [stake1, stake2]
    else:
        return [0,0]
    
def stakesFor2Rounded(odd1, odd2, amount): 
    stake1, stake2 = stakesFor2(odd1, odd2, amount)
    return [round(stake1), round(stake2)]

def stakesFor2Fractions(odd1, odd2):
    return stakesFor3(odd1, odd2, 100)
    
# Takes three odds and total amount of stakes
# Calculates the stakes for arbitrade game that consist of theree odds. 
# Take into consideration that rounding errors may make some stakes lose.
# Returns stakes  or each odd. Stake1 for Odd1 etc.. Or 0,0,0 if no arbitrade
def stakesFor3(odd1, odd2, odd3, amount): 
    props = total_propability([odd1, odd2, odd3], 3)
    if (props >= 1.0 or props < 0.0):
        return [0,0,0]
    winning_amount = amount/props
    stake1 = winning_amount/odd1
    stake2 = winning_amount/odd2
    stake3 = winning_amount/odd3
    ## if the stakes generate more than the amount we bet its a safe bet
    if (stake1*odd1 > amount and stake2*odd2 > amount and stake3*odd3 > amount):
        return [stake1, stake2, stake3]
    else:
        return [0,0,0]

def stakesFor3Rounded(odd1, odd2, odd3, amount): 
    stake1, stake2, stake3 = stakesFor3(odd1, odd2, odd3, amount)
    return [round(stake1), round(stake2), round(stake3)]

def stakesFor3Fractions(odd1, odd2, odd3):
    return stakesFor3(odd1, odd2, odd3, 100)
    


# Takes the home and away team and each sites info. 
# Checks witch site has the biggest odd for home and away teams.
# Returns home and away
# home has the site name and the best home odd.
# away has the site name and the best away odd.
def getBestOdd2(home, away, sites): 
    bestHome = ('', 0.0)
    bestAway = ('', 0.0)
    for site_info in sites: 
        name = site_info['site']
        odds = site_info['odds']
        homeOdd = odds.get(home)
        drawOdd = odds.get('Draw')
        awayOdd = odds.get(away)
        if drawOdd is not None or homeOdd is None or awayOdd is None:
            continue
        if homeOdd > bestHome[1]: 
            bestHome = (name, homeOdd)
        if awayOdd > bestAway[1]: 
            bestAway = (name, awayOdd)
        
    return {
        'home': bestHome,
        'away': bestAway
    } 


# Takes the home and away team and each sites info. 
# Checks witch site has the biggest odd for hometean awayteam and for draw.
# Returns home, draw and away
# home has the site name and the best home odd.
# draw has the site name and the best draw odd.
# away has the site name and the best away odd.
def getBestOdd3(home, away, sites): 
    bestHome = ('', 0.0)
    bestDraw = ('', 0.0)
    bestAway = ('', 0.0)
    for site_info in sites: 
        name = site_info['site']
        odds = site_info['odds']
        # print(f"Checking odds from {name}: {odds}")  # 👈 see what data you are working with
        homeOdd = odds.get(home)
        drawOdd = odds.get('Draw')
        awayOdd = odds.get(away)
        # print(f"[DEBUG] {name} odds:")
        # print(f"  → Home: {homeOdd}, Draw: {drawOdd}, Away: {awayOdd}")

        if drawOdd is None or homeOdd is None or awayOdd is None:
            continue
        if homeOdd > bestHome[1]: 
            bestHome = (name, homeOdd)
        if drawOdd > bestDraw[1]: 
            bestDraw = (name, drawOdd)
        if awayOdd > bestAway[1]: 
            bestAway = (name, awayOdd)
        
    return {
        'home': bestHome,
        'draw': bestDraw,
        'away': bestAway
    } 


# print h2h or totals type of event
def print_event(event_data):
    print(f"Event: {event_data['name']}")
    print(f"Time: {event_data['time']}\n")

    for site in event_data['betting_sites']:
        print(f"Bookmaker: {site['site']}")
        
        h2h = site['odds'].get('h2h')
        if h2h:
            print("  Head to Head Odds:")
            for name, price in h2h.items():
                print(f"    {name}: {price}")

        totals = site['odds'].get('totals')
        if totals:
            print("  Totals Odds:")
            for name, price in totals.items():
                print(f"    {name}: {price}")

        print() 

def getBestOddTotals(sites): 
    bestOver = ('', '', 0.0)
    bestUnder = ('', '', 0.0)
    for site_info in sites: 
        name = site_info['site']
        odds = site_info['odds']

        over = odds.get('Over')
        under = odds.get('Under')
        
        if over is None or under is None:
            continue
        
        overOdd = over.get('price')
        overPoint = over.get('point')
        underOdd = under.get('price')
        underPoint = under.get('point')
        if overOdd is None or underOdd is None:
            continue
        if overOdd > bestOver[2]: 
            bestOver = (name, overPoint, overOdd)
        if underOdd > bestUnder[2]: 
            bestUnder = (name, underPoint, underOdd)
        
    return {
        'over': bestOver,
        'under': bestUnder
    } 
