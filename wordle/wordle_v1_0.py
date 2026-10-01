import time
import random

def wait():

    for _ in range(3):

        time.sleep(0.3)
        print(".", end = "", flush = True)
        time.sleep(0.3)

    print("\n")


def create_wordle():
    try:
        with open("wordle_list.txt") as words:
            list_w = []
            for line in words:

                if line.strip():
                    list_line = line.strip().split(",")
                    clean_line = []

                    for dirty_word in list_line:

                        if dirty_word.strip():

                            cleaned_word = dirty_word.strip().lower()
                            clean_line.append(cleaned_word)

                            if cleaned_word not in list_w:
                                if len(cleaned_word) == 5:
                                    list_w.append(cleaned_word)
            print(list_w)

            return list_w


    except FileNotFoundError:
        print("The file does not exist")
        found = False
        return found


def chose_word(lista_w):

    x = random.choice(lista_w)
    print(f"The word has been chosen...")
    wait()

    return x

def first_guess(x, lists_w):

    while len(x) != 5:
        print("An error has occurred")
        wait()
        x = chose_word(lists_w)

    while True:
        guess = input("Take a guess\n")
        if len(guess.strip()) != 5:
            print("Try again... \n Your guess has to be a 5 letter word\n")
            wait()
            continue

        if guess.strip() not in lists_w:
            print("The word you chose is not supported or does not exist... Try again!\n")
            wait()
            continue

        if guess.strip() == x:
            print("\nResult:\n")
            findit = True
            return  guess.strip(), findit

        else:
            findit = False

        return guess, findit


def first_guess_analysis(guess,x,right_letters,not_right_letters):

    for letter in guess:
        if letter not in right_letters and letter in x:
            right_letters.append(letter)

        elif letter not in not_right_letters and letter not in x:
            not_right_letters.append(letter)


    print(f"Letters that appear both in your guesses and in the chosen word: \n{right_letters}")
    print(f"Letters that appear in your guesses but not in the chosen word: \n{not_right_letters}")

    for i in range(len(guess)):
        if guess[i] == x[i]:
            print(f"Letter {guess[i]} having position {i+1} is right!\n")

    print("Take another guess!!\n")
    give_up_value = ""

    while give_up_value.upper() not in ("YES", "NO"):
        give_up_value = input("Do you want to give up?  (YES/NO)\n")

        if give_up_value.upper() == "YES":
            print(f"The correct word was: {x}")
            give_up_value = True
            return give_up_value

        else:
            give_up_value = False
            return give_up_value

    return None


if __name__ == "__main__":

    right = []
    not_right = []
    full_list = create_wordle()
    if not full_list:
        wait()
        print("File has not been found  :(")
    else:
        chosen_word = chose_word(full_list)

        find = False
        give_up = False
        tries = 0

        while not find and not give_up:

            tries += 1
            print(f"--- Try {tries} ---")

            g, find = first_guess(chosen_word, full_list)

            if find:
                print(f"You guessed the word in {tries} tries")
                break

            give_up = first_guess_analysis(g, chosen_word, right, not_right)