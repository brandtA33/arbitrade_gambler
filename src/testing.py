from math import isclose
from formulas import total_propability, stakesFor2, stakesFor3
import io
import sys
from old_main import main

def test_arbitrage_probs():
    assert isclose(total_propability([2.0, 2.0], 2), 1.0)
    assert isclose(total_propability([3.0, 3.0, 3.0], 3), 1.0)
    assert total_propability([2.3, 1.8], 2) < 1
    assert total_propability([1.90, 3.20, 8.00], 3) < 1
    assert total_propability([2, 2, 3.0], 1) == 0

def test_arbitrage_stakes2():
    assert stakesFor2(2.0, 2.0, 100) == [0, 0]
    assert sum(stakesFor2(2.3, 1.8, 100)) < 100
    assert sum(stakesFor2(2.3, 1.9, 100)) < 100
    assert sum(stakesFor2(1.5, 9.0, 100)) < 100
    assert sum(stakesFor2(1.9, 1.9, 100)) == 0

def test_arbitrage_stakes2():
    stakes3 = stakesFor3(1.9, 3.20, 8.00, 1000)
    assert sum(stakesFor3(1.9, 3.20, 8.00, 950)) < 1000
    print("odd with 1.90: " + str(stakes3[0]) )
    print("odd with 3.20: " + str(stakes3[1]) ) 
    print("odd with 8.00: " + str(stakes3[2]) )


# Replace with your actual module name

def test_main_arbitrage_output():
    # Prepare a simple 2-outcome arbitrage event in realistic format
    test_events = [
        {
            "sport_key": "football_epl",
            "sport_title": "English Premier League",
            "commence_time": "2025-08-07T12:00:00Z",
            "home_team": "Team A",
            "away_team": "Team B",
            "bookmakers": [
                {
                    "key": "betsson",
                    "title": "Betsson",
                    "last_update": "2025-08-07T11:00:00Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-08-07T11:00:00Z",
                            "outcomes": [
                                {"name": "Team A", "price": 2.2},
                                {"name": "Team B", "price": 1.9},
                            ]
                        }
                    ]
                },
                {
                    "key": "betsson",
                    "title": "Betsson",
                    "last_update": "2025-08-07T11:05:00Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-08-07T11:05:00Z",
                            "outcomes": [
                                {"name": "Team A", "price": 2.1},
                                {"name": "Team B", "price": 2.0},
                            ]
                        }
                    ]
                }
            ]
        }
    ]

    # Capture stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output

    main(test_events)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert "Recommended Bets" in output
    assert "Team A" in output or "Team B" in output
    assert "Guaranteed Profit" in output

def test_main_no_arbitrage_output():
    # Prepare event with no arbitrage in realistic format
    test_events = [
        {
            "sport_key": "football_epl",
            "sport_title": "English Premier League",
            "commence_time": "2025-08-07T20:00:00Z",
            "home_team": "Team X",
            "away_team": "Team Y",
            "bookmakers": [
                {
                    "key": "betsson",
                    "title": "Betsson",
                    "last_update": "2025-08-07T19:00:00Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-08-07T19:00:00Z",
                            "outcomes": [
                                {"name": "Team X", "price": 1.2},
                                {"name": "Team Y", "price": 3.0},
                            ]
                        }
                    ]
                }
            ]
        }
    ]

    captured_output = io.StringIO()
    sys.stdout = captured_output

    main(test_events)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert "No arbitrage opportunities found." in output
