def gui(car_pos, movements, test_grid):
    import pygame
    import time
    import pygame.gfxdraw
    from pygame import mixer
    # define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GRAY = (128, 128, 128)
    RED = (238,64,0)
    
    # define constants for the garage and car dimensions
    CELL_SIZE     = 100
    GARAGE_HEIGHT  = len(test_grid) * CELL_SIZE
    GARAGE_WIDTH = len(test_grid[0]) * CELL_SIZE
    CAR_WIDTH     = 80
    CAR_HEIGHT    = 80
    col =len(test_grid)
    rows = len(test_grid[0])
    
    #Load used clip arts
    wall_img = pygame.image.load('assets/images/wall.png')
    obstacle_img = pygame.image.load('assets/images/obstacle.png')
    occupied_slot_img = pygame.image.load('assets/images/occupied_slot.png')
    car_img = pygame.image.load('assets/images/car.png')
    
    # initialize pygame
    pygame.init()
    
    #initialize text font
    text_font  = pygame.font.SysFont('Impact', 50)
    alert = pygame.font.SysFont('Impact', 25)
    # set up the display
    screen = pygame.display.set_mode((GARAGE_WIDTH, GARAGE_HEIGHT))
    pygame.display.set_caption("Car Parking System")

    # set up the clock
    clock = pygame.time.Clock()
    
    class Garage:
        def __init__(self, grid):
            self.grid = grid
            self.cell_size = CELL_SIZE
            self.width = GARAGE_WIDTH
            self.height = GARAGE_HEIGHT

        def draw(self):
            for i in range(len(self.grid)):
                for j in range(len(self.grid[0])):
                    x = j * self.cell_size
                    y = i * self.cell_size
                    if self.grid[i][j] == 1:  # starting pos for the car
                        pygame.draw.rect(screen, BLUE, (x, y, self.cell_size, self.cell_size))
                    elif self.grid[i][j] == 2:  # wall
                        screen.blit(pygame.transform.scale(wall_img, (self.cell_size, self.cell_size)), (x, y))
                    elif self.grid[i][j] == 3:  # obstacle
                        screen.blit(pygame.transform.scale(obstacle_img, (self.cell_size, self.cell_size)), (x, y))
                    elif self.grid[i][j] == 4:  # occupied slot
                        pygame.draw.rect(screen, GRAY, (x, y, self.cell_size, self.cell_size))
                        screen.blit(pygame.transform.scale(occupied_slot_img, (self.cell_size, self.cell_size)), (x, y))
                    elif self.grid[i][j] == 5:  # free slot
                        pygame.draw.rect(screen, GREEN, (x, y, self.cell_size, self.cell_size))
                    else:  # free path to walk through
                        pygame.draw.rect(screen, WHITE, (x, y, self.cell_size, self.cell_size))
                    # draw grid lines
                    pygame.draw.rect(screen, GRAY, (x, y, self.cell_size, self.cell_size), 1)


    class Car:
        def __init__(self, x, y, width, height, init_x, init_y):
            
            self.rect   =   pygame.Rect(x, y, width, height)
            self.image  =   pygame.transform.scale(car_img, (width, height))
            self.cell_x =   init_x
            self.cell_y =   init_y

        def draw(self):
            screen.blit(self.image, self.rect)

        def move(self, x, y):
            #check_border
            if (self.cell_x + x < 0) or (self.cell_x + x >= rows):
                x = 0
            if (self.cell_y + y < 0) or (self.cell_y + y >= col):
                y = 0
                
            self.rect.move_ip(x, y)
            self.cell_x +=   x
            self.cell_y +=   y
            self.rect.x =   (self.cell_x * garage.cell_size) 
            self.rect.y =   self.cell_y * garage.cell_size 
            
        #avoid passing in walls/obstcales/borders and parked cars
        def collide_with_wall(self, wall_rects):
            for wall_rect in wall_rects:
                if self.rect.colliderect(wall_rect):
                    return True
            return False
        
        def collide_with_parked(self, parked_rects):
            for parked_rects in parked_rects:
                if self.rect.colliderect(parked_rects):
                    return True
            return False
        
        def collide_with_obstacle(self, obstacle_rects):
            for obstacle_rect in obstacle_rects:
                if self.rect.colliderect(obstacle_rect):
                    return True
            return False
        
        def collide_with_border(self, border_rects):
            for border_rects in border_rects:
                if self.rect.colliderect(border_rects):
                    return True
                
        def parking(self, free_slots):
            for free_slots in free_slots:
                if self.rect.collidedict(free_slots):
                    return True
                return False
            
    #Function to parking alert
    def display_message(message):
        
        if message == "Parked !": #When the car trying to park in valid slot
            text = text_font.render(message, True, GREEN) #text render

            border = text_font.render(message, True, (0, 0, 0))
            border_rect = border.get_rect(center=text.get_rect(center=(GARAGE_WIDTH/2, GARAGE_HEIGHT/2)).center) #center the message
            border_rect.x += 2
            border_rect.y += 2
        
            screen.blit(border, border_rect)
            screen.blit(text, text.get_rect(center=(GARAGE_WIDTH/2, GARAGE_HEIGHT/2)))
            pygame.display.update()
        elif message == "You can't park here !": #When the car trying to park in invalid slot
            text = text_font.render(message, True, RED)
            border = text_font.render(message, True, (0, 0, 0))
            border_rect = border.get_rect(center=text.get_rect(center=(GARAGE_WIDTH/2, GARAGE_HEIGHT/2)).center)
            border_rect.x += 2
            border_rect.y += 2
        
            screen.blit(border, border_rect)
            screen.blit(text, text.get_rect(center=(GARAGE_WIDTH/2, GARAGE_HEIGHT/2)))
            pygame.display.update()
        else:
            text = alert.render(message, True, RED)
            border = alert.render(message, True, (0, 0, 0))
            border_rect = border.get_rect(center=text.get_rect(center=(GARAGE_WIDTH/2, GARAGE_HEIGHT/2)).center)
            border_rect.x += 2
            border_rect.y += 2
        
            screen.blit(border, border_rect)
            screen.blit(text, text.get_rect(center=(GARAGE_WIDTH/2, GARAGE_HEIGHT/2)))
            pygame.display.update()
            
        
    garage_grid = test_grid #define the garage 2d grid
    
    #Construct the garage and car
    garage = Garage(garage_grid)
    car = Car(car_pos[1] * CELL_SIZE, car_pos[0] * CELL_SIZE, CAR_WIDTH, CAR_HEIGHT, car_pos[1], car_pos[0])
    
    #intialize lists to memo special cells i,j
    wall_rects = []
    obstacle_rects = []
    parked_rects = []
    border_rects = []
    free_slots = []
    
    # find wall and obstacle rectangles
    for i in range(len(garage_grid)):
        for j in range(len(garage_grid[0])):
            if garage_grid[i][j] == 2:  # wall
                wall_rects.append(pygame.Rect(j * garage.cell_size, i * garage.cell_size, garage.cell_size, garage.cell_size))
            elif garage_grid[i][j] == 3:  # obstacle
                obstacle_rects.append(pygame.Rect(j * garage.cell_size, i * garage.cell_size, garage.cell_size, garage.cell_size))
            elif garage_grid[i][j] == 4:  # parked_car
                parked_rects.append(pygame.Rect(j * garage.cell_size, i * garage.cell_size, garage.cell_size, garage.cell_size))
            elif (i > col) or (j > rows):  # border
                border_rects.append(pygame.Rect(j * garage.cell_size, i * garage.cell_size, garage.cell_size, garage.cell_size))
            elif(garage_grid[i][j] == 5): #Free slot
                free_slots.append((j,i))

    # game loop
    indx = 0
    
    
    while indx<len(movements):
        # handle eventsmovements'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # move the car based on movements list
        time.sleep(0.5)
         #sleep to simulate car movements
        if movements[indx] == 'right':
            car.move(1, 0)
            if car.collide_with_wall(wall_rects) or car.collide_with_obstacle(obstacle_rects) or car.collide_with_parked(parked_rects) or car.collide_with_border(border_rects): #check non valid cells
                car.move(-1, 0)
                sound2 = mixer.Sound('assets/sounds/no_move.wav')
                sound2.play()
            else:
                sound1 = mixer.Sound('assets/sounds/move.wav')
                sound1.play()
                
        elif movements[indx] == 'left':
            car.move(-1, 0)
            if car.collide_with_wall(wall_rects) or car.collide_with_obstacle(obstacle_rects) or car.collide_with_parked(parked_rects) or car.collide_with_border(border_rects):
                car.move(1, 0)
                sound2 = mixer.Sound('assets/sounds/no_move.wav')
                sound2.play()
            else:
                sound1 = mixer.Sound('assets/sounds/move.wav')
                sound1.play()
        
        elif movements[indx] == 'down':
            car.move(0, 1)
            if car.collide_with_wall(wall_rects) or car.collide_with_obstacle(obstacle_rects) or car.collide_with_parked(parked_rects) or car.collide_with_border(border_rects):
                car.move(0, -1)
                sound2 = mixer.Sound('assets/sounds/no_move.wav')
                sound2.play()  
            else:
                sound1 = mixer.Sound('assets/sounds/move.wav')
                sound1.play()
            
        elif movements[indx] == 'up':
            car.move(0, -1)
            if car.collide_with_wall(wall_rects) or car.collide_with_obstacle(obstacle_rects) or car.collide_with_parked(parked_rects) or car.collide_with_border(border_rects):
                car.move(0, 1)
                sound2 = mixer.Sound('assets/sounds/no_move.wav')
                sound2.play()
            else:
                sound1 = mixer.Sound('assets/sounds/move.wav')
                sound1.play()
                
        elif movements[indx] == 'park':
            if (car.cell_x, car.cell_y) in free_slots:
                sound1 = mixer.Sound('assets/sounds/parked.wav')
                sound1.play()
                t_end = time.time() + 1
                while time.time() < t_end:
                    display_message("Parked !")
            else:
                sound1 = mixer.Sound('assets/sounds/no park.wav')
                sound1.play()
                t_end = time.time() + 1
                while time.time() < t_end:
                    display_message("You can't park here !")
        indx +=1
            
        #Construct the game window
        # draw the garage and car
        screen.fill(WHITE)
        garage.draw()
        car.draw()

        # update the display
        pygame.display.flip()

        # tick the clock
        clock.tick(10)
        if movements[0] == 'None':
            car.move(0, 0)
            pygame.time.wait(500)
            t_end = time.time() + 3
            sound = mixer.Sound('assets/sounds/no park.wav')
            sound.play()
            while time.time() < t_end:
                display_message('There is no path to simulate')