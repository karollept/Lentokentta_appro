import random
import sqlite3

# TIETOKANTA
def init_db():
    conn = sqlite3.connect("blackjack.db")
    c = conn.cursor()
   
    c.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            result TEXT,
            player_hand TEXT,
            dealer_hand TEXT
        )
    """)
    conn.commit()
    conn.close()

def record_result(result, player_hand, dealer_hand):
    conn = sqlite3.connect("blackjack.db")
    c = conn.cursor()
    c.execute("INSERT INTO games (result, player_hand, dealer_hand) VALUES (?, ?, ?)",
              (result, str(player_hand), str(dealer_hand)))
    conn.commit()
    conn.close()

# BLACKJACK
cards = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]

def card_value(card):
    if card in ["J","Q","K"]:
        return 10
    elif card == "A":
        return 11  
    else:
        return int(card)

def draw_card(deck):
    return deck.pop()

def calculate_score(hand):
    score = sum(card_value(c) for c in hand)
    # jos yli 21 ja kädessä ässiä, vähennetään arvoa 11 -> 1
    aces = hand.count("A")
    while score > 21 and aces > 0:
        score -= 10  # muutetaan yksi ässä arvosta 11 -> 1
        aces -= 1
    return score

def play_game():
    # Luodaan korttipakka (52 korttia)
    deck = cards * 4
    random.shuffle(deck)

    player_hand = [draw_card(deck), draw_card(deck)]
    dealer_hand = [draw_card(deck), draw_card(deck)]

    # PELAAJAN VUORO
    while True:
        print(f"Pelaajan käsi: {player_hand} (arvo: {calculate_score(player_hand)})")
        if calculate_score(player_hand) > 21:
            print("Yli 21! Hävisit.")
            return "LOSE", player_hand, dealer_hand
        action = input("Otatko lisää (h) vai jäät (j)? ").lower()
        if action == "h":
            player_hand.append(draw_card(deck))
        else:
            break

    # JAKAJAN VUORO
    while calculate_score(dealer_hand) < 17:
        dealer_hand.append(draw_card(deck))

    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    print(f"Jakajan käsi: {dealer_hand} (arvo: {dealer_score})")

    if dealer_score > 21 or player_score > dealer_score:
        print("Voitit!")
        return "WIN", player_hand, dealer_hand
    elif player_score == dealer_score:
        print("Tasapeli.")
        return "DRAW", player_hand, dealer_hand
    else:
        print("Hävisit.")
        return "LOSE", player_hand, dealer_hand

# MAIN
if __name__ == "__main__":
    init_db()
    result, player_hand, dealer_hand = play_game()
    record_result(result, player_hand, dealer_hand)
