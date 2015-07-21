# Rock-paper-scissors-lizard-Spock template
import random

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

def name_to_number(name):
    # delete the following pass statement and fill in your code below
    if name=='rock':
        number=0
    elif name=='Spock':
        number=1
    elif name=='paper':
        number=2
    elif name=='lizard':
        number=3
    elif name=='scissors':
        number=4
    else:
        print 'No such name!'
        
    return number

    # convert name to number using if/elif/else
    # don't forget to return the result!


def number_to_name(number):
    # delete the following pass statement and fill in your code below
    if number==0:
        name='rock'
    elif number==1:
        name='Spock'
    elif number==2:
        name='paper'
    elif number==3:
        name='lizard'
    elif number==4:
        name='scissors'
    else:
        print 'No such number!'
    return name    
    # convert number to a name using if/elif/else
    # don't forget to return the result!

def judge(player_choice_number, comp_choice_number):
    d=(player_choice_number-comp_choice_number)%5
    
    if d==0:
        r='This is a tie'
    if d==1:
        r='Player wins!'
    if d==2:
        r='Player wins!'
    if d==3:
        r='Computer wins!'
    if d==4:
        r='Computer wins!'
    return r

def rpsls(player_choice_name): 
    # delete the following pass statement and fill in your code below
        
    # print a blank line to separate consecutive games
    print ''

    # print out the message for the player's choice
    print 'Player chooses '+player_choice_name

    # convert the player's choice to player_number using the function name_to_number()
    
    player_choice_number=name_to_number(player_choice_name)

    # compute random guess for comp_number using random.randrange()
    
    comp_choice_number=random.randrange(0, 5)

    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice_name=number_to_name(comp_choice_number)
    
    # print out the message for computer's choice
    print 'Computer chooses '+comp_choice_name

    # compute difference of comp_number and player_number modulo five

    # use if/elif/else to determine winner, print winner message
    
    result=judge(player_choice_number, comp_choice_number)
    print result

    
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric


