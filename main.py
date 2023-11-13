'''
  A functioning classic bullet hell game with multiple difficulties and modes.
'''

# Imports
import pygame, sys, random, math, time, numpy
from pygame.locals import QUIT

# Constants

# These are meant to be modified
BOX_EXPLODE_COUNTDOWN = 100
BOX_EXPLODE_ANGLES = (0, math.pi / 2, math.pi, 3 * math.pi / 2)
BOX_EXPLODE_VELOCITY = 2

# Drink event configuration
HIGH_DIFFICULTY_CD = 4
LOW_DIFFICULTY_CD = 10
DRINK_MAX_DIST = 100
DRINK_LIVES_GAINED = 1


# These aren't meant to be modified
RESOLUTION_X = 640
RESOLUTION_Y = 480
SCREEN_LOWER_BOUND_X = -20
SCREEN_LOWER_BOUND_Y = 0

UPPER_Y_BOUND = 380
LOWER_Y_BOUND = 15
UPPER_X_BOUND = 565
LOWER_X_BOUND = -12

COKE_OFFSET_X = 2
COKE_OFFSET_Y = 4
BOX_OFFSET_X = 20
BOX_OFFSET_Y = 20
PLAYER_OFFSET_X = 20
PLAYER_OFFSET_Y = 20

LENA_LEFT_SIDE_X = -5
LENA_RIGHT_SIDE_X = RESOLUTION_X - 30
LENA_TOP_SIDE_Y = 0
LENA_BOTTOM_SIDE_Y = RESOLUTION_Y - 45

JERONE_DIFFICULTY = 1
PEP_DIFFICULTY = 2
APCSP_DIFFICULTY = 3
APCSA_DIFFICULTY = 4
POSTAP_DIFFICULTY = 5

JERONE_START_LIVES = 3
PEP_START_LIVES = 3
APCSP_START_LIVES = 4
APCSA_START_LIVES = 5
POSTAP_START_LIVES = 10

START_PLAYER_X = 300
START_PLAYER_Y = 180
PLAYER_VEL = 2

# Pygame Boilerplate
pygame.init()
screen = pygame.display.set_mode((RESOLUTION_X, RESOLUTION_Y))
pygame.display.set_caption('Coke')
clock = pygame.time.Clock()

# Sprites
backdrop_surface = pygame.image.load('Graphics/otherbg.png')
background_surface = pygame.image.load('Graphics/bg.png')
start_surface = pygame.transform.scale(pygame.image.load('Graphics/start.png'),
                                       (160, 40))
ready_surface = pygame.transform.scale(pygame.image.load('Graphics/Ready.png'),
                                       (70, 70))
title_surface = pygame.transform.scale(pygame.image.load('Graphics/title.png'),
                                       (360, 80))
cooldown_surface = pygame.transform.scale(
  pygame.image.load('Graphics/Cooldown.png'), (70, 70))
life_surface = pygame.image.load('Graphics/heart.png')
lena_surface = pygame.image.load('Graphics/lena.png')
coke_surface = pygame.transform.scale(
  pygame.image.load('Graphics/Coke-Thrown.png'), (100, 100))
coke_box_surface = pygame.transform.scale(
  pygame.image.load('Graphics/Coke-Box.png'), (30, 30))
player_surface = pygame.image.load('Graphics/player.png')
PostAP_surface = pygame.image.load('Graphics/post-ap.png')
APCSA_surface = pygame.image.load('Graphics/apcsa.png')
APCSP_surface = pygame.image.load('Graphics/apcsp.png')
PEP_surface = pygame.image.load('Graphics/pep.png')
Jerone_surface = pygame.image.load('Graphics/jerone.png')
trophy_surface = pygame.transform.scale(
  pygame.image.load('Graphics/Coke_Trophy.png'), (400, 300))
play_again_surface = pygame.image.load('Graphics/play_again.png')
quit_surface = pygame.image.load('Graphics/quit.png')
skull_surface = pygame.transform.scale(pygame.image.load('Graphics/skull.png'),
                                       (400, 300))
clone_surface = pygame.image.load('Graphics/clone.png')
Font = pygame.font.Font('freesansbold.ttf', 32)


class Projectile:
  '''
    Represents a projectile moving on the screen.

    Attributes:
      Angle: float
        The angle at which the projectile is moving in radians.

      Velocity: int
        The velocity at which the projectile moves at.

      x: int
        The horizontal position of the projectile.

      y: int
        The vertical position of the projectile

      screen: pygame display
        The screen to display to.

      mode: string
        The mode of the projectile. Must be either 'reg' or 'box'.

      start_frame: int
        The frame that the projectile is constructed at.
  '''

  def __init__(self, _angle, _velocity, _x, _y, _screen, _mode):
    '''
      Constructs a projectile and appends it to the projectile_list.

      Parameters:
        Angle: float
          The angle at which the projectile is moving in radians.
  
        Velocity: int
          The velocity at which the projectile moves at.
  
        x: int
          The horizontal position of the projectile.
  
        y: int
          The vertical position of the projectile
  
        screen: pygame display
          The screen to display to.
  
        mode: string
          The mode of the projectile. Must be either 'reg' or 'box'.
    '''
    self.angle = _angle
    self.velocity = _velocity
    self.x = _x
    self.y = _y
    self.screen = _screen
    self.mode = _mode
    self.start_frame = frame_count
    projectile_list.append(self)

  def delete(self):
    '''
      Deletes the projectile and removes it from projectile_list.
    '''
    projectile_list.remove(self)
    del self

  def positionChecks(self, rect):
    '''
      Checks if the projectile is in bounds as well as if it is colliding with the player.

      Parameters:
        rect: pygame.Rect
          Stores the rectangular coordinates of the player, checks for collision.
    '''
    if (self.x < SCREEN_LOWER_BOUND_X or self.x > RESOLUTION_X or self.y < SCREEN_LOWER_BOUND_Y
        or self.y > RESOLUTION_Y):
      self.delete()
    if (rect.collidepoint((self.x, self.y))):
      self.delete()
      hit()


def tick(rect):
  '''
    Moves a projectile forward one frame.

    Parameters:
      rect: pygame.Rect
        Stores the rectangular coordinates of the player.
  '''
  for p in projectile_list:
    # Moves the projectile itself.
    p.x += p.velocity * math.cos(p.angle)
    p.y += p.velocity * math.sin(p.angle)

    # Renders a regular coke projectile.
    if (p.mode == 'reg'):
      p.screen.blit(coke_surface, (p.x + COKE_OFFSET_X, p.y + COKE_OFFSET_Y))
    # Renders a box projectile.
    elif (p.mode == 'box'):
      p.screen.blit(coke_box_surface, (p.x + BOX_OFFSET_X, p.y + BOX_OFFSET_Y))
      # If BOX_EXPLODE_COUNTDOWN frames pass, then the box will explode.
      if (frame_count - p.start_frame >= BOX_EXPLODE_COUNTDOWN):
        p.delete()
        for angle in BOX_EXPLODE_ANGLES:
          Projectile(angle, BOX_EXPLODE_VELOCITY, p.x + BOX_OFFSET_X, p.y + BOX_OFFSET_Y, p.screen, 'reg')
    p.positionChecks(rect)


def keyEvents(keys):
  '''
    Takes in key input and maps it to the player's movement and ability.
  '''
  global player_x, player_y

  # Move down
  if keys[pygame.K_s]:
    player_y += vel
    if (player_y > UPPER_Y_BOUND):
      player_y = UPPER_Y_BOUND

  # Move right
  if keys[pygame.K_d]:
    player_x += vel
    if (player_x > UPPER_X_BOUND):
      player_x = UPPER_X_BOUND

  # Move up
  if keys[pygame.K_w]:
    player_y -= vel
    if (player_y < LOWER_Y_BOUND):
      player_y = LOWER_Y_BOUND

  # Move left
  if keys[pygame.K_a]:
    player_x -= vel
    if (player_x < LOWER_X_BOUND):
      player_x = LOWER_X_BOUND

  # Ability
  if (keys[pygame.K_SPACE]):
    drinkEvent()
    
  # Update the player sprite
  screen.blit(player_surface, (player_x + PLAYER_OFFSET_X, player_y + PLAYER_OFFSET_Y))

def drinkEvent():
  '''
    Player ability, allows for the player to drink a can of diet coke to regain a life and destroy the can.
  '''
  global player_x, player_y, cooldown, lives, difficulty
  
  for proj in projectile_list:
      # Checks distance and cooldown
      if (math.sqrt((proj.x - player_x)**2 + (proj.y - player_y)**2) <= DRINK_MAX_DIST
          and cooldown <= 0):
        proj.delete()
        lives += DRINK_LIVES_GAINED
        if (difficulty == POSTAP_DIFFICULTY):
          cooldown = HIGH_DIFFICULTY_CD
        else:
          cooldown = LOW_DIFFICULTY_CD
        break


def lenaMove():
  '''
    Lena movement throughout the screen, randomly moves him to any of the four sides.
  '''
  global lena_x
  global lena_y
  if (random.randint(1, 2) == 1): # Selects between Lena going to the top/bottom side and the left/right side.
    if (random.randint(1, 2) == 1): # Selects between Lena going to the left or the right side.
      lena_x = LENA_LEFT_SIDE_X
    else:
      lena_x = LENA_RIGHT_SIDE_X
    lena_y = random.randint(LENA_TOP_SIDE_Y, LENA_BOTTOM_SIDE_Y)
  else:
    if (random.randint(1, 2) == 1): # Selects between Lena going to the top or the bottom side.
      lena_y = LENA_TOP_SIDE_Y
    else:
      lena_y = LENA_BOTTOM_SIDE_Y
    lena_x = random.randint(LENA_LEFT_SIDE_X, LENA_RIGHT_SIDE_X)

def getAngle():
  '''
    Gets the angle between Lena and the player.
  '''
  try:
    angle = math.atan((lena_y - player_y) / (lena_x - player_x))
  except:
    # Accounts for divide by zero errors if lena_x and player_x are equal
    angle = math.atan((lena_y - player_y) / (lena_x - player_x + 0.01))
  angle += 0 if (lena_x < player_x) else math.pi
  return angle

def jeroneDifficultyProjTick(angle):
  '''
    Creates projectiles every tick for jerone difficulty
  '''
  global move_cd, lena_x, lena_y
  
  velocity = random.randint(3, 5)
  move_cd = 90
  
  if (time >= 45):
    win()
  elif (time >= 20):
    Projectile(angle, velocity / 3, lena_x, lena_y, screen, 'box')
  else:
    Projectile(angle, velocity, lena_x, lena_y, screen, 'reg')
    
def PEPDifficultyProjTick(angle):
  '''
    Creates projectiles every tick for PEP difficulty
  '''
  global move_cd, lena_x, lena_y
  
  velocity = random.randint(3, 5)
  move_cd = 60
  rand = random.random()
  
  if (time >= 45):
    win()
    
  elif (time >= 20):
    if (rand < 0.5):
      Projectile(angle, velocity / 2, lena_x, lena_y, screen, 'box')
      
    else:
      Projectile(angle, velocity, lena_x, lena_y, screen, 'reg')
      
  else:
    if (rand < 0.5):
      for a in [angle - 0.2, angle + 0.2]:
        Projectile(a, velocity, lena_x, lena_y, screen, 'reg')
        
    else:
      Projectile(angle, velocity, lena_x, lena_y, screen, 'reg')
      
def APCSPDifficultyProjTick(angle):
  '''
    Creates projectiles every tick for APCSP difficulty
  '''
  global move_cd, lena_x, lena_y
  
  velocity = random.randint(5, 7)
  move_cd = 60
  rand = random.random()

  if (time >= 60):
    win()

  elif (time >= 40):
    if (rand < 0.5):
      
      for a in [angle - 0.5, angle - 0.25, angle, angle + 0.25, angle + 0.5]:
        Projectile(a, velocity / 5, lena_x, lena_y, screen, 'reg')
    elif (rand < 0.8):
      
      Projectile(angle + 0.5, velocity / 3, lena_x, lena_y, screen, 'box')
      Projectile(angle - 0.5, velocity / 3, lena_x, lena_y, screen, 'box')
    else:
      
      for i in range(1, 5):
        Projectile(angle - (random.random() - 0.5) * 0.5,
                   velocity / 3 + (random.random() - 0.5), lena_x, lena_y,
                   screen, 'reg')

  elif (time >= 20):
    if (rand < 0.5):
      for a in [angle - 0.3, angle, angle + 0.3]:
        Projectile(a, velocity / 4, lena_x, lena_y, screen, 'reg')
        
    if (rand < 0.8):
      Projectile(angle, velocity / 5, lena_x, lena_y, screen, 'box')

  else:
    for a in [angle - 0.2, angle, angle + 0.2]:
      Projectile(a, velocity / 3, lena_x, lena_y, screen, 'reg')
      
def APCSADifficultyProjTick(angle):
  '''
    Creates projectiles every tick for APCSA difficulty
  '''
  global move_cd, lena_x, lena_y, lena_move
  
  velocity = random.randint(5, 7)
  move_cd = 60
  rand = random.random()
  
  if (time >= 60):
    win()
    
  elif (time >= 45):
    lena_move = True
    if (rand < 0.2):
      for a in [1, 0.8, 0.6, 0.4, 0.2, 0, -0.2, -0.4, -0.6, -0.8, -1]:
        Projectile(angle + a, velocity / 6, lena_x, lena_y, screen, 'reg')
        
    elif (rand < 0.75):
      for a in [angle - 0.3, angle + 0.3]:
        Projectile(a, velocity / 5, lena_x, lena_y, screen, 'reg')
      Projectile(angle, velocity / 4, lena_x, lena_y, screen, 'box')
      
    else:
      for a in [0.5, 0.25, -0.25, 0.5]:
        Projectile(angle - a, velocity / 8, lena_x, lena_y, screen, 'box')
        
  elif (time >= 40):
    lena_move = False
    # Special attack here
    
  elif (time >= 25):
    lena_move = True
    
    if (rand < 0.5):
      for a in [angle - 0.3, angle + 0.3]:
        Projectile(a, velocity / 5, lena_x, lena_y, screen, 'reg')
      Projectile(angle, velocity / 3, lena_x, lena_y, screen, 'box')
      
    else:
      for i in range(1, 5):
        Projectile(angle - (random.random() - 0.5),
                   velocity / 3 + (random.random() - 0.5), lena_x, lena_y,
                   screen, 'reg')
        
  elif (time >= 20):
    lena_move = False
    # Special attack here
  else:
    for a in [angle - 0.3, angle + 0.3]:
      Projectile(a, velocity / 5, lena_x, lena_y, screen, 'reg')
    Projectile(angle, velocity / 3, lena_x, lena_y, screen, 'box')
    
def PostAPDifficultyProjTick(angle):
  '''
    Creates projectiles every tick for Post-AP difficulty
  '''
  global move_cd, lena_x, lena_y, lena_move
  
  move_cd = 45
  velocity = random.randint(5, 7)
  rand = random.random()
  
  if (time > 75):
    win()
    
  elif (time > 60):
    if (rand < 0.2):
      for a in numpy.linspace(-1, 1, 20):
        Projectile(angle + a, velocity / 6, lena_x, lena_y, screen, 'reg')
        
    elif (rand < 0.75):
      for a in numpy.linspace(-1, 1, 5):
        Projectile(a, velocity / 5, lena_x, lena_y, screen, 'reg')
        
      for a in [-0.5, 0.5]:
        Projectile(angle + a, velocity / 4, lena_x, lena_y, screen, 'box')
        
    else:
      for a in [0.5, 0.25, -0.25, 0.5]:
        Projectile(angle - a, velocity / 5, lena_x, lena_y, screen, 'box')
        
  elif (time > 45):
    if (rand < 0.2):
      for a in [1, 0.8, 0.6, 0.4, 0.2, 0, -0.2, -0.4, -0.6, -0.8, -1]:
        Projectile(angle + a, velocity / 6, lena_x, lena_y, screen, 'reg')
        
    elif (rand < 0.75):
      for a in [angle - 0.3, angle + 0.3]:
        Projectile(a, velocity / 5, lena_x, lena_y, screen, 'reg')
      Projectile(angle, velocity / 4, lena_x, lena_y, screen, 'box')
      
    else:
      for a in [0.5, 0.25, -0.25, 0.5]:
        Projectile(angle - a, velocity / 8, lena_x, lena_y, screen, 'box')
        
  elif (time > 30):
    if (rand < 0.5):
      for a in [angle - 0.6, angle - 0.3, angle, angle + 0.3, angle + 0.6]:
        Projectile(a, velocity / 6, lena_x, lena_y, screen, 'reg')
        
    else:
      for a in [0.4, -0.4]:
        Projectile(angle + a, velocity / 3, lena_x, lena_y, screen, 'box')
        
  elif (time > 15):
    for a in [angle - 0.3, angle, angle + 0.3]:
      Projectile(a, velocity / 5, lena_x, lena_y, screen, 'reg')
      
  else:
    Projectile(angle, velocity / 4, lena_x, lena_y, screen, 'reg')

def projThrow():
  '''
    Throws projectiles every tick based on difficulty.
  '''
  angle = getAngle()

  if (difficulty == JERONE_DIFFICULTY):
    jeroneDifficultyProjTick(angle)
    
  elif (difficulty == PEP_DIFFICULTY):
    PEPDifficultyProjTick(angle)

  elif (difficulty == APCSP_DIFFICULTY):
    APCSPDifficultyProjTick(angle)

  elif (difficulty == APCSA_DIFFICULTY):
    APCSADifficultyProjTick(angle)

  elif (difficulty == POSTAP_DIFFICULTY):
    PostAPDifficultyProjTick(angle)


def hit():
  '''
    Runs if the player is hit, checks lose conditions and reduces lives
    by one.
  '''
  global lives, run, win
  lives -= 1
  if (lives <= 0):
    run = False
    win = False


def quit():
  '''
    Quits the game.
  '''
  pygame.quit()
  sys.exit()

def win():
  '''
    Runs if the player survives.
  '''
  global run, win
  win, run = True, False


def UIRender():
  '''
    Renders the lives remaining and the cooldown sprite.
  '''
  for i in range(1, lives + 1):
    screen.blit(life_surface, (i * 40, 5))
  if (cooldown <= 0):
    screen.blit(ready_surface, (570, 0))
  else:
    screen.blit(cooldown_surface, (570, 0))


def startup():
  '''
    Runs on game startup. Renders the game menu and detects input. Selects
    the difficulty based on player input.
  '''
  global difficulty, lives
  init()
  
  while (not difficulty):
    screen.blit(backdrop_surface, (0, 0))
    screen.blit(title_surface, (150, 80))
    screen.blit(PostAP_surface, (100, 200))
    screen.blit(APCSA_surface, (440, 200))
    screen.blit(APCSP_surface, (100, 300))
    screen.blit(PEP_surface, (440, 300))
    screen.blit(Jerone_surface, (270, 250))
    
    ev = pygame.event.get()
    for event in ev:
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
        
      if (event.type == pygame.MOUSEBUTTONUP):
        if (pygame.Rect(270, 250, 120,
                        40).collidepoint(pygame.mouse.get_pos())):
          difficulty = JERONE_DIFFICULTY
          lives = JERONE_START_LIVES
                          
        if (pygame.Rect(440, 300, 120,
                        40).collidepoint(pygame.mouse.get_pos())):
          difficulty = PEP_DIFFICULTY
          lives = PEP_START_LIVES
                          
        if (pygame.Rect(100, 300, 120,
                        40).collidepoint(pygame.mouse.get_pos())):
          difficulty = APCSP_DIFFICULTY
          lives = APCSP_START_LIVES
                          
        if (pygame.Rect(440, 200, 120,
                        40).collidepoint(pygame.mouse.get_pos())):
          difficulty = APCSA_DIFFICULTY
          lives = APCSA_START_LIVES
                          
        if (pygame.Rect(100, 200, 120,
                        40).collidepoint(pygame.mouse.get_pos())):
          difficulty = POSTAP_DIFFICULTY
          lives = POSTAP_START_LIVES
    # Updates the display every frame.
    pygame.display.update()
    clock.tick(60)


def end():
  '''
    Runs on game end, whether win or loss. Allows for the player to replay the game if they select to. Depicts win or loss.
  '''
  global run
  run = False
  
  while (not run):
    screen.blit(backdrop_surface, (0, 0))
    screen.blit(play_again_surface, (100, 340))
    screen.blit(quit_surface, (420, 340))
    
    if (win):
      screen.blit(trophy_surface, (140, 40))
      
    else:
      screen.blit(skull_surface, (120, 30))
      
    for event in pygame.event.get():
      if (event.type == pygame.MOUSEBUTTONUP):
        if (pygame.Rect(100, 340, 120,
                        40).collidepoint(pygame.mouse.get_pos())):
          main()
                          
        if (pygame.Rect(420, 340, 120,
                        40).collidepoint(pygame.mouse.get_pos())):
          quit()
                          
    pygame.display.update()
    clock.tick(60)


def init():
  '''
    Initializes all global variables at the start of the game.
  '''
  global lena_x, lena_y, player_x, player_y, lives, vel, frame_count, projectile_list, move_cd, difficulty, run, win, cooldown, lena_move, temp_frames, time, time_surface
  lena_x = 300
  lena_y = 0
  player_x = START_PLAYER_X
  player_y = START_PLAYER_Y
  lives = 6
  vel = PLAYER_VEL
  frame_count = 0
  projectile_list = []
  move_cd = 60
  difficulty = 0
  run = True
  win = False
  cooldown = 0
  lena_move = True
  temp_frames = 0
  time = 0
  time_surface = Font.render('Time:'+str(time), True, (255, 255, 255))

def specialAttacks():
  '''
    Runs during a special attack, changes based on the difficulty.
  '''
  global lena_x, lena_y, temp_frames, time
  rand = (random.random() - 0.5)
  
  if (not lena_move):
    lena_x, lena_y = 300, 0
    temp_frames = frame_count
    
  if (difficulty == APCSA_DIFFICULTY and (time > 20 and time < 25)
      or (time > 40 and time < 45)):
    if (frame_count % 60 == 0):
      for a in numpy.linspace(-0.1, math.pi + 0.1, 22):
        Projectile(a + rand, 1.5, lena_x, lena_y, screen, 'reg')
        
  if (difficulty == POSTAP_DIFFICULTY):
    screen.blit(clone_surface, (300, 0))
    
    if (time < 15):
      if (frame_count % 120 == 0):
        for a in numpy.linspace(-0.1, math.pi + 0.1, 10):
          Projectile(a + rand, 1.5, 300, 0, screen, 'reg')
          
    elif (time < 30):
      if (frame_count % 60 == 0):
        for a in numpy.linspace(-0.1, math.pi + 0.1, 10):
          Projectile(a + rand, 1.5, 300, 0, screen, 'reg')
          
    elif (time < 45):
      if (frame_count % 60 == 0):
        for a in numpy.linspace(-0.1, math.pi + 0.1, 10):
          Projectile(a + rand, 1.5, 300, 0, screen, 'reg')
          
    elif (time < 60):
      if (frame_count % 45 == 0):
        for a in numpy.linspace(-0.1, math.pi + 0.1, 10):
          Projectile(a + rand, 1.5, 300, 0, screen, 'reg')
          
    else:
      if (frame_count % 20 == 0):
        for a in numpy.linspace(-0.1, math.pi + 0.1, 20):
          Projectile(a, 2, 300, 0, screen, 'reg')


def main():
  '''
    Main function, includes main loop, rendering of the backdrop, quit detection, key events, and projectile ticks.
  '''
  global frame_count, run, cooldown, time, temp_frames, time_surface
  
  run = True
  startup()
  
  while run:
    # Increments frame count every iteration.
    frame_count += 1
    # Renders the time at every iteration where it changes.
    if (frame_count % 60 == 0):
      time = frame_count // 60
      time_surface = Font.render('Time:' + str(time), True, (255, 255, 255))
      
    # Backdrop rendering
    screen.blit(backdrop_surface, (0, 0))
    screen.blit(background_surface, (20, 40))
    screen.blit(time_surface, (0, 440))

    # Quit event detection
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
        
    # Key events
    keys = pygame.key.get_pressed()
    keyEvents(keys)

    # Cooldown decrementation
    if (cooldown > 0):
      cooldown -= 1 / 60

    # Lena movement and projectile generation
    if (frame_count % move_cd == 0):
      if (lena_move): lenaMove()
      projThrow()
      
    # Special attacks
    specialAttacks()
    
    # Rendering lena and the UI
    screen.blit(lena_surface, (lena_x, lena_y))
    UIRender()
    
    # Displaying to screen
    tick(pygame.Rect(player_x - 10, player_y - 20, 20, 40))
    pygame.display.update()
    clock.tick(60)
  end()


main()
