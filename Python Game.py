# ***********************************************************
# Program: AMMAR_AZRIN-ADDINA_AMLI-WAIEE_ZAINOL.py
# Course: PSP0101 PROBLEM SOLVING AND PROGRAM DESIGN
# Class: TT02
# Year: 2020/21 Trimester 1
# Names: MUHAMMAD_AMMAR_BIN_MUHAMAD_AZRIN | ADDINA_BINTI_MOHD_AMLI | MUHAMMAD_WAIEE_BIN_ZAINOL
# IDs: 1191102915 | 1201100480 | 1191103225
# Emails: 1191102915@student.mmu.edu.my | 1201100480@student.mmu.edu.my | 1191103225@student.mmu.edu.my
# Phones: +60 19-892 7574 | +60 11-1004 8372 | +60 12-627 5758
# *************************************************************

import random
import psphelper

# Defining functions that will be used #
def turnUnderscore(quote, con_letter, vow_letter):

    quote_copy = ["?"]*len(quote)

    for i in range(len(quote)):
        if quote[i].upper() not in con_letter and quote[i].upper() not in vow_letter:
            quote_copy[i] = psphelper.alphaToUnderscore(quote[i])
        else:
            quote_copy[i] = quote[i]

    new_quote = ''.join(quote_copy)
    return new_quote

def mainInterface(quote, player_money, current_player):
    title = "..:: C.O.V.I.D ::.."
    width = 50
    print(title.center(width))
    psphelper.showQuoteScreen(quote, 50)

    print() # Money Screen
    print(f'Player 1: RM {player_money[0]}')
    print(f'Player 2: RM {player_money[1]}')
    print(f'Player 3: RM {player_money[2]}')

    print() # Input Options
    print('Input Options:')
    print('	/            :- Solve the puzzle')
    print('	a vowel      :- Buy a vowel')
    print('	a consonant  :- Guess a consonant')

    print()
    print(f'Player {current_player + 1}')
    print('========')

def cheat_function(quote, consonant):
    consonant_dict = {}
    for x in consonant:
        consonant_dict[x] = quote.count(x)

    return consonant_dict

def highest_frequency(con_dict):
    max_freq = max(con_dict, key=con_dict.get)

    return max_freq

def remove_guessed_cons(cons_list, guessed_letter):
    y = []
    for x in cons_list:
        y.append(x)

    for x in guessed_letter:
        y.remove(x)
    return y

def reset_screen(current_answer, current_player):
    psphelper.clearScreen()
    mainInterface(current_answer, player_money, current_player)

def reset_player(curr_player):
    if curr_player > 2:
        return 0
    else:
        return curr_player


# Declaration of Players, Money, and Cheat usage #
current_player = 0 # Player 1 starts
player_money = [0, 0, 0] # [p1, p2, p3]'s money
player_cheat = [False, False, False] # [p1, p2, p3]'s cheat usage

# Declaration of Game Variables #
isPuzzleSolved = False
current_answer = ""
alphabets = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N',
                'O','P','Q','R','S','T','U','V','W','X','Y','Z')
vow_list = ('A','E','I','O','U')
con_list = ('B','C','D','F','G',
            'H','J','K','L','M',
            'N','P','Q','R','S',
            'T','V','W','X','Y',
            'Z')
dice = (500, 600, 700, 800, 900, 1000, "Bankrupt", "Lose a turn")
guessed_vows = []
guessed_cons = []

# Read quotes from quotes.txt and randomly choosing a quote then display the hidden quote.
quotes = psphelper.readQuotesFromFile("quotes.txt")
chosen_quote = random.choice(quotes)

quote_answer = chosen_quote.upper()
quote_listed = list(quote_answer)

changed_quote = turnUnderscore(quote_listed, guessed_cons, guessed_vows)
mainInterface(changed_quote, player_money, current_player)

# Game Logic
while isPuzzleSolved == False:
    current_answer = turnUnderscore(quote_listed, guessed_cons, guessed_vows)

    if current_answer != quote_answer:
        user_input = input("Input > ").upper()

        ### To give final answer and solve the quote ###
        if user_input == "/":
            final_answer = input("Solve it > ").upper()
            
            if final_answer == quote_answer:
                player_money[current_player] *= 2
                print("Congratulations! You have solved it. Your money is doubled.\nPress ENTER to end the game.")
                input("")
                current_answer = quote_answer
                reset_screen(current_answer, current_player)
                isPuzzleSolved = True

            else:
                print("WRONG SOLUTION!\nYour turn ends. Press ENTER to end turn.")
                input("")
                current_player += 1
                current_player = reset_player(current_player)
                reset_screen(current_answer, current_player)

        ### To input an alphabet, separated by 2 situations; a vowel or a consonant ###
        elif user_input in alphabets:

            ### To guess and purchase a vowel ###
            if user_input in vow_list:
                vow_count = quote_answer.count(user_input)
                vow_price = vow_count * 200
                
                if vow_count > 0 and user_input not in guessed_vows:

                    if player_money[current_player] - vow_price >= 0:
                        player_money[current_player] -= vow_price
                        guessed_vows.append(user_input)
                        current_answer = turnUnderscore(quote_listed, guessed_cons, guessed_vows)
                        print(f"Found {vow_count} letter {user_input}.\nYou have spent RM{vow_price}.\nPress ENTER to continue play.")
                        input("")
                        reset_screen(current_answer, current_player)

                    else:
                        print("Insufficient money.\nPress ENTER to continue play.")
                        input("")
                        reset_screen(current_answer, current_player)

                elif vow_count == 0:
                    print(f"Sorry. There is no letter {user_input}.\nYour turn ends. Press ENTER to end turn.")
                    input("")
                    current_player += 1
                    current_player = reset_player(current_player)
                    reset_screen(current_answer, current_player)

                elif user_input in guessed_vows:
                    print(f"Letter {user_input} has been taken.\nPress ENTER to continue play.")
                    input("")
                    reset_screen(current_answer, current_player)
            
            ### To guess a consonant and roll a dice for prize ###
            elif user_input in con_list:
                con_count = quote_answer.count(user_input)
                dice_index = random.randint(0, 7)
                dice_value = dice[dice_index]
                
                if con_count > 0 and user_input not in guessed_cons:

                    if dice_index >= 0 and dice_index <= 5:
                        con_prize = int(dice_value) * con_count
                        player_money[current_player] += con_prize
                        guessed_cons.append(user_input)
                        current_answer = turnUnderscore(quote_listed, guessed_cons, guessed_vows)
                        print(f'You rolled "RM{dice_value}".\nFound {con_count} letter {user_input}.\nYou earned RM {con_prize}.\nPress ENTER to continue play.')
                        input("")
                        reset_screen(current_answer, current_player)

                    elif dice_value == "Bankrupt":
                        player_money[current_player] = 0
                        print(f'You rolled "{dice_value}".\nSorry, you lose all your money.\nYour turn ends. Press ENTER to end turn.')
                        input("")
                        current_player += 1
                        current_player = reset_player(current_player)
                        reset_screen(current_answer, current_player)

                    elif dice_value == "Lose a turn":
                        print(f'You rolled "{dice_value}".\nYou have lost your turn, sorry.\nPress ENTER to lose turn.')
                        input("")
                        current_player += 1
                        current_player = reset_player(current_player)
                        reset_screen(current_answer, current_player)

                elif con_count == 0:
                    print(f"Sorry. There is no letter {user_input}.\nYour turn ends. Press ENTER to end turn.")
                    input("")
                    current_player += 1
                    current_player = reset_player(current_player)
                    reset_screen(current_answer, current_player)

                elif user_input in guessed_cons:
                    print(f"Letter {user_input} has been taken.\nPress ENTER to continue play.")
                    input("")
                    reset_screen(current_answer, current_player)

        ### To input the cheat command, for hinting the most frequent consonant and to change player's money ###
        elif "CHEAT" in user_input:

            if player_cheat[current_player] == False:
                cheat_input = user_input.replace("CHEAT", "")

                ### When user inputs only CHEAT, to find out available consonants. ###
                if cheat_input == "":
                    new_con_list = remove_guessed_cons(con_list, guessed_cons)
                    final_count_dict = cheat_function(quote_answer, new_con_list)
                    max_frequency = highest_frequency(final_count_dict)
                    player_cheat[current_player] = True

                    if final_count_dict[max_frequency] == 0:
                        print("Sorry, no more consonants available.\nPress ENTER to continue play.")
                        input("")
                        reset_screen(current_answer, current_player)
                    
                    else:
                        print(f"There are {final_count_dict[max_frequency]} letter {max_frequency}.\nPress ENTER to continue play.")
                        input("")
                        reset_screen(current_answer, current_player)
                
                ### When user inputs CHEAT together with a positive integer to change money. ###
                else:
                    amount = cheat_input.replace(" ", "")
                    if amount.isnumeric():

                        if int(amount) >= 0:
                            amount_int = int(amount)
                            player_money[current_player] = amount_int
                            player_cheat[current_player] = True
                            print(f"Money changed to RM {amount_int}.\nYour turn ends. Press ENTER to end turn.")
                            input("")
                            current_player += 1
                            current_player = reset_player(current_player)
                            reset_screen(current_answer, current_player)
                        else:
                            print("Invalid input.")
                    else:
                        print("Invalid input.")
            else:
                print("No more cheat available.\nPress ENTER to continue play.")
                input("")
                reset_screen(current_answer, current_player)
        
        else:
            print("Invalid input.")
    else:
        isPuzzleSolved = True

# Ending the Game!
if isPuzzleSolved == True:
    psphelper.clearScreen()
    title = "..:: C.O.V.I.D ::.."
    width = 50
    print(title.center(width))
    psphelper.showQuoteScreen(current_answer, 50)
    print() # Money Screen
    print(f'Player 1: RM {player_money[0]}')
    print(f'Player 2: RM {player_money[1]}')
    print(f'Player 3: RM {player_money[2]}')
    print()

# Quote is solved, whoever is the richest at the end wins the game.
p1 = player_money[0]
p2 = player_money[1]
p3 = player_money[2]

if p1 > p2 and p1 > p3:
    print("Player 1 wins.\n\nGame Ends.")
elif p2 > p1 and p2 > p3:
    print("Player 2 wins.\n\nGame Ends.")
elif p3 > p1 and p3 > p2:
    print("Player 3 wins.\n\nGame Ends.")
elif p1 == p2 or p1 == p3 or p2 == p3:
    print("It's a tie.\n\nGame Ends.")
elif p1 == p2 and p2 == p3 and p1 == p3:
    print("It's a tie.\n\nGame Ends.")