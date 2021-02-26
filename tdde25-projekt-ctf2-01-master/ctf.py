import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
import math

#----- Initialisation -----#

#-- Initialise the display
pygame.init()
pygame.display.set_mode()
pygame.display.set_caption('Capture The Flag - Tank Combat')
pygame.font.init()
#+pygame.mixer.init()

#-- Initialise the clock
clock = pygame.time.Clock()

#-- Initialise the physics engine
space = pymunk.Space()
space.gravity = (0.0,  0.0)

#-- Import from the ctf framework
import ai
import boxmodels
import images
import gameobjects
import maps

#-- Constants
FRAMERATE = 50
COOLDOWN = 0

#-- Variables
#   Define the current level
current_map         = maps.map0
#   List of all game objects
game_objects_list   = []
tanks_list          = []
ai_list             = []

screenwidth = 600
screenheight = 600

#-- Resize the screen to the size of the current level
screen = pygame.display.set_mode((screenwidth, screenheight))

#<INSERT GENERATE BACKGROUND>
#-- Generate the background
background = pygame.Surface(screen.get_size())
largetext = pygame.font.SysFont('Courier', 60)
mediumtext = pygame.font.SysFont('Courier', 30)
smalltext = pygame.font.SysFont('Courier', 15)
pointstext = pygame.font.SysFont('Courier', 40)
topicposition = (10, 50)
start_screen_bg = pygame.image.load("startscreenbackground.jpg")
score_screen_bg = pygame.image.load("scorescreenbackground.jpg")
button_bg = pygame.image.load("button.png")
orange_tank = images.tanks[0]
orange_tank = pygame.transform.scale(orange_tank, (90, 90))
orange_tank = pygame.transform.rotate(orange_tank, 180)
blue_tank = images.tanks[1]
blue_tank = pygame.transform.scale(blue_tank, (90, 90))
blue_tank = pygame.transform.rotate(blue_tank, 180)
terrain1 = pygame.image.load("terrain1.png")
terrain2 = pygame.image.load("terrain2.png")
terrain3 = pygame.image.load("terrain3.png")
terrain4 = pygame.image.load("terrain4.png")
terrain5 = pygame.image.load("terrain5.png")
terrain6 = pygame.image.load("terrain6.png")
resume = mediumtext.render('Press "Enter" to continue', False, (255, 255, 255))
press = mediumtext.render('Press number (1-6) to play', False, (255, 255, 255))
pygame.display.update()
#<THE START SCREEN>
start_screen = True
while start_screen:
    global multi
    screen.blit(start_screen_bg, (0,0))
    topic = largetext.render('CAPURE THE FLAG', False, (255, 255, 255))
    combat = mediumtext.render('Tank Combat', False, (255, 255, 255))
    playsingle = mediumtext.render('Press "S" to play Single-player', False, (255, 255, 255))
    playmulti = mediumtext.render('Press "M" to play Multi-player', False, (255, 255, 255))
    screen.blit(topic, topicposition)
    screen.blit(combat, (190, 130))
    screen.blit(playsingle, (10, 230))
    screen.blit(playmulti, (10, 290))
    clock.tick(FRAMERATE)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN and event.key == K_s:
            print("Play singleplayer")
            multi = False
            start_screen = False
        if event.type == pygame.KEYDOWN and event.key == K_m:
            print("Play multiplayer")
            multi = True
            start_screen = False
you_are = True
while you_are:
    screen.blit(score_screen_bg, (0,0))
    screen.blit(score_screen_bg, (0, 440))
    steer_up = smalltext.render('Up', False, (255, 255, 255))
    steer_down = smalltext.render('Down', False, (255, 255, 255))
    steer_left = smalltext.render('Left', False, (255, 255, 255))
    steer_right = smalltext.render('Right', False, (255, 255, 255))
    steer_w = smalltext.render('W', False, (255, 255, 255))
    steer_s = smalltext.render('S', False, (255, 255, 255))
    steer_a = smalltext.render('A', False, (255, 255, 255))
    steer_d = smalltext.render('D', False, (255, 255, 255))
    shoot_first = smalltext.render('Shoot with "Space"', False, (255, 255, 255))
    shoot_second = smalltext.render('Shoot with "1"', False, (255, 255, 255))
    if multi == True:
        topic = mediumtext.render('Control tanks:', False, (255, 255, 255))
        screen.blit(button_bg, (20, 275))
        screen.blit(button_bg, (230, 275))
        screen.blit(button_bg, (125, 170))
        screen.blit(button_bg, (125, 380))
        screen.blit(steer_up, (127, 180))
        screen.blit(steer_down, (127, 390))
        screen.blit(steer_left, (22, 285))
        screen.blit(steer_right, (232, 285))
        screen.blit(shoot_first, (75, 475))
        screen.blit(orange_tank, (105, 255))
        screen.blit(button_bg, (320, 275))
        screen.blit(button_bg, (530, 275))
        screen.blit(button_bg, (425, 170))
        screen.blit(button_bg, (425, 380))
        screen.blit(steer_w, (445, 180))
        screen.blit(steer_s, (445, 390))
        screen.blit(steer_a, (340, 285))
        screen.blit(steer_d, (550, 285))
        screen.blit(shoot_second, (375, 475))
        screen.blit(blue_tank, (405, 255))
    if multi == False:
        topic = mediumtext.render('Control tank:', False, (255, 255, 255))
        screen.blit(button_bg, (150, 275))
        screen.blit(button_bg, (400, 275))
        screen.blit(button_bg, (275, 150))
        screen.blit(button_bg, (275, 400))
        screen.blit(steer_up, (277, 160))
        screen.blit(steer_down, (277, 410))
        screen.blit(steer_left, (152, 285))
        screen.blit(steer_right, (402, 285))
        screen.blit(shoot_first, (225, 475))
        screen.blit(orange_tank, (255, 255))
    screen.blit(topic, topicposition)
    screen.blit(resume, (10, 550))
    clock.tick(FRAMERATE)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN and event.key == K_RETURN:
            you_are = False
select_terrain = True
while select_terrain:
    screen.blit(score_screen_bg, (0,0))
    screen.blit(score_screen_bg, (0, 440))
    topic = mediumtext.render('Select terrain:', False, (255, 255, 255))
    map1 = smalltext.render('Map 1', False, (255, 255, 255))
    map2 = smalltext.render('Map 2', False, (255, 255, 255))
    map3 = smalltext.render('Map 3', False, (255, 255, 255))
    map4 = smalltext.render('Map 4', False, (255, 255, 255))
    map5 = smalltext.render('Map 5', False, (255, 255, 255))
    map6 = smalltext.render('Map 6', False, (255, 255, 255))
    screen.blit(topic, topicposition)
    screen.blit(terrain1, (10, 100))
    screen.blit(terrain2, (169, 100))
    screen.blit(terrain3, (425, 100))
    screen.blit(terrain4, (30, 350))
    screen.blit(terrain5, (220, 350))
    screen.blit(terrain6, (420, 350))
    screen.blit(map1, (10, 255))
    screen.blit(map2, (169, 287))
    screen.blit(map3, (425, 191))
    screen.blit(map4, (30, 505))
    screen.blit(map5, (220, 441))
    screen.blit(map6, (420, 505))
    screen.blit(press, (10, 550))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN and event.key == K_1:
            current_map = maps.map0
            print("map 1")
            select_terrain = False
        if event.type == pygame.KEYDOWN and event.key == K_2:
            current_map = maps.map1
            print("map 2")
            select_terrain = False
        if event.type == pygame.KEYDOWN and event.key == K_3:
            current_map = maps.map2
            print("map 3")
            select_terrain = False
        if event.type == pygame.KEYDOWN and event.key == K_4:
            current_map = maps.map3
            print("map 4")
            select_terrain = False
        if event.type == pygame.KEYDOWN and event.key == K_5:
            current_map = maps.map4
            print("map 5")
            select_terrain = False
        if event.type == pygame.KEYDOWN and event.key == K_6:
            current_map = maps.map5
            print("map 6")
            select_terrain = False
        if not select_terrain:
            #-- Resize the screen to the size of the current level
            screen = pygame.display.set_mode(current_map.rect().size)
            scorescreen = pygame.display.set_mode((920, current_map.rect().size[1]))
        pygame.display.update()
    clock.tick(FRAMERATE)

background.blit(score_screen_bg, (0,0))
scorescreen.blit(score_screen_bg, (0,0))

#   Copy the grass tile all over the level area
for x in range(0, current_map.width):
    for y in range(0,  current_map.height):
        # The call to the function "blit" will copy the image
        # contained in "images.grass" into the "background"
        # image at the coordinates given as the second argument
        background.blit(images.grass,  (x*images.TILE_SIZE, y*images.TILE_SIZE))

def reset_gameboard(winning_tank = None):
    """
    Function that resets the gameboard when someone has won.
    """
    for tanks in range(len(tanks_list)):
        pos = current_map.start_positions[tanks]
        tanks_list[tanks].body.position = (pos[0], pos[1])
        tanks_list[tanks].body.angle = pos[2] * (180/math.pi)
    if winning_tank != None:
        winning_tank.drop_flag(flag)
        flag.x = current_map.flag_position[0]
        flag.y = current_map.flag_position[1]

        for i in range(100):
            for obj in game_objects_list:
                if isinstance(obj, gameobjects.Box):
                    game_objects_list.remove(obj)
                    space.remove(obj.shape)
        create_boxes()

def create_boxes():
    """
    Function that creats boxes in the map.
    """
    #<INSERT CREATE BOXES>
    for x in range(0, current_map.width):
        for y in range(0,  current_map.height):
            # Get the type of boxes
            box_type  = current_map.boxAt(x, y)
            box_model = boxmodels.get_model(box_type)
            # If the box model is non null, create a box
            if(box_model != None):
                # Create a "Box" using the model "box_model" at the
                # coordinate (x,y) (an offset of 0.5 is added since
                # the constructor of the Box object expects to know
                # the centre of the box, have a look at the coordinate
                # systems section for more explanations).
                box = gameobjects.Box(x + 0.5, y + 0.5, box_model, space)
                game_objects_list.append(box)

#gameobject => Box => boxmodel => destructable
create_boxes()


def collision_bullet_box(arb,space,data):
    """ This function tells ut what will happen when a bullet collides
        with a box"""
    now = pygame.time.get_ticks()
    box = arb.shapes[1].parent
    if box.boxmodel.destructable and box.hp >1:
        game_objects_list.remove(arb.shapes[0].parent)
        space.remove(arb.shapes[0], arb.shapes[0].body)
        box.hp -= 1
        return True
    elif box.hp == 1 and box.boxmodel.destructable:
        #+pygame.mixer.music.load('wood.wav')
        #+pygame.mixer.music.play(0)
        game_objects_list.remove(arb.shapes[1].parent)
        game_objects_list.remove(arb.shapes[0].parent)
        space.remove(arb.shapes[0], arb.shapes[0].body)
        space.remove(arb.shapes[1], arb.shapes[1].body)
        expl = gameobjects.Explosion(box.body.position[0], box.body.position[1], game_objects_list)
        game_objects_list.append(expl)
        return True
    else:
        game_objects_list.remove(arb.shapes[0].parent)
        space.remove(arb.shapes[0], arb.shapes[0].body)
        return True

handler2 = space.add_collision_handler(1,3)
handler2.pre_solve = collision_bullet_box


#<INSERT CREATE TANKS>
# Loop over the starting poistion
for i in range(0, len(current_map.start_positions)):
    # Get the starting position of the tank "i"
    pos = current_map.start_positions[i]
    # Create the tank, images.tanks contains the image representing the tank
    tank = gameobjects.Tank(pos[0], pos[1], pos[2], images.tanks[i], space)
    # Add the tank to the list of objects to display
    game_objects_list.append(tank)
    # Add the tank to the list of tanks
    tanks_list.append(tank)

    ai_tank  = ai.Ai(tanks_list[i], game_objects_list,  tanks_list, space , current_map)
    ai_list.append(ai_tank)


#<TANK RESPAWN WHEN HIT BY BULLET>
def collision_bullet_tank(arb, space, data):
    """This function tells us what will happen when a bullet and
        tank collides"""
    tank = arb.shapes[1].parent
    if tank.hp >= 1:
        tank.hp -= 1
    if tank.hp <= 0:
        #+pygame.mixer.music.load('tank.wav')
        #+pygame.mixer.music.play(0)
        expl = gameobjects.Explosion(tank.body.position[0], tank.body.position[1],game_objects_list)
        game_objects_list.append(expl)
        gameobjects.Tank.respawn(arb.shapes[1].parent)
        game_objects_list.remove(arb.shapes[0].parent)
        space.remove(arb.shapes[0], arb.shapes[0].body)
        return True
    else:
        game_objects_list.remove(arb.shapes[0].parent)
        space.remove(arb.shapes[0], arb.shapes[0].body)
        return True

handler1 = space.add_collision_handler(1,2)
handler1.pre_solve = collision_bullet_tank


def collision_bullet_bullet(arb, space, data):
    """This function tells us what will happen when a bullet and
        bullet collides"""
    game_objects_list.remove(arb.shapes[1].parent)
    game_objects_list.remove(arb.shapes[0].parent)
    space.remove(arb.shapes[0], arb.shapes[0].body)
    space.remove(arb.shapes[1], arb.shapes[1].body)
    return True

handler1 = space.add_collision_handler(1,1)
handler1.pre_solve = collision_bullet_bullet

#<INSERT CREATE FLAG>
flag = gameobjects.Flag(current_map.flag_position[0], current_map.flag_position[1])
game_objects_list.append(flag)


#<INSERT CREATE BASES>
for i in range(0, len(current_map.start_positions)):
    # Get the starting position of the tank "i"
    pos = current_map.start_positions[i]
    # Create the tank, images.tanks contains the image representing the tank
    base = gameobjects.GameVisibleObject(pos[0], pos[1], images.bases[i],)
    # Add the tank to the list of objects to display
    game_objects_list.append(base)


#<INSERT INVISIBLE WALLS>
static_body = space.static_body
static_lines = [pymunk.Segment(static_body, (0.0, 0.0), (0.0, current_map.height), 0.0)
,pymunk.Segment(static_body, (0.0, current_map.height), (current_map.width, current_map.height), 0.0)
,pymunk.Segment(static_body, (current_map.width, current_map.height), (current_map.width, 0.0), 0.0)
, pymunk.Segment(static_body, (current_map.width, 0.0), (0.0, 0.0), 0.0)
]

for line in static_lines:
    line.elasticity = 0.95
    line.friction = 0.9
space.add(static_lines)

# static_lines - a sensor that removes anything touching it
top = pymunk.Segment(static_body, (current_map.width, 0.0), (0.0, 0.0), 0.0)
left = pymunk.Segment(static_body, (0.0, 0.0), (0.0, current_map.height), 0.0)
bottom = pymunk.Segment(static_body, (0.0, current_map.height), (current_map.width, current_map.height), 0.0)
right = pymunk.Segment(static_body, (current_map.width, current_map.height), (current_map.width, 0.0), 0.0)

top.sensor = True
left.sensor = True
bottom.sensor = True
right.sensor = True

top.collision_type = 4
left.collision_type = 5
bottom.collision_type = 6
right.collision_type = 7


def collision_bullet_invisible_wall(arb, space, data):
    """This function tells us what will happen when a bullet
        collides with the invisible wall"""
    game_objects_list.remove(arb.shapes[0].parent)
    space.remove(arb.shapes[0], arb.shapes[0].body)
    return True

h = space.add_collision_handler(1,4)
h.begin = collision_bullet_invisible_wall
space.add(top)

h = space.add_collision_handler(1,5)
h.begin = collision_bullet_invisible_wall
space.add(left)

h = space.add_collision_handler(1,6)
h.begin = collision_bullet_invisible_wall
space.add(bottom)

h = space.add_collision_handler(1,7)
h.begin = collision_bullet_invisible_wall
space.add(right)


#----- Main Loop -----#

#-- Control whether the game run
running = True
skip_update = 0

while running:
    #-- Handle the events
    for event in pygame.event.get():
        # Check if we receive a QUIT event (for instance, if the user press the
        # close button of the wiendow) or if the user press the escape key.
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False

        #Control of the Tank
        if event.type == KEYDOWN and event.key == K_LEFT:
            gameobjects.Tank.turn_left(tanks_list[0])
        elif event.type == KEYUP and event.key == K_LEFT:
            gameobjects.Tank.stop_turning(tanks_list[0])

        elif event.type == KEYDOWN and event.key == K_UP:
            gameobjects.Tank.accelerate(tanks_list[0])
        elif event.type == KEYUP and event.key == K_UP:
            gameobjects.Tank.stop_moving(tanks_list[0])

        elif event.type == KEYDOWN and event.key == K_RIGHT:
            gameobjects.Tank.turn_right(tanks_list[0])
        elif event.type == KEYUP and event.key == K_RIGHT:
            gameobjects.Tank.stop_turning(tanks_list[0])

        elif event.type == KEYDOWN and event.key == K_DOWN:
            gameobjects.Tank.decelerate(tanks_list[0])
        elif event.type == KEYUP and event.key == K_DOWN:
            gameobjects.Tank.stop_moving(tanks_list[0])

        #Shooting with the Tank
        if event.type == KEYDOWN and event.key == K_SPACE:
            if COOLDOWN == 0:
                bullet = gameobjects.Tank.shoot(tanks_list[0], space)
                game_objects_list.append(bullet)
                COOLDOWN = FRAMERATE

        if multi == True:
            if event.type == KEYDOWN and event.key == K_a:
                gameobjects.Tank.turn_left(tanks_list[1])
            elif event.type == KEYUP and event.key == K_a:
                gameobjects.Tank.stop_turning(tanks_list[1])

            elif event.type == KEYDOWN and event.key == K_w:
                gameobjects.Tank.accelerate(tanks_list[1])
            elif event.type == KEYUP and event.key == K_w:
                gameobjects.Tank.stop_moving(tanks_list[1])

            elif event.type == KEYDOWN and event.key == K_d:
                gameobjects.Tank.turn_right(tanks_list[1])
            elif event.type == KEYUP and event.key == K_d:
                gameobjects.Tank.stop_turning(tanks_list[1])

            elif event.type == KEYDOWN and event.key == K_s:
                gameobjects.Tank.decelerate(tanks_list[1])
            elif event.type == KEYUP and event.key == K_s:
                gameobjects.Tank.stop_moving(tanks_list[1])

            elif event.type == KEYDOWN:
                if event.key == K_1:
                    if COOLDOWN == 0:
                        bullet = gameobjects.Tank.shoot(tanks_list[1], space)
                        game_objects_list.append(bullet)
                        COOLDOWN = FRAMERATE
    if multi == False:
        for i in range(1,len(ai_list)):
            ai.Ai.decide(ai_list[i])
    if multi == True:
        for i in range(2,len(ai_list)):
            ai.Ai.decide(ai_list[i])

    for tanks in tanks_list:
        gameobjects.Tank.try_grab_flag(tanks, flag)

    for tanks in range(len(tanks_list)):
        if tanks_list[tanks].has_won():
            #+pygame.mixer.music.load('victory.wav')
            #+pygame.mixer.music.play(0)
            tanks_list[tanks].score += 1
            for x in range(len(tanks_list)):
                print("Player", x+1, ":", tanks_list[x].score)
            reset_gameboard(tanks_list[tanks])
            scorescreen.blit(score_screen_bg, (0,0))
            pygame.display.flip()
        points = pointstext.render("Player " + str(tanks + 1) + ": " + str(tanks_list[tanks].score), False, (255, 255, 255))
        end = mediumtext.render('"Esc" to quit', False, (255, 255, 255))
        scorescreen.blit(points, (610, 10 + tanks * 65))
        scorescreen.blit(end, (610, 10 + len(tanks_list) * 65))
        pygame.display.update()



    #-- Update physics

    if skip_update == 0:
        # Loop over all the game objects and update their speed in function of their
        # acceleration.
        for obj in game_objects_list:
            obj.update()
        skip_update = 2
        if COOLDOWN > 0:
            COOLDOWN -= 1
    else:
        skip_update -= 1
        if COOLDOWN > 0:
            COOLDOWN -=1
#   Check collisions and update the objects position
    space.step(1/ FRAMERATE)



    #   Update object that depends on an other object position (for instance a flag)
    for obj in game_objects_list:
        obj.post_update()

    #-- Update Display
    #<INSERT DISPLAY BACKGROUND>
    # Display the background on the screen
    screen.blit(background, (0, 0))
    #<INSERT DISPLAY OBJECTS>
    # Update the display of the game objects on the screen
    for obj in game_objects_list:
        obj.update_screen(screen)
    #   Redisplay the entire screen (see double buffer technique)
    pygame.display.flip()

    #   Control the game framerate
    clock.tick(FRAMERATE)

pygame.quit()
