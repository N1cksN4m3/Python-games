import time

GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

from wordle_v1_0 import wait,create_wordle,chose_word,first_guess


def insert_nick():
    nick = input("Insert a NICKNAME: \n")
    while not nick.strip():
        nick = input("Insert a NICKNAME: \n")
    return nick


def save(nick,tries):
    with open("leaderboard.txt", "a") as lead:
        lead.write(f"{nick}, {tries}\n")
    return

def show_lead():
    print("LEADERBOARD\n", "-"*30,"\n")
    diz_lead = {}
    with open("leaderboard.txt") as lead:
        for line in lead:
            name,score = (line.strip().split(","))
            diz_lead[name] = score
        def sort(thing):
            return thing[1]

        for k,v in sorted(diz_lead.items(), key = sort):
            print(k,":",v)


def first_guess_analysis(guess,x,not_right):
    letter_list = list(x)
    block = ["", "", "", "", ""]
    print("\nResult: \n")


    for i in range(len(guess)):
        if guess[i] == x[i]:
            block[i] = GREEN + "[" + guess[i].upper() + "]" + RESET
            letter_list.remove(guess[i])

    for i in range(len(guess)):
        if block[i] == "":
            if guess[i] in letter_list:
                block[i] = YELLOW + "[" + guess[i].upper() + "]" + RESET
                letter_list.remove(guess[i])

            else:
                block[i] = "[" + guess[i].upper() + "]"
                if guess[i] not in not_right:
                    not_right.append(guess[i])

    for part in block:
        print(part, end ="", flush=True)
        time.sleep(0.5)

    wait()
    print(f"\nLetter you used and that are wrong:\n {sorted(not_right)}")


    give_up = ""

    while give_up.upper() not in ("YES","NO"):
        give_up = input("Do you want to give up?  (YES/NO)\n")

        if give_up.upper() == "YES":
            print(f"The correct word was: {x}")
            give_up = True
            return give_up

        else:
            give_up = False
            return give_up

    return None


def chose_difficulty():
    while True:
        diff = input("Chose your mode (EASY / CLASSIC / HARD): ").strip().upper()

        if diff == "EASY":
            return 15
        elif diff == "CLASSIC":
            return 6
        elif diff == "HARD":
            return 4
        else:
            print("Invalid. Try again.")

def print_real(x):
    for char in range(len(x)):
        print(GREEN + "[" + x[char].upper() + "]" + RESET, end="", flush=True)
        time.sleep(0.5)
    print("\n")



def game():
    print("Welcome to WORDLE 2.0 \n")
    print("-" * 30)

    nickname = insert_nick()

    not_right = []
    full_list = create_wordle()
    if not full_list:
        wait()
        print("File not found  :(")
    else:
        chosen_word = chose_word(full_list)

        find = False
        tries = 0

        mode = chose_difficulty()

        while not find and tries < mode:

            print("Take a guess!!\n")

            tries += 1

            print(f"--- Try {tries} ---")
            print(f"You have {mode - tries} tries left")

            g, find = first_guess(chosen_word, full_list)

            if find:
                print_real(chosen_word)
                print(f"You guessed in {tries} tries")

                save(nickname, tries)
                show_lead()
                break

            first_guess_analysis(g, chosen_word, not_right)


        if not find:
            print(f"What a shame... :(\n The word was {chosen_word}")

            show_lead()
if __name__ == "__main__":

    while True:
        game()
        stop = input("Want to play again? (YES/NO)").strip().upper()
        if stop == "NO":
            break



