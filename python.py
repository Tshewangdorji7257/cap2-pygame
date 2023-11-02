import pygame
from pygame.locals import *
import random
import sys

# Initialize Pygame
pygame.init()

# Create the window
width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Retro Highway')

# Define colors
gray = (100, 100, 100)
green = (76, 208, 56)
red = (255, 255, 255)
yellow = (255, 232, 0)

# Game settings
gameover = False
speed = 2
score = 0

# Marker size
marker_width = 10
marker_height = 50

# Road and edge markers
road = (100, 0, 300, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

# x coordinates of lanes
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# For animating movement of the lane markers
lane_mark_move_y = 0


# Define the Vehicle class
class Vehicle(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Scale the image down so it fits in the lane
        image_scale = 85 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (int(new_width), int(new_height)))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

# Define the PlayerVehicle class, which is a subclass of Vehicle
class PlayerVehicle(Vehicle):

    def __init__(self, x, y):
        # Load the player's vehicle image
        image = pygame.image.load("C:\\Users\\Damchey\\OneDrive\\Desktop\\pygame\\red.png")
        super().__init__(image, x, y)


# Player's starting coordinates
player_x = 250
player_y = 400

# Create the player's car
player_group = pygame.sprite.Group()
player = PlayerVehicle(player_x, player_y)      
player_group.add(player) 

# Load the other vehicle images
image_filenames = ["C:\\Users\\Damchey\\OneDrive\\Desktop\pygame\\police car.png","C:\\Users\\Damchey\\OneDrive\\Desktop\\pygame\\red.png"]
vehicle_images = []
for filename in image_filenames:
    # Load each vehicle image
    image = pygame.image.load(filename)
    vehicle_images.append(image)

# Create a sprite group for vehicles
vehicle_group = pygame.sprite.Group()

#load the crash image
crash = pygame.image.load("C:\\Users\\Damchey\\OneDrive\\Desktop\\pygame\\crash.png")
crash_rect = crash.get_rect()


# Define the display_menu function
def display_menu():
    menu_font = pygame.font.Font(pygame.font.get_default_font(), 36)

    while True:
        screen.fill(green)

        title_text = menu_font.render('Retro Highway', True, red)
        title_rect = title_text.get_rect(center=(width//2, height//4))
        screen.blit(title_text, title_rect)

        start_text = menu_font.render('Press Enter to Start', True, yellow)
        start_rect = start_text.get_rect(center=(width//2, height//2))
        screen.blit(start_text, start_rect)

        quit_text = menu_font.render('Press Q to Quit', True, yellow)
        quit_rect = quit_text.get_rect(center=(width//2, height//1.5))
        screen.blit(quit_text, quit_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return
                elif event.key == K_q:
                    pygame.quit()
                    sys.exit()

# Call the display_menu function before the game loop
display_menu()

# Game loop
clock = pygame.time.Clock()
fps = 120
running = True
while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # move the player's car using the left/right arrows keys
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100   

   # check if there's a side awipe collision after changing lanes
        for vehicle in vehicle_group:
            if pygame.sprite.collide_rect(player, vehicle):

                gameover = True

                # place the player's car next to other vehicle
                # and determine where to position the crash image
                if event.key == K_LEFT:
                    player.rect.left = vehicle.rect.right
                    crash_rect.center =[player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                elif event.key == K_RIGHT:
                    player.rect.left = vehicle.rect.left
                    crash_rect.center =[player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]




    # Draw the grass
    screen.fill(green)

    # Draw the road
    pygame.draw.rect(screen, gray, road)

    # Draw the edge markers
    pygame.draw.rect(screen, 00, left_edge_marker)
    pygame.draw.rect(screen, 00, right_edge_marker)

    # Draw the lane marker
    lane_mark_move_y += speed * 2
    if lane_mark_move_y >= marker_height * 2:
        lane_mark_move_y = 0

    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, red, (left_lane + 45, y + lane_mark_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, red, (center_lane + 45, y + lane_mark_move_y, marker_width, marker_height))

    # Draw the player's car
    player_group.draw(screen)

    # Add the player's car
    if len(vehicle_group) < 2:
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False

        if add_vehicle:
            lane = random.choice(lanes)
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, height / -2)
            vehicle_group.add(vehicle)

    # Move the vehicles
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        if vehicle.rect.top >= height:
            vehicle.kill()
            score += 1
            if score > 0 and score % 10 == 0:
                speed += 0.5

    # Draw the vehicles
    vehicle_group.draw(screen)
    
    # displatb the score
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Score: ' + str(score), True, 00)
    text_rect = text.get_rect()
    text_rect.center = (50, 200)
    screen.blit(text, text_rect)

   # Check if there's a head-on collision
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]

    # Display game over 
    if gameover:
        screen.blit(crash, crash_rect)

        pygame.draw.rect(screen, red, (0, 50, width, 100))

        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Game over, Play again? (Enter Y or N)', True, 00 )
        text_rect = text.get_rect()
        text_rect.center = (width / 2, 100)
        screen.blit(text, text_rect)


    # Update the display
    pygame.display.update()

    #check if player wants to play again
    while gameover:

        clock.tick(fps)

        for event in pygame.event.get():

            if event.type == QUIT:
                gameover = False
                running = False

             # get the player's input (y or n)
            if event.type == KEYDOWN:
                if event.key == K_y:
                    # reset the game
                    gameover = False
                    speed = 2
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    # exit the loops
                    gameover = False
                    running = False      

# Quit Pygame
pygame.quit()