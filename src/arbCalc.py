
from formulas import stakesFor2, total_propability, stakesFor3

# calculates arbitrade for 2 odds games
def calculate_2ARB(): 
    try: 
        amount = float(input("Enter total amount to bet (€): "))
        odd1 = float(input("Enter first odd: "))
        odd2 = float(input("Enter second odd: "))

        stakes = stakesFor2(odd1, odd2, amount)
        probability = total_propability([odd1, odd2], 2)

        if stakes == [0, 0]:
            print(f"\n❌ No arbitrage opportunity found.")
            print(f"Total implied probability: {probability:.4f}")
        else:
            stake1, stake2 = stakes
            profit = round(min(stake1 * odd1, stake2 * odd2) - amount, 2)
            print(f"\n✅ Arbitrage Opportunity Found!")
            print(f"→ Stake 1: €{stake1}")
            print(f"→ Stake 2: €{stake2}")
            print(f"→ Guaranteed Profit: €{profit}")
            print(f"→ Total implied probability: {probability:.4f}")
            if (probability > 0):
                print(f"→ Guaranteed Profit margin: {(1/probability):.4f}")
    except ValueError:
            print("⚠️ Please enter valid numbers.")

# calculates arbitrade for 3 odds games
def calculate_3ARB(): 
    try: 
        amount = float(input("Enter total amount to bet (€): "))
        odd1 = float(input("Enter first odd: "))
        odd2 = float(input("Enter second odd: "))
        odd3 = float(input("Enter third odd: "))

        stakes = stakesFor3(odd1, odd2, odd3, amount)
        probability = total_propability([odd1, odd2, odd3], 3)

        if stakes == [0, 0, 0]:
            print(f"\n❌ No arbitrage opportunity found.")
            print(f"Total implied probability: {probability:.4f}")
        else:
            stake1, stake2, stake3 = stakes
            min_return = min(stake1 * odd1, stake2 * odd2, stake3 * odd3)
            profit = round(min_return - amount, 2)          
            print(f"\n✅ Arbitrage Opportunity Found!")
            print(f"→ Total implied probability: {probability:.4f}")
            print(f"→ Home Stake: €{stake1}")
            print(f"→ Draw Stake: €{stake2}")
            print(f"→ Away Stake: €{stake3}")
            print(f"→ Guaranteed Profit: €{profit}")
            if (probability > 0):
                print(f"→ Guaranteed Profit margin: {(1/probability):.4f}")

    except ValueError:
            print("⚠️ Please enter valid numbers.")

print("=== Arbitrage Calculator ===")
print("2. 2-way market (e.g. tennis, baseball)")
print("3. 3-way market (e.g. football/soccer)")
choice = input("Choose mode (2 or 3): ")

if choice == '2':
    calculate_2ARB()
elif choice == '3':
    calculate_3ARB()
else:
    print("⚠️ Invalid choice.")