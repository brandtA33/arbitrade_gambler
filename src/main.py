from data_api import getData, getManyData
from find_arbitrade import findArb_h2h, findArb_Totals, print_arb_h2h_2, print_arb_h2h_3, print_arb_totals

# main function
# asks user amount to bet
# goes through each event gets best odds and checks if there is possibilities for arbitrade. 
# prints the results

def main(events=None): 
    try: 
        amount = float(input("Enter total amount to bet (€): "))   
        # sport = input("Enter sport from which to import data from or skip with X: " ).strip().lower()
        # if sport =='x' or sport == 'X':
        #     sport == 'upcoming'
        if events is None:
            events = getData()
            # events = getManyData()
        arbitrade_totals = findArb_Totals(events, amount)
        arbitrade_h2h = findArb_h2h(events, amount)
        
        # Sort all arbitrage games by probability descending       
        arbitrade_totals.sort(key=lambda x: x['probability'], reverse=True)
        arbitrade_h2h.sort(key=lambda x: x['probability'], reverse=True)

        total_arbs = len(arbitrade_totals) + len(arbitrade_h2h)
        print("Found total of: ", total_arbs, " games")

        while True:
            print("\nWhich type of games do you want to view?")
            print("1. H2H (Head-to-Head)")
            print("2. Totals")
            print("3. New amount")
            print("q. Quit")      
            game_type_choice = input("Enter choice: ").strip().lower()

            if game_type_choice == 'q':
                print("Exiting.")
                break

            elif game_type_choice == '1': 
                print("\n\n\n-->Showcasing Head-to-Head games: \n")
                if not arbitrade_h2h:
                    print("No arbitrage opportunities found.")
                for arb in arbitrade_h2h: 
                    if arb['type'] == 'h2h_2':
                        print_arb_h2h_2(arb, amount)
                    if arb['type'] == 'h2h_3':
                        print_arb_h2h_3(arb, amount)

            elif game_type_choice == '2': 
                print("\n\n\n-->Showcasing Totals games: \n")
                if not arbitrade_totals:
                    print("No arbitrage opportunities found.")
                for arb in arbitrade_totals:
                    print_arb_totals(arb, amount)

            elif game_type_choice == '3': 
                amount = float(input("\nEnter total amount to bet (€): "))  
                arbitrade_totals = findArb_Totals(events, amount)
                arbitrade_h2h = findArb_h2h(events, amount)
                # Sort all arbitrage games by probability descending       
                arbitrade_totals.sort(key=lambda x: x['probability'], reverse=True)
                arbitrade_h2h.sort(key=lambda x: x['probability'], reverse=True)
                total_arbs = len(arbitrade_totals) + len(arbitrade_h2h)
                print("Found total of: ", total_arbs, " games")
                continue

            elif game_type_choice not in ('1', '2', '3', 'q'):
                print("\n⚠️ Invalid choice. Try again.")
                continue

            input("Type something to continue: ").strip().lower()



    except ValueError:
            print("⚠️ Please enter valid numbers.")

if __name__ == "__main__":
    main()