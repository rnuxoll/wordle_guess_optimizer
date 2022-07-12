import english_words as ew
import random
import string
import copy
import math
import functools


"""
get_five_letter_words():

uses the english_words module to get all five letter words in english
"""
def get_five_letter_words():
    all_words = ew.english_words_lower_set
    five_letter_words = []
    for word in all_words:
        if len(word) != 5:
            continue
        elif not ("." in word or "'" in word):
            five_letter_words.append(word)

    return five_letter_words

"""
generate_random_word():

used to generate an answer for a particular game.
note that this is not necessary in the case where we don't know the word
"""
def generate_random_word():
    pos = get_five_letter_words()
    selected_word = random.choice(get_five_letter_words())
    return selected_word


# todo make compare_word tell you if there are multiple letters in a word
"""
compare_word(actual, guess):

returns feedback as to which letters in the guess might be in the answer, and in what positions
in the following format:

[[letter_1, possible_positions], [letter_2, possible_positions], ...]

where possible positions is a list. It could have one position, zero positions (the empty list), or
all positions in the word, which would be [0, 1, 2, 3, 4]
"""
def compare_word(actual, guess):
    # takes in a word and
    output = []
    # preset yellow_letters to every letter in the alphabet with value zero
    yellow_letters = {letter:0 for letter in string.ascii_lowercase}
    for i in range(len(guess)):
        if guess[i] == actual[i]:
            # output.append('GN')
            output.append([guess[i], [i]])
        elif actual.count(guess[i]) > yellow_letters[guess[i]]:
            # output.append('Y')
            possible_positions = list(range(5))
            possible_positions.remove(i)
            output.append([guess[i], possible_positions])
            yellow_letters[guess[i]] += 1
        else:
            output.append([guess[i], []])
            # output.append('GY')
    return output



"""
returns all of the possibilities in initial_set if and only if
position could be an integer position or a list of possible integer positions
minimum_instances is used to specify if you want to check if a word has a 2nd instance of a letter
(or more generally, an nth instance of a letter)

todo
this should also modify the already_matched list it is passed
the already_matched list is a dictionary in the format {position, letter} and should be reset for every new guess
"""
def match_in_position(character, position, initial_set, already_matched, minimum_instances=1):
    # if position is an integer (or anything besides a list), cast it to a list so it becomes
    # iterable

    final_set = []
    # todo the problem here is that initial_set is equal to zero
    print("initial set =", initial_set)
    for item in initial_set:
        found_instances = 0
        for specific_position in position:
            if item[specific_position] == character:
                # the following lines will prevent double-matching multiple instances to the same position
                if specific_position in already_matched.keys():
                    if item == already_matched[specific_position]:
                        break # stop looking for matches at positions that have already been matched
                else:
                    already_matched[specific_position] = item
                    found_instances += 1
                if found_instances >= minimum_instances:
                    final_set.append(item)
                    break

    return final_set


"""
eliminate_no_occurances(character, initial_set)

given a character and a set of possible words, make the set into the subset of possible words
that does not include the character (i.e. remove the words that do)

does not return anything. instead, it modifies initial_set
"""

#todo is there an efficient way to write this so that match_in_position handles this in the same loop
# as the other loop
def remove_no_occurances(character, initial_set):
    for word in initial_set:
        if character in word:
            initial_set.remove(word)

    return None

"""
given some wordle feedback in the following format

[[letter_1, possible_positions], [letter_2, possible_positions], ...]

returns the set of words in the initial
"""


#todo check again and make sure that it knows that the second n cannot be in position 2
# otherwise it might meet the requirements for both ns just by having an n in position 2
# e.g. "banal" would meet both requirements
"""
look at this interesting feedback case and make sure it handles it
possibility=  tenon
guess=  penna
[['p', []], ['e', [1]], ['n', [2]], ['n', [0, 1, 2, 3, 4]], ['a', []]]
"""

def return_possibilities(feedback, initial_set):
    # for letter in feedback_set:
    #     if letter
    current_set = copy.copy(initial_set)

    # todo the current problem in the code is with this loop that gets the current set
    # rails
    #
    # Would meet the feedback
    #
    # [r, [0, 1, 3, 4]]
    # [r, [0, 1, 2, 4]]
    #
    # Which is generated by a a word like “carry”

    # todo so the problem is that it can match feedback that should imply the word has two occurances of the letter
    # todo to words that only have one, since each occurance is

    matched_letters_and_positions = dict() # this should store which letters have been matched, and in what positions?

    for letter in feedback:
        if letter[1] == []:
            remove_no_occurances(letter[0], current_set)
        else:
            # this automatically incorporates double letters
            print("letter= ", letter)
            # letter[0] gives the letter in char form
            # letter[1] gives the set of possible positions
            current_set = match_in_position(letter[0], letter[1], current_set, matched_letters_and_positions)

    return current_set

"""
calculates the entropy of each guess in the guess space using the possibility space
"""
def calculate_entropy_of_possibility_space(guess_space, possibility_space):
    size_of_possibility_space = len(possibility_space)
    for guess in guess_space:
        possible_feedback = []
        for possibility in possibility_space:
            # to calculate the bits of information from a guess, calculate the set all the possible feedback
            # from that guess (which is found by calculating the feedback for each thing in the guess space)
            # then, for each feedback, the amount by which it narrows down your possibilities is given by
            # number_of_possibilities_matching_feedback / number_of_possibilities
            # or (number_of_possibilities | feedback) / number_of_possibilities
            # take -log_2 of the above number to get the bits of information

            # to get it for a guess, multiply all possible feedback by the probability of getting that feedback
            # and then sum it up

            # todo make the program compute the entropy of all guesses from the initial possibility set to save time
            # todo and save the information in a separate file

            # todo incorporate word frequency data
            feedback = compare_word(possibility, guess)
            # print("possibility= ", possibility)
            # print("guess= ", guess)
            # print(feedback)
            # print()
            possibilities = return_possibilities(feedback, possibility_space)
            possibility_percentage = len(possibilities) / size_of_possibility_space

            # todo we get a math.domain error for cases where return possibilities returns 0 possibilities (which are necessarily erroneous)
            try:
                information = -1 * math.log2(possibility_percentage)
            except ValueError as e:
                print(e)
                print("possibility= ", possibility)
                print("guess= ", guess)
                print("possibility percentage= ", possibility_percentage)
                print("end of error message")
                quit()

            print("possibility = ", possibility)
            print("guess = ", guess)
            print(information)
            print()

            # possible error source
            # rails Would meet the feedback
            #
            # [r, [0, 1, 3, 4]]
            # [r, [0, 1, 2, 4]]
            #
            # Which is generated by a word like “carry”

            # todo math domain errors
            # math domain error
            # possibility = freud
            # guess = deer
            # end of error message
            # there are zero matches


            possible_feedback.append(feedback)

    return None

    # get all five letter words in English
    five_letter_words = get_five_letter_words()
    # randomly choose a five letter word to be the answer
    # this is currently commented out to represent the usual case where we don't know the answer
    # and this program only tells you what to guess, but doesn't contain and implementation of the game
    # itself
    # answer = random.choice(five_letter_words)

    possibility_space = five_letter_words
    guess_space = copy.copy(possibility_space)

    calculate_entropy_of_possibility_space(guess_space, possibility_space)
    print("done")
    # later, consider adding a distinct guess space if guessing words that are not possible might
    # give more information than words that are in some situations
    while True:
        # for each possibility, calculate all of the possible matches
        break


        # todo decide what breaks the loop when there is no game being simulated
        # if guess==answer:
        #     break

    already_matched = {}
    quit()
    possibilities = match_in_position("r", list(range(5)), already_matched, minimum_instances=2)
    for p in possibilities:
        print(p)
    quit()
    #
    # possibilities = []
    # for word in five_letter_words:
    #     maybe_in_it = True
    #     if word[1] == "a" and word[2] == "r":
    #         letters_not_in_it = "edbtsyiphnc"
    #         for letter in letters_not_in_it:
    #             if letter in word:
    #                 maybe_in_it = False
    #                 break
    #         if maybe_in_it == True:
    #             possibilities.append(word)
    #         if maybe_in_it == False:
    #             break

    quit()

    return_possibilities()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
