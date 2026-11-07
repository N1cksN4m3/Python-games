from blackjack_v1 import wait, leaderboard
import random

class Deck:
    def __init__(self):
        self.cards = None
        self.reset()
        
    def reset(self):
        self.cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if len(self.cards) == 0:
            self.reset()
        return self.cards.pop()


class Wallet:
    def __init__(self):
        self.money = 200
        self.currbet = 0

    def __str__(self):
        return f'You now have {self.money} dollars available'


    def betting(self,bet: int):
        self.money -= bet
        self.currbet = bet
        if self.money <= 0:
            self.money = 0
            return True
        return False

    def winning(self, double_value=False):
        if double_value:
            self.money += (self.currbet * 4)
        else:
            self.money += (self.currbet * 2)

    def split(self):
        if self.money - self.currbet <= 0:
            self.money = 0
            return True
        else:
            self.money -= self.currbet
            return False

    def draw(self,double_value = False):
        self.money += self.currbet
        if double_value:
            self.money += self.currbet

    def double(self):
        if self.money - self.currbet <= 0:
            self.money = 0
            return True
        else:
            self.money -= self.currbet
            return False


    def blackjack(self):
        self.money += (self.currbet*2.5)

class Hand:
    def __init__(self,curr_deck: Deck,starting_cards=None):

        if starting_cards is not None:
            self.cards = starting_cards
        else:
            self.cards =[curr_deck.draw_card(), curr_deck.draw_card()]

        self.handvalue = self.create_handvalue()
        self.double_value = False


    def add_card(self,curr_deck: Deck):
        self.cards.append(curr_deck.draw_card())
        self.create_handvalue()

    def __str__(self):
        return f"{self.cards} (Value: {self.handvalue})\n"

    def create_handvalue(self):
        ace: int = self.cards.count(11)
        self.handvalue = sum(self.cards)
        while self.handvalue > 21 and ace >= 1:
            self.handvalue -= 10
            ace -= 1

        return self.handvalue

class User:
    def __init__(self):
        self.name = ""
        self.score = 200
        self.hands = 0

    def save_user(self):
        records = {}

        try:
            with open("leaderboard_bj.txt", "r") as f:
                try:
                    next(f)
                except StopIteration:
                    pass
                for line in f:
                    if line.strip():
                        nickname, curr_money, hands = line.strip().split(",")
                        records[nickname.strip()] = {"money": float(curr_money), "hands": int(hands)}
        except FileNotFoundError:
            pass


        records[self.name] = {"money": self.score, "hands": self.hands}

        with open("leaderboard_bj.txt", "w") as f:
            f.write("Nickname -- money -- hands\n")
            for nickname, data in records.items():
                f.write(f"{nickname},{data['money']},{data['hands']}\n")

    def __str__(self):
        return f"name: {self.name} score: {self.score} hands: {self.hands}\n"

    def loaduser(self):
        try:
            with open ("leaderboard_bj.txt", "r") as f:
                try:
                    next(f)
                except StopIteration:
                    pass

                for line in f:
                    if line.strip():
                        nickname,curr_money,hands = line.strip().split(',')

                        if nickname.strip() == self.name:
                            self.score = float(curr_money)
                            self.hands = int(hands)

                            return True


        except FileNotFoundError:
            pass

        return False


def insert_name(curr_user: User):

    while True:
        special: bool = False
        curr_user.name = str(input("Insert your nickname\nNO SPECIAL CHARACTERS ALLOWED\n"))

        for c in curr_user.name:
            if c in (',',';','.',':','_','-','"','<','>','°','#'):
                print("NO SPECIAL CHARACTERS ALLOWED\n")
                special: bool = True

        if not special:
            break

def save_user_fun(curr_user: User,curr_wallet: Wallet,hands: int):
    curr_user.score = curr_wallet.money
    curr_user.hands = hands

    curr_user.save_user()




def betting_system(current_wallet: Wallet):
    while True:
        try:
            while True:
                bet: int = int(input(f'How much do you want to bet??\nYou have {current_wallet.money} dollars\n'))
                if bet <= 0:
                    print("Not valid\n")
                    continue

                if bet >= current_wallet.money:
                    sure: str = input("Are you sure you want to bet all this money? (ALLIN) -- (YES/NO)\n").strip().upper()
                    if sure == "YES":
                        bet = current_wallet.money
                        break
                    if sure == "NO":
                        continue
                    else:
                        print("Not valid\n")

                else:
                    break

            allin: bool = current_wallet.betting(bet)
            break
        except ValueError:
            print("Not valid")
            wait()
    return allin

def check_bj(user_cards: Hand,dealer_cards: Hand,curr_wallet: Wallet):
    if user_cards.handvalue == 21 and len(user_cards.cards) == 2:
        print("You got BLACKJACK\n")
        wait()
        if dealer_cards.handvalue == 21 and len(dealer_cards.cards) == 2:
            print("You tied with the dealer\n")
            wait()
            print(dealer_cards)
            curr_wallet.draw()
            wait()
            print(curr_wallet)

        else:
            print(dealer_cards)
            wait()
            curr_wallet.blackjack()
            print(curr_wallet)


        return True

    return False



def split_menu(user_cards: Hand,curr_wallet: Wallet,curr_deck: Deck):
    while True:
        try:
            c: str = str(input("Do you want to split? (YES/NO)\n")).upper().strip()
            break
        except ValueError:
            print("Not valid\n")


    if c == "YES":

        allin: bool = curr_wallet.split()
        user_firsthand: Hand = Hand(curr_deck, starting_cards=[user_cards.cards[0], curr_deck.draw_card()])
        user_secondhand: Hand = Hand(curr_deck, starting_cards=[user_cards.cards[1], curr_deck.draw_card()])


        print("First hand\n")
        print(user_firsthand)
        wait()

        a, allin = play(user_firsthand,curr_wallet,curr_deck,allin,split = True)

        wait()
        print("Second hand\n")
        print(user_secondhand)
        wait()

        b, allin = play(user_secondhand,curr_wallet,curr_deck,allin,split = True)

        return a + b

    return False



def play(user_cards: Hand,curr_wallet: Wallet,curr_deck: Deck,allin,split=False):

    if not split and len(user_cards.cards) == 2 and user_cards.cards[0] == user_cards.cards[1] and curr_wallet.money >= curr_wallet.currbet:
        split_hand_value = split_menu(user_cards,curr_wallet,curr_deck)
        if split_hand_value is not False:
            return split_hand_value, allin

    while True:
        while True:
            try:
                choice = int(input("What's the next move?\n1.Call\n2.Stay\n3.Fold\n4.Double\nCANNOT DOUBLE ON ALLIN\n"))
                break
            except ValueError:
                print("Not valid")


        if choice == 1:
            print("Drawing card")
            wait()
            user_cards.add_card(curr_deck)
            print(user_cards)
            wait()

            if user_cards.handvalue > 21:
                print("BUSTED!!")
                print(curr_wallet)
                break

            if user_cards.handvalue == 21:
                print("21!!")
                break

        elif choice == 4 and not allin:
            if curr_wallet.money >= curr_wallet.currbet:
                print("Drawing card")
                wait()
                allin = curr_wallet.double()
                if allin:
                    print("ALLIN\n")

                user_cards.double_value = True
                user_cards.add_card(curr_deck)
                print(user_cards)
                wait()

                if user_cards.handvalue > 21:
                    print("BUSTED!!")


                if user_cards.handvalue == 21:
                    print("21!!")

                break

            else:
                print("Insufficient money\n")





        elif choice in (2,3):
            if choice == 3:
                return [], allin
            break


        else:
            print("Enter a valid choice\n")

    return [user_cards], allin


def dealers_play(dealers_cards: Hand,curr_deck: Deck):

    print("Dealer's cards: ", dealers_cards)
    wait()

    while dealers_cards.handvalue < 17:
        print("The dealer's drawing a card\n")
        wait()
        dealers_cards.add_card(curr_deck)
        print(f'The dealer drew a {dealers_cards.cards[-1]}\nCurrent dealers handvalue: {dealers_cards}')
        wait()


    if 17 <= dealers_cards.handvalue <= 21:
        print("The dealer stays\n")

    if dealers_cards.handvalue > 21:
        print("The dealer busted!\n")


def winning_system(user_cards: Hand,dealers_cards: Hand,curr_wallet: Wallet,hands: int):

    #checking if the user has won
    if dealers_cards.handvalue <= 21:
        if user_cards.handvalue > dealers_cards.handvalue:
            print(f"You won the {hands} hand\n")
            curr_wallet.winning(user_cards.double_value)
            wait()
            print(curr_wallet)

        elif user_cards.handvalue < dealers_cards.handvalue:
            print(f"You lost the {hands} hand\n")
            wait()
            print(curr_wallet)

        else:
            print(f"You tied the {hands} hand\n")
            curr_wallet.draw(user_cards.double_value)
            wait()
            print(curr_wallet)
    else:
        print(f"You won the {hands} hand\n")
        curr_wallet.winning(user_cards.double_value)
        wait()
        print(curr_wallet)

    hands += 1

    return hands





def set_game(curr_wallet: Wallet,curr_deck: Deck,hands: int):

    #betting
    allin: bool = betting_system(curr_wallet)
    if allin:
        print("ALLIN\n")

    #user's hand value

    user_cards: Hand = Hand(curr_deck)
    wait()
    print(f'Your cards: {user_cards}\n')



    #dealer's hand value
    dealer_cards: Hand = Hand(curr_deck)
    wait()
    print(f'Dealers cards: {dealer_cards.cards[0]} and the hidden card\n')

    #blackjack checking
    bj: bool = check_bj(user_cards, dealer_cards, curr_wallet)
    if bj:
        hands += 1
        return hands

    #starting user's turn
    hands_played, allin= play(user_cards, curr_wallet, curr_deck, allin)

    valid_hand: bool = False
    for hand in hands_played:
        if hand.handvalue <= 21:
            valid_hand: bool = True

    if valid_hand:
        dealers_play(dealer_cards, curr_deck)

    for i,hand in enumerate(hands_played,1):
        if len(hands_played) > 1:
            print(f"Evaluating hand {i}\n")
            wait()

        if hand.handvalue > 21:
            print(f"You busted with {hand.handvalue}. You've lost your bet!\n")

        else:
            winning_system(hand, dealer_cards, curr_wallet, hands)

    return hands + 1

def menu():
    while True:
        try:
            x = int(input("--------MENU-----------------\n"
                          "1.Play\n"
                          "2.Save\n"
                          "3.Show lead\n"
                          "4.Exit\n"))


            if x in (1,2,3,4):
                return x

        except ValueError:
            print("Not valid")

def load_menu():
    while True:
        try:
            load_value = int(input("\n--------------WELCOME TO PYTHON BLACKJACK (by Nicole Betto)--------------\n\n"
                            "1.New Game\n"
                            "2.Load Game\n"
                            "3.Leaderboard\n"
                            "4.Exit Game\n"))
            if load_value in (1, 2, 3, 4):
                return load_value

        except ValueError:
            print("Not value\n")


def play_loop(curr_user: User,curr_wallet: Wallet,curr_deck: Deck,curr_handnum: int):
    while True:

        if curr_wallet.money <= 0:
            print("No more money left... YOU LOST\n")
            return curr_handnum

        menu_choice: int = menu()


        if menu_choice == 1:

            curr_handnum = set_game(curr_wallet, curr_deck, curr_handnum)


        if menu_choice == 4:
            print("Thanks for playing\n")
            return curr_handnum

        elif menu_choice == 2:
            save_user_fun(curr_user,curr_wallet,curr_handnum)
            print("Saved successfully\n")

        elif menu_choice == 3:
            leaderboard()







if __name__ == "__main__":


    while True:
        load: int = load_menu()

        if load == 1:  #newgame
            wallet: Wallet= Wallet()
            deck: Deck = Deck()
            user: User = User()
            handnumber: int = 1

            insert_name(user)
            handnumber: int = play_loop(user,wallet,deck,handnumber)
            save_user_fun(user, wallet, handnumber)

        elif load == 2:     #loadgame
            wallet: Wallet = Wallet()
            deck: Deck = Deck()
            user: User = User()
            handnumber: int = 1

            insert_name(user)

            if user.loaduser():

                wallet.money = user.score
                handnumber: int = user.hands
                print("Game loaded succesfully\n")

                handnumber: int = play_loop(user, wallet, deck, handnumber)
                save_user_fun(user, wallet, handnumber)

            else:
                print("Game not found")

        elif load == 3:
            #showlead
            leaderboard()
            input("Type anything to go back\n")

        else:       #fullexit
            break