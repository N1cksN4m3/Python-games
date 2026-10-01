import time
import random

def name():
    while True:
        n = input("Insert your nickname:\n")
        if ',' in n:
            print("Error: you cannot use commas in your nickname. Try again.\n")
        else:
            return n

def save(curr_name, curr_money, hands):
    with open("leaderboard_bj.txt", "a") as f:
        f.write(f"{curr_name},{curr_money},{hands}\n")
    return

def leaderboard():
    try:
        with open("leaderboard_bj.txt", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("No leaderboard has been found.")
        return

    records = []
    for r in lines:
        nickname, curr_money, hands = r.strip().split(",")
        records.append((nickname, float(curr_money), int(hands)))

    records.sort(key=lambda x: x[1], reverse=True)

    print("\n=== LEADERBOARD ===")
    for i, (nickname, curr_money, hands) in enumerate(records, 1):
        print(f"{i}. {nickname} - Saldo {curr_money}€ | Mani {hands}")



def wait():
    for i in range(3):
        time.sleep(0.5)
        print(".", end="", flush = True)
    print("\n")
    return

def betting_system(money):


    while True:
        try:
            bet = float(input(
                f"To start insert a bet, right now you have: {money} dollars. Your bet must not be a number equal to zero or less than zero: "))
            if 0 < bet <= money:
                break
            else:
                print("Error: your bet must be higher than zero and cannot be higher that your current money.\n")
        except ValueError:
            print("Unrecognized value. You must insert a valid number.\n")


    money -= bet
    return bet, money

def init_deck():
    new_deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
    random.shuffle(new_deck)
    return new_deck

def draw(current_deck):

    if len(current_deck) == 0:
        print("Deck has ended... Shuffling again...\n")
        wait()
        current_deck.extend(init_deck())

    deck_choice = current_deck.pop()
    return deck_choice


def cards(current_deck):
    print("Starting to deal the cards, it's you against the dealer\n")
    wait()

    user_cards = [draw(current_deck), draw(current_deck)]
    print("Your cards are ", user_cards)
    wait()
    dealer_cards = [draw(current_deck), draw(current_deck)]
    print("The dealer's got a hidden card and ", dealer_cards[1])
    wait()
    return user_cards, dealer_cards


def handvalue(user_cards):
    ace = user_cards.count(11)
    user_hand_value = sum(user_cards)
    while user_hand_value > 21 and ace >= 1:
        user_hand_value -= 10
        ace -= 1
    print("Your hand value is: ", user_hand_value)

    bust = False

    if user_hand_value>21:
        print("BUSTED!!\n")
        wait()
        bust = True

    if user_hand_value == 21:
        print("You achieved 21\n")

    return user_hand_value, bust

def dealershand(dealer_cards, current_deck):

    ace = dealer_cards.count(11)
    dealer_value = sum(dealer_cards)
    while dealer_value > 21 and ace >= 1:
        dealer_value -= 10
        ace -= 1
    print("The dealer's hand value is: ", dealer_value)
    wait()

    while dealer_value < 17:
        print("The dealer draws...\n")
        dealer_cards.append(draw(current_deck))
        print(dealer_cards)
        ace = dealer_cards.count(11)
        dealer_value = sum(dealer_cards)
        if dealer_value > 21 and ace >= 1:
            dealer_value -= 10
            ace -= 1
        print("The dealer's hand value is: ", dealer_value)
        wait()


    if dealer_value == 21:
        print("The dealer's got 21\n")
        wait()

    elif dealer_value > 21:
        print("The dealer busted.\nVictory!!\n")
        dealer_value -= 100000

    return dealer_value


def choice_menu(current_bet, current_money, user_cards, current_deck):
    double = False
    choice = 0

    while choice not in (1, 2, 3):
        try:
            choice = int(input("What do you want to do with your cards?\n1 = Call\n2 = Stay\n3 = Double\n"))
        except ValueError:
            print("Error unrecognized value\n")

    if choice == 1:
        user_cards.append(draw(current_deck))
        wait()
        print(user_cards)
    elif choice == 3:
        user_cards.append(draw(current_deck))
        wait()
        print(user_cards)
        current_money -= current_bet
        double = True
        if current_money <= 0:
            current_money = 0
            print("ALLIN")

    return choice, current_bet, user_cards, current_money, double


def blackjack(user_cards):
    blackjack_v = False
    if sum(user_cards) == 21 and len(user_cards) == 2:
        print("BlackJack!!!")

        blackjack_v = True
    return blackjack_v

def play(current_bet, current_money, user_cards, current_deck):

    while True:
        choice, current_bet, user_cards, current_money, double = choice_menu(current_bet, current_money, user_cards,
                                                                             current_deck)
        hand_value, bust = handvalue(user_cards)

        if bust:
            print("Game over!")
            break


        if hand_value == 21:
          break

        if choice == 2:
            print("It's the dealer's turn\n")
            wait()
            break

        elif choice == 3:
            print("You drawed the last card... It's the dealer turn\n")
            hand_value, bust = handvalue(user_cards)
            if bust:
                print("Game over!")
            wait()
            break

    return hand_value, current_money, bust, user_cards, double

def victory(current_money, hand_value, dealer_value, current_bet, double, current_n_hand):
    if hand_value > dealer_value:
        current_money += (2 * current_bet)
        if double:
            current_money += (2 * current_bet)
        print(f"Congrats!! You won the {current_n_hand} hand, now you have {current_money} dollars.")
    elif hand_value == dealer_value:
        current_money += current_bet
        if double:
            current_money += current_bet
        print(f"Draw!! This was the {current_n_hand} hand, now you have {current_money} dollars.")
    else:
        print(f"You lost!! This was the {current_n_hand} hand, now you have {current_money} dollars.")
    current_n_hand += 1
    return current_money, current_n_hand

def setting_game(current_money, current_hand, current_deck):

    #betting
    current_bet, total_money = betting_system(current_money)

    #user's turn
    user_cards, dealer_cards = cards(current_deck)
    blackjack_v= blackjack(user_cards)

    if blackjack_v:
        if dealer_cards[0]+dealer_cards[1] != 21:
            total_money = total_money + (current_bet * 2.5)
            print(f"You won {current_bet * 1.5} dollars. Now you have {total_money} dollars")

        else:
            print("Draw in blackjack...\n")
            total_money += current_bet

        current_hand += 1
        return total_money, current_hand


    hand_value, total_money, bust, user_cards, double = play(current_bet, total_money, user_cards, current_deck)

    # dealer's turn
    if not bust:
        dealer_value = dealershand(dealer_cards, current_deck)
        total_money, current_hand = victory(total_money, hand_value, dealer_value, current_bet, double,
                                            current_hand)  # victory

    if bust:
        current_hand += 1
        print(f"You busted and lost. Current money: {total_money}")


    return total_money,current_hand

if __name__ == "__main__":
    deck = init_deck()
    blackjack_value = False
    hand = 1
    wallet = 20.0
    print("WELCOME TO PYTHON'S BLACKJACK (by Nicole Betto)!!\n----------------------------------------\n")
    player_name = name()
    wallet, hand = setting_game(wallet, hand, deck)
    while True:
        response = .1

        while response not in (0, 1, 2, 3):
            try:
                response = int(input(
                    "Insert:\n1. If you want to play again \n0. If you want to exit from the program\n2.If you want the leaderboard to show\n3. If you want to save\n"))
            except ValueError:
                print("Value not recognized\n")


        if response == 1:
            print("\n")
            blackjack_value = False
            if wallet == 0:
                print("You finished your money\n")
                break
            wallet, hand = setting_game(wallet, hand, deck)
        elif response == 2:
            leaderboard()
        elif response == 3:
            save(player_name, wallet, hand)
            wait()
            print("Done!")
        else:
            save(player_name, wallet, hand)
            print("Thank you for playing!!")
            break


