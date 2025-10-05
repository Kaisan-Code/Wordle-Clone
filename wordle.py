def main():
    import random as r
    import string as st
    
    with open("official_allowed_guesses.txt", "r") as f:
        answers = [line.strip() for line in f]
    
    with open("shuffled_real_wordles.txt", "r") as f:
        allowed_guesses = [line.strip() for line in f]
    
    allowed_guesses.extend(answers)
    
    rules = """
    WORDLE SUMMARY:
    
    Wordle is a word guessing game where players (You and/or others)
    attempt to quess a 5 letter word within 6 tries.
    
    
    There are 3 rules to WORDLE:
    1 - If a letter is GREEN (√) then it is in the correct spot.
    
    2 - If a letter is YELLOW (?) then it is in the word BUT not
    in the correct space.
    
    3 - If a letter if GREY (X) then it is NOT in the word.
    
    
    This version of wordle is compatiable with CUSTOM words!
    Enter "C" when prompted to use a custom word!
    """
    
    
    print("WORDLE MENU")
    
    def type_of_game():
        while True:
          r = input("\nSee the (R)ules or (S)tart playing? - ")
          if not r.lower() in ["r", "s"]:
            print("Invalid Input. Type 'r' to see the rules OR type 's' to start playing.")
          elif r == "r":
            print(f"\n\n{rules}\n")
          else:
            break
    
        while True:
          choice = input("\n(C)ustom or (O)riginal Wordle? - ")
          if not choice.lower() in ["c", "o"]:
            print("Invalid Input. Type 'c' for a custom game OR type 'o' for original wordle.")
          else:
            break
        return choice
    
    
    def original_game():
        return r.choice(answers), 6
    
    
    def custom_game():
        while True:
          custom_or_random_word = input("\n(C)ustom or (R)andom word? - ")
          if not custom_or_random_word.lower() in ["c", "r"]:
            print("Invalid Input. Type 'c' for a custom word OR type 'r' for a random word. - ")
          else:
            break
    
        if custom_or_random_word.lower() == 'c':
          while True:
            answer = input("\nEnter your custom 5 Letter word. - ")
            if len(answer) != 5 or any(char for char in answer if char in "0123456789"):
              print("Invalid word. Please type a word without the use of Digits or Special Characters.")
            else:
              break
        else:
          answer = r.choice(answers)
    
        while True:
          try:
            guesses = int(input("\nHow many guesses? - "))
            if guesses > 0:
              print("\n" * 10)
              break
          except ValueError:
            pass
          print("Incorrect value. Please type an interger greater than 0.")
        return answer, guesses
    
    
    if type_of_game() == 'o':
        answer, guesses = original_game()
    else:
        answer, guesses = custom_game()
        allowed_guesses.append(answer)
    
    print("\n\n5 LENGTH WORDLE")
    
    max_guess = guesses + 1 #To find what guess the user is on.
    letters_list = {l: "_" for l in st.ascii_lowercase}
    
    print(f"\n{guesses} Word Game")
    if input("\nPress ENTER when you are ready to start.") == "dev test":
        print(answer)
    
    
    def check_letters(guess):
        my_set, marks = set(), ""
        
        for i, letter in enumerate(guess):
    
            if letter == answer[i]:
                marks += " √"
                my_set.add(letter)
            
            elif letter in answer and letter in my_set:
                marks += " X"
            
            elif letter in answer:
                #Start (Fixes an Error that occurs if answer is "lanky" and the use inputs "nanny".)
                other_count = 0
    
                for k in range(abs(i - 5)): #How many letters are above the current one.
                    future_l = 4 - k #Next k from the current letter.
                    if answer[future_l] == letter and guess[future_l] == answer[future_l]:
                        other_count += 1
    
                if other_count:
                    marks += " X"
                #End
                else:
                    marks += " ?"
                    my_set.add(letter)
            
            else:
                marks += " X"
        
        marks = marks[1:] #Removes the first letter of the string.
        word_splitted = " ".join(list(guess))
        print(f"\n\n{marks}")
        print(word_splitted)
    
        add_to_letter_list(marks, word_splitted)
    
        if guess == answer:
          return True
        return False
    
    
    def make_suffix(): #For UI purposes
        num_guess = abs(guesses - max_guess)
        suffix_dict = {1: "st", 2: "nd", 3: "rd"}
        
        s = suffix_dict[num_guess] if num_guess < 4 else "th"
        return s
    
    
    def add_to_letter_list(marks, letters):
        for i, j in zip(marks, letters):
            if not i == " " and not j == " ":
                item = letters_list[j]
                if item == "?" and i == "√":
                    letters_list[j] = "√"
                elif item == "_":
                    letters_list[j] = i
    
    
    def print_letters():
        m, l = "", ""
        for i, j in letters_list.items():
            m += f" {j}"
            l += f" {i}"
        m = m[1:]
        l = l[1:]
        print(f"\n{m}\n" + l)
    
    
    while guesses > 0:
        suffix = make_suffix()
        guess = input(f"\nEnter your {abs(guesses - max_guess)}{suffix} guess! - ").lower()
    
        if not guess in allowed_guesses:
            print("Invalid input. Please type a valid English Wordle word.")
            continue
        elif check_letters(guess):
            print("\nYou Win!")
            return
    
        guesses -= 1
        print_letters()
    print("\nYou lost!", f"\nThe word was {answer.upper()}.")

if __name__ == "__main__":
    main()