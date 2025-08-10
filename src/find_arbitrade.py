from formulas import (total_propability, getBestOdd2, getBestOdd3, stakesFor3Rounded, stakesFor3Fractions,
                       stakesFor2Rounded, stakesFor2Fractions, print_event, getBestOddTotals)

from parsing import parse_event, parse_totals_event


# finds arbitrade games for totals

def findArb_Totals(events, amount): 
    arbitradeGames = []
    if (events):
        for event0 in events: 
            event = parse_totals_event(event0)
            home = event['home']
            away = event['away']
            sites = event['betting_sites']
            n = event['odds_count']
            # print(event, '\n')
            total_bet = amount
            if event: 
                sites_t = event['betting_sites']
                result1 = getBestOddTotals(sites_t)
                overOdd = result1['over']
                underOdd = result1['under']
                if (overOdd[2] == 0 or underOdd[2] == 0 or underOdd[1] != overOdd[1]):
                    continue
                probs = total_propability([underOdd[2], overOdd[2]],2)
                if (probs < 1): 
                    # Calculate stakes proportional to the inverse of odds
                    overStake, underStake = stakesFor2Rounded(overOdd[2], underOdd[2], total_bet)
                    # Calculate profit for either outcome
                    win_over = overStake * overOdd[2]
                    win_under = underStake * underOdd[2]
                    guaranteed_profit = min(win_over, win_under) - total_bet
                    if (guaranteed_profit < 0):
                        continue

                    arbitradeGames.append({
                        'event': event,
                        'type': 'totals',
                        'stakes': (overStake, underStake),
                        'odds': (overOdd, underOdd),
                        'profits': (win_over, win_under),
                        'guaranteed_profit': guaranteed_profit,
                        'probability': probs
                })
    return arbitradeGames

            
# finds arbitrade games for h2h
def findArb_h2h(events, amount): 
    arbitradeGames = []
    if (events):
        for event0 in events: 
            event = parse_event(event0)
            home = event['home']
            away = event['away']
            sites = event['betting_sites']
            n = event['odds_count']
            # print(event_totals, '\n')
            total_bet = amount

            if (n == 2): 
                result0 = getBestOdd2(home, away, sites)
                bestHome_site_odd = result0['home']
                bestAway_site_odd = result0['away']
                if (bestHome_site_odd[1] == 0 or bestAway_site_odd[1] == 0):
                    continue

                probs = total_propability([bestHome_site_odd[1], bestAway_site_odd[1]], 2)
                if (probs < 1): 
                    # Calculate stakes proportional to the inverse of odds
                    homeStake, awayStake = stakesFor2Rounded(bestHome_site_odd[1], bestAway_site_odd[1], total_bet)
                    # Calculate profit for either outcome
                    win_home = homeStake * bestHome_site_odd[1]
                    win_away = awayStake * bestAway_site_odd[1]
                    guaranteed_profit = min(win_home, win_away) - total_bet
                    if (guaranteed_profit < 0):
                        continue

                    arbitradeGames.append({
                        'event': event,
                        'type': 'h2h_2',
                        'stakes': (homeStake, awayStake),
                        'odds': (bestHome_site_odd, bestAway_site_odd),
                        'profits': (win_home, win_away),
                        'guaranteed_profit': guaranteed_profit,
                        'probability': probs
                    })


            elif (n == 3): 
                result0 = getBestOdd3(home, away, sites)
                bestHome_site_odd = result0['home']
                bestAway_site_odd = result0['away']
                bestDraw_site_odd = result0['draw']
                if (bestHome_site_odd[1] == 0 or bestAway_site_odd[1] == 0 or bestDraw_site_odd[1] == 0):
                    continue
                probs = total_propability([bestHome_site_odd[1], bestDraw_site_odd[1], bestAway_site_odd[1]], 3)

                if (probs < 1):
                    # Calculate stakes proportional to the inverse of odds
                    homeStake, drawStake, awayStake = stakesFor3Rounded(bestHome_site_odd[1], bestDraw_site_odd[1], bestAway_site_odd[1], total_bet)
                    # Calculate profit for each outcome
                    win_home = homeStake * bestHome_site_odd[1]
                    win_draw = drawStake * bestDraw_site_odd[1]
                    win_away = awayStake * bestAway_site_odd[1]
                    guaranteed_profit = min(win_home, win_draw, win_away) - total_bet
                    if (guaranteed_profit < 0):
                        continue

                    arbitradeGames.append({
                        'event': event,
                        'type': 'h2h_3',
                        'stakes': (homeStake, drawStake, awayStake),
                        'odds': (bestHome_site_odd, bestDraw_site_odd, bestAway_site_odd),
                        'profits': (win_home, win_draw, win_away),
                        'guaranteed_profit': guaranteed_profit,
                        'probability': probs
                    })
    return arbitradeGames

def print_arb_h2h_2(arb, amount):
    event = arb['event']
    if arb['type'] == 'h2h_2':
        homeStake, awayStake = arb['stakes']
        bestHome_site_odd, bestAway_site_odd = arb['odds']
        win_home, win_away = arb['profits']
        guaranteed_profit = arb['guaranteed_profit']
        probs = arb['probability']
        if ((1-probs) > 0.03): 
            print("\n=== SUPER BETS ===")
        else: 
            print("\n=== Recommended Bets ===")
        print(f"Game €{event['name']} at {event['time']} (probability: {probs:.4f})")
        print(f"\nGuaranteed Return: €{min(win_home, win_away):.2f}")
        print(f"Total Bet: €{amount:.2f}")
        print(f"Guaranteed Profit: €{guaranteed_profit:.2f}")
        print(f"\nBet €{homeStake:.2f} on {event['home']} at {bestHome_site_odd[0]} (odds: {bestHome_site_odd[1]}) (winning: {win_home:.2f})")
        print(f"Bet €{awayStake:.2f} on {event['away']} at {bestAway_site_odd[0]} (odds: {bestAway_site_odd[1]}) (winning: {win_away:.2f})")
        if (probs > 0):
            print(f"Guaranteed Profit margin: %{(100*1/probs):.4f}")
        print("=" * 30 + "\n")
 
def print_arb_h2h_3(arb, amount): 
    event = arb['event']
    if arb['type'] == 'h2h_3':
        homeStake, drawStake, awayStake = arb['stakes']
        bestHome_site_odd, bestDraw_site_odd, bestAway_site_odd = arb['odds']
        win_home, win_draw, win_away = arb['profits']
        guaranteed_profit = arb['guaranteed_profit']
        probs = arb['probability']

        print("\n=== Recommended Bets ===")
        print(f"Game €{event['name']} at {event['time']} (probability: {probs:.4f})")
        print(f"\nGuaranteed Return: €{min(win_home, win_draw, win_away):.2f}")
        print(f"Total Bet: €{amount:.2f}")
        print(f"Guaranteed Profit: €{guaranteed_profit:.2f}")
        print(f"\nBet €{homeStake:.2f} on {event['home']} at {bestHome_site_odd[0]} (odds: {bestHome_site_odd[1]}) (winning: {win_home:.2f})")
        print(f"Bet €{drawStake:.2f} on draw at {bestDraw_site_odd[0]} (odds: {bestDraw_site_odd[1]}) (winning: {win_draw:.2f})")
        print(f"Bet €{awayStake:.2f} on {event['away']} at {bestAway_site_odd[0]} (odds: {bestAway_site_odd[1]}) (winning: {win_away:.2f})")
        if (probs > 0):
            print(f"Guaranteed Profit margin: %{(100*1/probs):.4f}")
        print("=" * 30 + "\n")

def print_arb_totals(arb, amount): 
    event = arb['event']
    if arb['type'] == 'totals': 
        overStake, underStake = arb['stakes']
        overOdd, underOdd = arb['odds']
        win_over, win_under = arb['profits']
        guaranteed_profit = arb['guaranteed_profit']
        probs = arb['probability']
        event = arb['event']

        # overOdd and underOdd have form: [site_name, point, price]
        print("\n=== Recommended Totals Bets ===")
        print(f"Game €{event['name']} at {event['time']} (probability: {probs:.4f})")
        print(f"\nGuaranteed Return: €{min(win_over, win_under):.2f}")
        print(f"Total Bet: €{amount:.2f}")
        print(f"Guaranteed Profit: €{guaranteed_profit:.2f}")
        print(f"\nBet €{overStake:.2f} on Over {overOdd[1]} at {overOdd[0]} (odds: {overOdd[2]}) (winning: {win_over:.2f})")
        print(f"Bet €{underStake:.2f} on Under {underOdd[1]} at {underOdd[0]} (odds: {underOdd[2]}) (winning: {win_under:.2f})")

        if probs > 0:
            print(f"Guaranteed Profit margin: %{(100*1/probs):.4f}")

        print("=" * 30 + "\n")