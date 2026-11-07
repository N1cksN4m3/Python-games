import unittest
import os
import tempfile

from blackjack_v2_0 import check_bj
from blackjack_v2_0 import Deck, Wallet, Hand, User

class DeckTest(unittest.TestCase):
    def test_more_than_one_ace(self):
        """Testing wether the deck as the right number of cards"""
        deck: Deck = Deck()

        self.assertEqual(len(deck.cards), 52, "Cards should be 52")

        ten_count = deck.cards.count(10)
        self.assertEqual(ten_count, 16, "The deck should contain 16 10s")

        ace_count = deck.cards.count(11)
        self.assertEqual(ace_count,4,"Aces should be 4")

    def test_check_auto_reset(self):
        """Testing wether the deck will reset itself after finishing the 52 cards"""

        deck: Deck = Deck()

        for _ in range(0,53):
            deck.draw_card()

        self.assertEqual(len(deck.cards),51,"The deck should contain 51 cards")

class WalletTest(unittest.TestCase):
    def test_allin_betting(self):
        """Testing wether the allin system works"""

        wallet: Wallet = Wallet()

        allin = wallet.betting(250)

        self.assertEqual(wallet.money, 0, "Current money should be zero")
        self.assertTrue(allin, "Allin should be True")

    def test_split_money(self):
        """Testing wether the split paying system works"""

        wallet: Wallet = Wallet()
        wallet.betting(50)

        wallet.split()

        self.assertEqual(wallet.money,100,"Money should be starting wallet (200) minus 50 minus 50 (100)")

    def test_winning(self):
        """Testing wether the win paying system works"""

        wallet: Wallet = Wallet()
        wallet.money = 50
        wallet.betting(50)

        wallet.winning()

        self.assertEqual(wallet.money, 100, "Wallet money should be 100: bet * 2 --> 50 * 2")


        wallet.money = 50
        wallet.betting(50)

        wallet.winning(double_value=True)

        self.assertEqual(wallet.money,200,"Wallet money should be 50 * 2 * 2 (200)")

    def test_drawing(self):
        """Testing wether the draw paying system works"""

        wallet: Wallet = Wallet()
        wallet.money = 50
        wallet.betting(50)

        wallet.draw()

        self.assertEqual(wallet.money,50,"Wallet money should be exactly the bet (50)")

        wallet.money = 50
        wallet.betting(50)

        wallet.draw(double_value=True)

        self.assertEqual(wallet.money, 100, "Wallet money should be exactly the bet * 2 (100)")


    def test_blackjack_winning(self):
        """Testing wether the blackjack paying system works"""


        wallet: Wallet = Wallet()
        wallet.money = 100
        wallet.betting(100)

        wallet.blackjack()

        self.assertEqual(wallet.money, 250, "Wallet money should be bet * 2.5 = 250")




class HandTest(unittest.TestCase):
    def test_multiple_aces(self):
        """Testing wether the and value will multiple aces will remain stable"""
        deck: Deck = Deck()
        hand: Hand = Hand(deck, starting_cards=[11,11,11,11])

        self.assertEqual(hand.handvalue, 14,"The hand value should be 14")

        hand2: Hand = Hand(deck, starting_cards=[11,11])

        self.assertEqual(hand2.handvalue,12,"The hand value shuld be 12")

    def test_soft_hand(self):
        """Testing wether the hand value will go down if there's an ace in the hand and the value is higher than 21"""
        deck: Deck = Deck()
        hand: Hand = Hand(deck, starting_cards=[11,6])

        hand.cards.append(10)

        handvalue = hand.create_handvalue()

        self.assertEqual(handvalue,17,"Handvalue should be 17")

        hand.cards.append(4)
        handvalue = hand.create_handvalue()

        self.assertEqual(handvalue,21,"Handvalue should be 21")

    def test_hard_hand(self):
        """Testing wether the hand value will not change if you bust without having aces"""
        deck: Deck = Deck()
        hand: Hand = Hand(deck, starting_cards=[10,7])

        hand.cards.append(10)

        handvalue = hand.create_handvalue()

        self.assertEqual(handvalue, 27, "Handvalue should be 27")

    def test_natural_bj(self):
        """Testing wether the program will notice the difference between a natural bj and a 21"""

        deck: Deck = Deck()
        hand1: Hand = Hand(deck, starting_cards=[10,11])
        hand2: Hand = Hand(deck, starting_cards=[7,7,7])
        dealers: Hand = Hand(deck)
        wallet: Wallet = Wallet()

        bj = check_bj(hand1,dealers,wallet)

        self.assertTrue(bj,"Value should be True")

        bj = check_bj(hand2,dealers,wallet)

        self.assertFalse(bj,"Value should be False")





class UserTest(unittest.TestCase):

    def setUp(self):
        self.original_cwd = os.getcwd()

        self.temp_dir = tempfile.TemporaryDirectory()

        os.chdir(self.temp_dir.name)

    def tearDown(self):

        os.chdir(self.original_cwd)

        self.temp_dir.cleanup()

    def test_new_file(self):
        """Testing wether save_user() will create a new file with header or not"""
        file_name = "leaderboard_bj.txt"

        self.assertFalse(os.path.exists(file_name))

        user: User = User()
        user.name = "Tester"
        user.score = 200
        user.hands = 0
        user.save_user()

        self.assertTrue(os.path.exists(file_name),"File Leaderboard_bj.txt hasn't been created")

        with open(file_name, "r") as f:
            lines = f.readlines()

        self.assertEqual(len(lines),2,"File length should be of exactly 2 lines")

        expected_header = "Nickname -- money -- hands\n"
        self.assertEqual(lines[0],expected_header,"The line shown should be the same as expected_header")

        expected_record = "Tester,200,0\n"
        self.assertEqual(lines[1],expected_record,"Second line (expected_record) does not match")


    def test_new_users(self):
        """Testing wether the program doen't doplicate already existing users"""

        user1: User = User()
        user1.name = "Alice"
        user1.score = 200
        user1.hands = 0
        user1.save_user()

        user2: User = User()
        user2.name = "Bob"
        user2.score = 200
        user2.hands = 0
        user2.save_user()

        user3: User = User()
        user3.name = "Alice"
        user3.score = 500
        user3.hands = 3
        user3.save_user()

        file_name = "leaderboard_bj.txt"

        with open(file_name, "r") as f:
            lines = f.readlines()


        self.assertEqual(len(lines),3,"There's should be only 3 lines in total (The header + Alice + Bob)")

        expected_alice_record = "Alice,500,3\n"
        self.assertEqual(lines[1],expected_alice_record,"Alice's record should be the one cited")


    def test_loaduser_handling_zero_byte_files(self):
        """Testing wether loaduser() can handle zero byte files gracefully"""


        file_name = "leaderboard_bj.txt"

        with open(file_name, "w"):
            pass

        self.assertTrue(os.path.exists(file_name),"File wasn't created correctly")
        self.assertEqual(os.path.getsize(file_name),0,"File is not zero byte")

        user: User = User()
        user.name = "Tester"

        result = user.loaduser()

        self.assertFalse(result, "loaduser() should return False for an empty file.")
        self.assertEqual(user.score, 200, "User score should retain its default value.")
        self.assertEqual(user.hands, 0, "User hands should retain its default value.")







if __name__ == '__main__':
    unittest.main()
