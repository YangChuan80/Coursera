# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

#import modules
import simplegui
import random
import math

# Global Variable
number_range=100
remaining_guess=int(math.ceil(math.log(number_range+1, 2)))
secret_number=0

remaining_number=remaining_guess

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number
    global remaining_number
    
    remaining_number=remaining_guess
    print 'New game. Range is from 0 to '+ str(number_range) 
    print 'Number of remaining guesses is '+str(remaining_guess)+'.'
    # remove this when you add your code    
    secret_number=random.randrange(0, number_range)
    print ''    

# define event handlers for control panel
def range100():
    global number_range
    global remaining_guess
    # button that changes the range to [0,100) and starts a new game 
    number_range=100
    remaining_guess=int(math.ceil(math.log(number_range+1, 2)))
    new_game()    

def range1000():
    global number_range
    global remaining_guess
    # button that changes the range to [0,1000) and starts a new game     
    number_range=1000
    remaining_guess=int(math.ceil(math.log(number_range+1, 2)))
    new_game()   
    
def input_guess(guess):
    # main game logic goes here	
    global remaining_number        
    
    print 'Guess was ' + guess + '.'
    guess_number=int(guess)
    
    if secret_number>guess_number:
        remaining_number=remaining_number-1
        
        if remaining_number==0:
            print 'You have run out of guesses. The number is '+str(secret_number)
            print ''
            new_game()
        else:
            print 'Number of remaining guesses is '+str(remaining_number)+'.'
            print 'Higher!'     
            print ''
            
    elif secret_number<guess_number:
        remaining_number=remaining_number-1      
        
        if remaining_number==0:
            print 'You have run out of guesses. The number is '+str(secret_number)
            print ''
            new_game()
        else:
            print 'Number of remaining guesses is '+str(remaining_number)+'.'
            print 'Lower!'
            print ''
            
    else:
        remaining_number=remaining_number-1
        print 'Number of remaining guesses is '+str(remaining_number)+'.'
        print 'Correct!'
        print ''
        new_game()   
    
# create frame
frame=simplegui.create_frame('Guess the Number', 200, 200)

# register event handlers for control elements and start frame
frame.add_button('Range: 0 - 100', range100, 200)
frame.add_button('Range: 0 - 1000', range1000, 200)
frame.add_input('Enter a guess number: ', input_guess, 200)

# call new_game 
new_game()

# always remember to check your completed program against the grading rubric
