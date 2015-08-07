# program template for Spaceship
import simpleguitk as simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started=False

EXPLOSION_CENTER = [50, 50]
EXPLOSION_SIZE = [100, 100]
EXPLOSION_DIM = [9, 9]

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_info_thrust=ImageInfo([135, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.angle+=self.angle_vel
        accelerate=[0,0]
        
        self.vel[0]*=0.95
        self.vel[1]*=0.95
        
        self.pos[0]+=self.vel[0]
        self.pos[1]+=self.vel[1]
        
        self.pos[0]%=WIDTH
        self.pos[1]%=HEIGHT
        
        if self.thrust==True:
            accelerate=angle_to_vector(self.angle)            
            self.vel[0]+=0.3*accelerate[0]
            self.vel[1]+=0.3*accelerate[1]
            
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
            
    def shoot(self):
        global missle_group
        
        front=angle_to_vector(self.angle)
        
        shoot_vel=angle_to_vector(self.angle) 
        
        missile_group.add(Sprite([self.pos[0]+40*front[0], self.pos[1]+40*front[1]], 
                        [6*shoot_vel[0]+0.95*self.vel[0], 6*shoot_vel[1]+0.95*self.vel[1]], 
                        0, 0, 
                        missile_image, missile_info, missile_sound))
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.sound=sound
        if self.sound:
            self.sound.rewind()
            self.sound.play()   
        
    def draw(self, canvas):
        global time
        if self.animated==False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:  
            canvas.draw_image(self.image, [64 + time % 24*128, 64], [128, 128], self.pos, [128, 128])
            time += 1
    
    def update(self):
        self.pos[0]+=self.vel[0]
        self.pos[1]+=self.vel[1]
        
        self.angle+=self.angle_vel
        
        self.pos[0]%=WIDTH
        self.pos[1]%=HEIGHT
        
        self.age+=1
        
        if self.age>=self.lifespan:
            return True
        else:
            return False
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self, other_object):
        if math.sqrt((self.pos[0]-other_object.get_position()[0])**2+(self.pos[1]-other_object.get_position()[1])**2) <= self.radius+other_object.get_radius():
            return True
        else:
            return False
        
    def far_away(self, other_object):
        if math.sqrt((self.pos[0]-other_object.get_position()[0])**2+(self.pos[1]-other_object.get_position()[1])**2) >= 3*(self.radius+other_object.get_radius()):
            return True
        else:
            return False
        
def draw(canvas):
    global time, rock_group, missle_group, score, started, lives
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text('Lives: '+str(lives), [20, 35], 30, "White")
    canvas.draw_text('Score: '+str(score*10), [660, 35], 30, "White")
    
    process_sprite_group(explosion_group, canvas)
    
    if lives<=0:
        started=False        
        
    if started==True:
        # draw ship and sprites
        my_ship.draw(canvas) 
        
        # update ship and sprites
        my_ship.update()
        
        process_sprite_group(missile_group, canvas)
        process_sprite_group(rock_group, canvas)
        process_sprite_group(missile_group, canvas)
        
        group_collide(rock_group, my_ship)    

        score+=group_group_collide(rock_group, missile_group)  
    elif started==False:
        soundtrack.pause()
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
   
            
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, score
    
    if len(rock_group)<12:
        rock=Sprite([random.randrange(WIDTH), random.randrange(HEIGHT)], 
                              [0.03*(score+10)*random.randint(-2, 2), 0.03*(score+10)*random.randint(-2, 2)],
                              0, 0.04*random.random()*random.choice([1, -1]), 
                              asteroid_image, asteroid_info) 
        if rock.far_away(my_ship):
            rock_group.add(rock)

def process_sprite_group(sprite_set, canvas):
    sprite_copy=set(sprite_set)
    
    for sprite in sprite_copy:
        if sprite.update():
            sprite_set.discard(sprite)
    
    for sprite in sprite_set:
        sprite.draw(canvas)
        
def group_collide(group, other_object):
    global lives, explosion_group
    group_copy=set(group)
    
    for g in group_copy:
        if g.collide(other_object):
            group.discard(g)
            
            explosion_group.add(Sprite([g.pos[0], g.pos[1]], [0, 0],0, 0, 
                              explosion_image, explosion_info, explosion_sound))
            explosion_group.add(Sprite([other_object.pos[0], other_object.pos[1]], [0, 0],0, 0, 
                              explosion_image, explosion_info, explosion_sound))
            lives-=1
            
def group_group_collide(group1, group2):
    group1_copy=set(group1)
    group2_copy=set(group2)
    
    i=0
    
    for g1 in group1_copy:
        for g2 in group2_copy:
            if g1.collide(g2):
                group1.discard(g1)
                group2.discard(g2)
                explosion_group.add(Sprite([g1.pos[0], g1.pos[1]], [0, 0],0, 0, 
                              explosion_image, explosion_info, explosion_sound))
                i+=1                
    return i
    
def keydown(key):
    if started:
        if key==simplegui.KEY_MAP['left']:
            my_ship.angle_vel=-0.08

        if key==simplegui.KEY_MAP['right']:
            my_ship.angle_vel=0.08

        my_ship.angle+=my_ship.angle_vel

        if key==simplegui.KEY_MAP['up']:
            my_ship.thrust=True

            my_ship.image_center = ship_info_thrust.get_center()
            my_ship.image_size = ship_info_thrust.get_size()

            ship_thrust_sound.play()

        if key==simplegui.KEY_MAP['space']:
            my_ship.shoot()
        
def keyup(key):        
    if key==simplegui.KEY_MAP['left'] or key==simplegui.KEY_MAP['right']:
        my_ship.angle_vel=0
    my_ship.angle+=my_ship.angle_vel
        
    if key==simplegui.KEY_MAP['up']:
        my_ship.thrust=False
        my_ship.image_center = ship_info.get_center()
        my_ship.image_size = ship_info.get_size()
        
        ship_thrust_sound.pause()
        ship_thrust_sound.rewind()

def mouseclick(pos):
    if pos[0]<=WIDTH and pos[0]>=0 and pos[1]<=HEIGHT and pos[1]>=0 and started==False:
        restart()
        
def restart():
    global lives, score, started, rock_group, my_ship
    lives=3
    score=0
    started=True
    rock_group=set()
    missile_group=set()
    explosion_group=set()
    
    soundtrack.rewind()
    soundtrack.play()
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

rock_group=set()
rock_group.add(Sprite([random.randrange(WIDTH), random.randrange(HEIGHT)], 
                      [0.3*random.randint(-2, 2), 0.3*random.randint(-2, 2)], 
                      0, 0.04*random.random()*random.choice([1, -1]), 
                      asteroid_image, asteroid_info))

missile_group=set()

explosion_group=set()

# register handlers
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.set_mouseclick_handler(mouseclick)

# get things rolling
timer.start()
frame.start()

soundtrack.play()
