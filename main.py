import random
import time

template_deck = [
    "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH", "AH",  # Hearts
    "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD", "AD",  # Diamonds
    "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC", "AC",  # Clubs
    "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS", "AS"   # Spades
]

print(f"\n\n{'#' * 50}\n")
print('Welcome to Crazy Eights!\n')
print(f"{'#' * 50}\n")


def gameloop():
    deck = template_deck
    players = get_number_of_players() + 1

    print('Shuffling Cards...\n')
    time.sleep(2)
    random.shuffle(deck)

    print('Dealing Cards...')
    time.sleep(2)
    hands, deck = deal_hands(players, deck)
    faceup = deck.pop()

    while True:
        for player in range(1, players + 1):
            if len(deck) == 0:
                deck = template_deck
                deck.remove(faceup)
                random.shuffle(deck)
            faceup, hands, deck, finished = players_turn(player, deck, hands, faceup)
            if finished:
                print(f'Player {player} has won the game!')
                print(f"{'#' * 50}\n\n")
                exit()



def get_number_of_players():
    while True:
        returned = input('How many opponents do you want? (1-3): ')
        returned = returned.strip()
        if returned in ["1", "2", "3"]:
            print('')
            return int(returned)

def deal_hands(num_of_players, deck):
    players_hands = {}
    for i in range(1, num_of_players + 1):
        players_hands[f'player_{i}'] = []

    for i in range(0, 8):
        for j in range(1, num_of_players + 1):
            players_hands[f'player_{j}'].append(deck.pop())

    return players_hands, deck

def display_hands(hands, faceup):
    print(f"\n{'#' * 50}")
    for player, hand in hands.items():
        if player == 'player_1':
            print(f"Your Hand: " + " ".join([f"[{_}]" for _ in hand]))
        else:
            print(f"{player.capitalize()}: " + " ".join(["[XX]" for _ in hand]))
    print(f"\nCurrent face up card: [{faceup}]")
    print(f"{'#' * 50}\n")

def players_turn(player, deck, hands, faceup):
    if player == 1:
        time.sleep(1)
        display_hands(hands, faceup)
        hand = hands['player_1']
        print('Pickup A Card [P]')
        print("Your Cards are: ", end="")
        for index, card in enumerate(hand):
            print(f"[{card}][{index}] ", end="")
        print('\n')

        while True:
            returned = input('What would you like to do?: ')
            returned = returned.strip()
            if returned.isdigit() and 0 <= int(returned) < len(hand):
                returned = int(returned)
                chosen_card = hand[returned]

                if chosen_card[-1] == faceup[-1] or (len(faceup) > 1 and chosen_card[:-1] == faceup[:-1]):
                    hands['player_1'].remove(chosen_card)
                    faceup = chosen_card
                    if len(hands['player_1']) > 0:
                        finished = False
                    else:
                        finished = True
                    return faceup, hands, deck, finished
                elif chosen_card[0] == '8' :
                    print(f"\nYou played a wild 8!")
                    while True:
                        returned = input(f'Which suit would you like to change it to? [H][0], [D][1], [C][2], [S][3]: ')
                        if returned in ["0", "1", "2", "3"]:
                            suits = {"0": 'H', "1": 'D', "2": 'C', "3": 'S'}
                            hands['player_1'].remove(chosen_card)
                            faceup = suits[returned]
                            if len(hands['player_1']) > 0:
                                finished = False
                            else:
                                finished = True
                            return faceup, hands, deck, finished
            elif returned.lower() == 'p':
                pickup = deck.pop()
                print(f'\nYou picked up a [{pickup}]')
                hands['player_1'].append(pickup)
                return faceup, hands, deck, False
    else:
        time.sleep(2)
        print(f"\nPlayer {player}'s Turn")
        time.sleep(2)
        print(f'Player {player} is thinking...')
        time.sleep(2)
        hand = hands[f'player_{player}']
        
        for card in hand:
            if card[-1] == faceup[-1] and card[:-1] != "8":
                faceup = card
                hands[f'player_{player}'].remove(card)
                print(f'Player {player} has played [{card}]')
                finished = len(hands[f'player_{player}']) == 0
                return faceup, hands, deck, finished

        for card in hand:
            if card[:-1] == faceup[:-1] and card[:-1] != "8": 
                faceup = card
                hands[f'player_{player}'].remove(card)
                print(f'Player {player} has played [{card}]')
                finished = len(hands[f'player_{player}']) == 0
                return faceup, hands, deck, finished
        
        for card in hand:
            if card[0] == '8':
                print(f'Player {player} has played a wild 8!')
                
                suit_count = {'H': 0, 'D': 0, 'C': 0, 'S': 0}
                for item in hand:
                    suit_count[item[-1]] += 1
                
                highest_suit = max(suit_count, key=suit_count.get)
                faceup = highest_suit
                hands[f'player_{player}'].remove(card)
                print(f'Player {player} changed the suit to {highest_suit}')
                finished = len(hands[f'player_{player}']) == 0
                return faceup, hands, deck, finished
        
        print(f"Player {player} could not play and picked up a card")
        pickup = deck.pop()
        hands[f'player_{player}'].append(pickup)
        return faceup, hands, deck, False
        
gameloop()
    