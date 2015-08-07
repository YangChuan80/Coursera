# implementation of card game - Memory

import simplegui
import random

card_list=[]
exposed=[]
turn=0
state=0
selected=100
previous_selected=100
second_previous_selected=100

# helper function to initialize globals
def new_game():
    global card_list, exposed, turn, state
    exposed=[False]*16
    turn=0
    state=0    
    card_list=list(range(8))+list(range(8))
    random.shuffle(card_list)
    label.set_text('Turns = '+str(turn))
    
# define event handlers
def mouseclick(pos):
    global exposed, turn, state, selected, previous_selected, second_previous_selected 
    
    for i in range(16):
        if ((i+1)*50-pos[0]>=0) and ((i+1)*50-pos[0]<50) and (pos[1]>0) and (pos[1]<100) and (exposed[i]==False):
            
            second_previous_selected=previous_selected
            previous_selected=selected
            
            selected=i
            exposed[selected]=True  
                       
            if state == 0:
                state = 1

            elif state == 1:
                state = 2
                turn+=1
                if card_list[selected]==card_list[previous_selected]:
                    state=0
                
            elif state==2:                
                exposed[previous_selected]=False
                exposed[second_previous_selected]=False
                state = 1
            break 
            
    label.set_text('Turns = '+str(turn))
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global exposed
    i=0
    for l in card_list:
        l_string=str(l)
        canvas.draw_text(l_string, [50*i+5, 75], 75, "White")
        
        if exposed[i]==False:
            canvas.draw_polygon([(i*50, 0), (i*50+50, 0), (i*50+50, 100), (i*50, 100)], 1, 'Black', 'Green')        
        i+=1

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric