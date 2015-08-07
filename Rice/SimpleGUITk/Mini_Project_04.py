# Implementation of classic arcade game Pong
import simpleguitk as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

def tick():
    global ball_vel, ball_pos    
    ball_pos[0]+=ball_vel[0]
    ball_pos[1]+=ball_vel[1]    

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos=[WIDTH/2, HEIGHT/2]    
    x=random.randrange(120, 240)/400.0
    y=random.randrange(60, 180)/400.0
    
    if direction==RIGHT:
        ball_vel=[x,-y]
    elif direction==LEFT:
        ball_vel=[-x,-y]
        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    paddle1_pos=HEIGHT/2
    paddle1_vel=0

    paddle2_pos=HEIGHT/2
    paddle2_vel=0

    score1=0
    score2=0
    
    direction=random.choice([LEFT, RIGHT])

    spawn_ball(direction)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if ball_pos[1]>=HEIGHT-1-BALL_RADIUS or ball_pos[1]<=BALL_RADIUS:
        ball_vel[1]=-ball_vel[1]    
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, 'White', 'White')
    
    # update paddle's vertical position, keep paddle on the screen    
    paddle1_pos+=paddle1_vel
    paddle2_pos+=paddle2_vel
    
    if paddle1_pos<=0:
        paddle1_pos=0
    elif paddle1_pos>=HEIGHT-1-PAD_HEIGHT:
        paddle1_pos=HEIGHT-1-PAD_HEIGHT
        
    if paddle2_pos<=0:
        paddle2_pos=0
    elif paddle2_pos>=HEIGHT-1-PAD_HEIGHT:
        paddle2_pos=HEIGHT-1-PAD_HEIGHT
        
    # draw paddles
    canvas.draw_polyline([(PAD_WIDTH/2, paddle1_pos), (PAD_WIDTH/2, paddle1_pos+PAD_HEIGHT)], PAD_WIDTH, 'White')
    canvas.draw_polyline([(WIDTH-PAD_WIDTH/2, paddle2_pos), (WIDTH-PAD_WIDTH/2, paddle2_pos+PAD_HEIGHT)], PAD_WIDTH, 'White')
    
    # determine whether paddle and ball collide
    if ball_pos[0]>=WIDTH-1-BALL_RADIUS-PAD_WIDTH:
        if ball_pos[1]<=paddle2_pos+PAD_HEIGHT and ball_pos[1]>=paddle2_pos:
            ball_vel[0]=-1.1*ball_vel[0]
            ball_vel[1]=1.1*ball_vel[1]
        else:
            score1+=1
            spawn_ball(LEFT)
            
    elif ball_pos[0]<=BALL_RADIUS+PAD_WIDTH:
        if ball_pos[1]<=paddle1_pos+PAD_HEIGHT and ball_pos[1]>=paddle1_pos:
            ball_vel[0]=-1.1*ball_vel[0]
            ball_vel[1]=1.1*ball_vel[1]
        else:
            score2+=1
            spawn_ball(RIGHT)
    
    # draw scores
    canvas.draw_text(str(score1), [WIDTH/4, 80], 50, "White")
    canvas.draw_text(str(score2), [WIDTH*3/4, 80], 50, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key==simplegui.KEY_MAP['w']:
        paddle1_vel=-5
    if key==simplegui.KEY_MAP['s']:
        paddle1_vel=5
        
    if key==simplegui.KEY_MAP['up']:
        paddle2_vel=-5
    if key==simplegui.KEY_MAP['down']:
        paddle2_vel=5
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key==simplegui.KEY_MAP['w']:
        paddle1_vel=0
    if key==simplegui.KEY_MAP['s']:
        paddle1_vel=0
        
    if key==simplegui.KEY_MAP['up']:
        paddle2_vel=0
    if key==simplegui.KEY_MAP['down']:
        paddle2_vel=0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.add_button('Retart', new_game, 120)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer=simplegui.create_timer(1, tick)

# start frame
frame.start()
timer.start()
new_game()
