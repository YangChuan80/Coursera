# template for "Stopwatch: The Game"
# import the module
import simpleguitk as simplegui

# define global variables
time_general=0
time_string='0:00.0'
score_string='0/0'
running=False
trying=0
winning=0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global time_string, score_string
    
    decisecond=t%10
    minute=t/600   
    second=(t-minute*600)/10
    if second<10:
        second_str='0'+str(second)
    elif second>=10:
        second_str=str(second)
        
    time_string=str(minute)+':'+second_str+'.'+str(decisecond)
    
    score_string=str(winning)+'/'+str(trying)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global running
    
    timer.start()
    running=True
    
def stop():
    global running, trying, winning
    
    timer.stop()
    if running==True:
        trying+=1
        if time_string[-2:]=='.0':
            winning+=1
    format(time_general)        
    running=False

def reset():
    global time_general, winning, trying, running
    
    timer.stop()
    time_general=0
    winning=0
    trying=0
    format(time_general)
    running=False

# define event handler for timer with 0.1 sec interval
def elapse():
    global time_general
    time_general+=1
    format(time_general)
    
# define draw handler
def draw(canvas):
    canvas.draw_text(time_string, [40, 120], 50, "White")
    canvas.draw_text(score_string, [130, 32], 40, "Green")
    
# create frame
frame=simplegui.create_frame('Stopwatch', 200, 200)

# register event handlers
frame.add_button('Start', start, 120)
frame.add_label('')
frame.add_button('Stop', stop, 120)
frame.add_label('')
frame.add_button('Reset', reset, 120)

frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, elapse)

# start frame
frame.start()

# Please remember to review the grading rubric
