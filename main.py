import random
import time

template_deck = [
    "2❤️", "3❤️", "4❤️", "5❤️", "6❤️", "7❤️", "8❤️", "9❤️", "10❤️", "J❤️", "Q❤️", "K❤️", "A❤️",  # Hearts
    "2💎", "3💎", "4💎", "5💎", "6💎", "7💎", "8💎", "9💎", "10💎", "J💎", "Q💎", "K💎", "A💎",  # Diamonds
    "2♣️", "3♣️", "4♣️", "5♣️", "6♣️", "7♣️", "8♣️", "9♣️", "10♣️", "J♣️", "Q♣️", "K♣️", "A♣️",  # Clubs
    "2♠️", "3♠️", "4♠️", "5♠️", "6♠️", "7♠️", "8♠️", "9♠️", "10♠️", "J♠️", "Q♠️", "K♠️", "A♠️"   # Spades
]

print(f"\n\n{'#' * 50}")
print('Welcome to Crazy Eights!\n')

def gameloop():
    deck = template_deck
    players = get_number_of_players() + 1

    print('Shuffling Cards...\n')
    time.sleep(2)
    random.shuffle(deck)

    print('Dealing Cards...\n')
    time.sleep(2)
    hands, deck = deal_hands(players, deck)
    faceup = deck[-1]

    display_hands(hands, faceup)

    while True:
        for player in range(1, players + 1):
            faceup, hands, deck, finished = players_turn(player, deck, hands, faceup)
            if finished:
                print(f'Player {player} has won the game!')
                print(f"{'#' * 50}\n\n")
                break



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
    print(f"{'#' * 50}")
    for player, hand in hands.items():
        if player == 'player_1':
            print(f"Your Hand: " + " ".join([f"[{_}]" for _ in hand]))
        else:
            print(f"{player.capitalize()}: " + " ".join(["[XX]" for _ in hand]))
    print(f"\nCurrent face up card: [{faceup}]")
    print(f"{'#' * 50}\n")

def players_turn(player, deck, hands, faceup):
    if player == 1:
        print("Your Turn:\n")
        hand = hands['player_1']
        print
        print(f"Current Face-up Card is [{deck[-1]}]")
        print('Pickup A Card: [P]')
        print("Your Cards are: ", end="")
        for index, card in enumerate(hand):
            print(f"[{card}][{index}] ", end="")
        print('')

        while True:
            returned = input('Which Card Would You Like To Play?: ')
            returned = returned.strip()
            if returned.isdigit() and hand[int(returned)]:
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
                        returned = input(f'Which suit would you like to change it to? [❤️][0], [💎][1], [♣️][2], [♠️][3]: ')
                        if returned in ["0", "1", "2", "3"]:
                            suits = {"0": '❤️', "1": '💎', "2": '♣️', "3": '♠️'}
                            hands['player_1'].remove(chosen_card)
                            faceup = suits[returned]
                            if len(hands['player_1']) > 0:
                                finished = False
                            else:
                                finished = True
                            return faceup, hands, deck, finished
            elif returned.lower() == 'p':
                pickup = deck.pop()
                print(f'You picked up a [{pickup}]')
                hands['player_1'].append(pickup)
                return faceup, hands, deck, False
    else:
        print(f"Player {player}'s Turn")
        print(f'Player {player} is thinking..')
        time.sleep(1)
        hand = hands[f'player_{player}']
        for card in hand:
            if card[-1] == faceup[-1]:
                faceup = card
                hands[f'player_{player}'].remove(card)
                print(f'Player {player} has played [{card}]')
                if len(hands[f'player_{player}']) > 0:
                    finished = False
                else:
                    finished = True
                return faceup, hands, deck, finished
        for card in hand:
            if card[:-1] == faceup[:-1] and not card[:-1] == "8":
                faceup = card
                hands[f'player_{player}'].remove(card)
                print(f'Player {player} has played [{card}]')
                if len(hands[f'player_{player}']) > 0:
                    finished = False
                else:
                    finished = True
                return faceup, hands, deck, finished
        for card in hand:
            if card[:-1] == "8":
                suit_count = {'❤️': 0, '💎': 0, '♣️': 0, '♠️': 0}
                for item in hand:
                    suit_count[item[-1]] += 1
                highest_count = max(suit_count, key=suit_count.get)
                faceup = highest_count
                hands[f'player_{player}'].remove(card)
                print(f'Player {player} has played a wild 8 and changed the suit to {highest_count}')
                if len(hands[f'player_{player}']) > 0:
                    finished = False
                else:
                    finished = True
                return faceup, hands, deck, finished
        print(f"Player {player} could not play and picked up a card")
        pickup = deck.pop()
        hands[f'player_{player}'].append(pickup)
        return faceup, hands, deck, False
        

        

                





gameloop()
    