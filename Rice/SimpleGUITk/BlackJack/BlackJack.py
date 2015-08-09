# Mini-project #6 - Blackjack

import simpleguitk as simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("https://raw.githubusercontent.com/Tritiums/Coursera/master/Rice/SimpleGUITk/BlackJack/Images/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("https://raw.githubusercontent.com/Tritiums/Coursera/master/Rice/SimpleGUITk/BlackJack/Images/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):        
        self.hand_list=[] # create Hand object

    def __str__(self):
        return str([str(hand) for hand in self.hand_list])	# return a string representation of a hand

    def add_card(self, card):
        self.hand_list.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value=0
        
        for hand in self.hand_list:
            value+=VALUES[hand.get_rank()]
        current_ranks=[hand.get_rank() for hand in self.hand_list]
        
        if ('A' in current_ranks) and (value+10<=21):
            value=value+10 
            
        return value  # compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        i=0
        for card in self.hand_list:
            card.draw(canvas, [pos[0]+i*90, pos[1]])
            i+=1 
            # draw a hand on the canvas, use the draw method for cards
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck_list=[Card(suit, rank) for suit in SUITS for rank in RANKS]		# create a Deck object

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck_list)    # use random.shuffle()

    def deal_card(self):
        return self.deck_list.pop(0)	# deal a card object from the deck
    
    def __str__(self):
        return str([str(deck) for deck in self.deck_list])	# return a string representing the deck



#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, deck, score       
    outcome=''
    
    if in_play==True:
        score-=1
    
    player=Hand()
    dealer=Hand()
    
    deck=Deck()
    deck.shuffle()
    
    card1=deck.deal_card()
    player.add_card(card1)
    
    card2=deck.deal_card()
    dealer.add_card(card2)
    
    card3=deck.deal_card()
    player.add_card(card3)
    
    card4=deck.deal_card()
    dealer.add_card(card4)
    
    in_play = True

def hit():
    # replace with your code below
    global outcome, in_play, player, dealer, deck, score
    
    if in_play==True: 
    # if the hand is in play, hit the player    
        if player.get_value()<=21:
            player.add_card(deck.deal_card())

        # if busted, assign a message to outcome, update in_play and score
        if player.get_value()>21:        
            outcome='You went bust and lose!'
            in_play=False        
            score-=1

def stand():
    # replace with your code below
    global outcome, in_play, player, dealer, deck, score
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while (in_play==True) and (dealer.get_value()<=17):
        dealer.add_card(deck.deal_card())
        
    if (in_play==True) and (dealer.get_value()>17):
        outcome='Dealer\'s value is larger than 17!'
        in_play=False
        
        if dealer.get_value()>21:
            outcome='Dealer went bust! You win!'            
            score+=1

        else:
            if player.get_value()<=dealer.get_value():
                outcome='You lose!'                
                score-=1
                
            else:
                outcome='You Win!'
                score+=1
    # assign a message to outcome, update in_play and score    
    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global outcome, in_play, player, dealer, deck, score
    
    canvas.draw_text('Blackjack', [50, 80], 40, "Aqua")
    canvas.draw_text('Dealer', [50, 170], 30, "Black")
    canvas.draw_text('Player', [50, 390], 30, "Black")
    canvas.draw_text(outcome, [230, 170], 25, "Black")
    canvas.draw_text('Score: '+str(score), [400, 80], 30, "Black")   
    
    if in_play==False:
        dealer.draw(canvas, [50, 200])
        player.draw(canvas, [50, 420])
        canvas.draw_text('New deal?', [230, 390], 30, "Black")
    else:        
        dealer.draw(canvas, [50, 200])
        player.draw(canvas, [50, 420])
        canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, [50+CARD_CENTER[0], 200+CARD_CENTER[1]], CARD_SIZE)
        canvas.draw_text('Hit or stand?', [230, 390], 30, "Black")        
        
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
# remember to review the gradic rubric
