import pygame, os, math
from pygame.locals import *
pygame.init()

class Vector():
    '''
        Class:
            creates operations to handle vectors such
            as direction, position, and speed
        '''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self): # used for printing vectors
        return "(%s, %s)"%(self.x, self.y)

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("This "+str(key)+" key is not a vector key!")

    def __sub__(self, o): # subtraction
        return Vector(self.x - o.x, self.y - o.y)

    def length(self): # get length (used for normalize)
        return math.sqrt((self.x**2 + self.y**2)) 

    def normalize(self): # divides a vector by its length
        l = self.length()
        if l != 0:
            return (self.x / l, self.y / l)
        return None

class Sprite(pygame.sprite.Sprite):
    
    def __init__(self, unitType):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('sprites', unitType.unitImage1))
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255,255,255))
        self.unitType = unitType

        self.trueX = 100 # created because self.rect.center does not hold
        self.trueY = 100 # decimal values but these do
        self.rect.center = (self.trueX, self.trueY) # set starting position
        self.speed = unitType.unitSpeed # movement speed of the sprite
        self.speedX = 0 # speed in x direction
        self.speedY = 0 # speed in y direction

        self.target = None #start with no destination

    def get_direction(self, target):
        '''
        Function:
            takes total distance from sprite.center
            to the sprites target
            (gets direction to move)
        Returns:
            a normalized vector
        Parameters:
            - self
            - target
                x,y coordinates of the sprites target
                can be any x,y coorinate pair in
                brackets [x,y]
                or parentheses (x,y)
        '''
        if self.target: # if the square has a target
            position = Vector(self.rect.centerx, self.rect.centery) # create a vector from center x,y value
            target = Vector(target[0], target[1]) # and one from the target x,y
            self.dist = target - position # get total distance between target and position

            direction = self.dist.normalize() # normalize so its constant in all directions
            return direction

    def distance_check(self, dist):
        '''
        Function:
            tests if the total distance from the
            sprite to the target is smaller than the
            ammount of distance that would be normal
            for the sprite to travel
            (this lets the sprite know if it needs
            to slow down. we want it to slow
            down before it gets to it's target)
        Returns:
            bool
        Parameters:
            - self
            - dist
                this is the total distance from the
                sprite to the target
                can be any x,y value pair in
                brackets [x,y]
                or parentheses (x,y)
        '''
        dist_x = dist[0] ** 2 # gets absolute value of the x distance
        dist_y = dist[1] ** 2 # gets absolute value of the y distance
        t_dist = dist_x + dist_y # gets total absolute value distance
        speed = self.speed ** 2 # gets aboslute value of the speed

        if t_dist < (speed): # read function description above
            return True
        

    def updatePosition(self):
        '''
        Function:
            gets direction to move then applies
            the distance to the sprite.center
            ()
        Parameters:
            - self
        '''
        
        self.dir = self.get_direction(self.target) # get direction
        if self.dir: # if there is a direction to move
            
            if self.distance_check(self.dist): # if we need to stop
                self.rect.center = self.target # center the sprite on the target
                
            else: # if we need to move normal
                self.trueX += (self.dir[0] * self.speed) # calculate speed from direction to move and speed constant
                self.trueY += (self.dir[1] * self.speed)
                self.rect.center = (round(self.trueX),round(self.trueY)) # apply values to sprite.center

                angleRad = math.atan2(self.dist[1], self.dist[0]) #finds angle
                angleDeg = math.degrees(angleRad) #converts to degrees
                self.image = pygame.transform.rotate(self.image, (-angleDeg - 90)) #rotates sprite to match, and adjusts angle
                
    def updateAnim(self, animCounter, unitType):
        if animCounter >= 15 and animCounter <= 29:
            self.image = pygame.image.load(os.path.join('sprites', unitType.unitImage2))
            self.image.set_colorkey((255,255,255)) #half the time use sprite 2
            animCounter += 1
        elif animCounter >= 0 and animCounter <= 14:
            self.image = pygame.image.load(os.path.join('sprites', unitType.unitImage1))
            self.image.set_colorkey((255,255,255)) #otherwise use 1
            animCounter += 1
        else:
            animCounter = 0
            self.image = pygame.image.load(os.path.join('sprites', unitType.unitImage1))
            self.image.set_colorkey((255,255,255)) #reset counter, and use 1
        return animCounter

class unitType():
    unitName = ""
    unitImage1 = None
    unitImage2 = None
    unitSpeed = 0.0
    

def main(animCounter, unitList):

    screen = pygame.display.set_mode((640,480)) #initial settings
    pygame.display.set_caption("Sprite Test 1")
    background_color = pygame.Surface(screen.get_size()).convert()
    background_color.fill((21,22,32))
    
    SpriteList = pygame.sprite.Group() #list holding all sprites

    for object in unitList:
         # create the sprite
        SpriteList.add(Sprite(object))

    selectedObject = None

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1: #on left click
                    changed = False
                    for object in SpriteList: #for all sprites
                        if object.trueX < (event.pos[0] + 24) and object.trueX > (event.pos[0] - 24) and object.trueY < (event.pos[1] + 24) and object.trueY > (event.pos[1] - 24):
                            selectedObject = object #set new selected sprite
                            changed = True
                    if changed == False: #checks if nothing was selected
                        selectedObject = None
                if event.button == 3:
                    if selectedObject != None:
                        selectedObject.target = event.pos # set the sprite.target to the mouse click position

        screen.blit(background_color, (0,0))

        animInit = 0 #var to skip if for first run
        for object in SpriteList:
            if animInit == 1:
                animCounter -= 1 #resets animCounter each run, after first, to avoid speeding up
            animCounter = object.updateAnim(animCounter, object.unitType)
            animInit = 1

            object.updatePosition() #updates position of all sprites

        SpriteList.draw(screen) #draws sprites
        
        pygame.display.flip() #draw frame
    
    pygame.quit() # for a smooth quit

if __name__ == "__main__":
    animCounter = 0
    unitList = []

    #unit definitions
    stalker = unitType()
    stalker.unitName = "Stalker"
    stalker.unitImage1 = 'Stalker1 64x64.bmp'
    stalker.unitImage2 = 'Stalker2 64x64.bmp'
    stalker.unitSpeed = 2.953
    unitList.append(stalker)

    zealot = unitType()
    zealot.unitName = "Zealot"
    zealot.unitImage1 = 'Zealot1 48x48.bmp'
    zealot.unitImage2 = 'Zealot2 48x48.bmp'
    zealot.unitSpeed = 2.25
    unitList.append(zealot)

    marine = unitType()
    marine.unitName = "Marine"
    marine.unitImage1 = 'Marine1 48x48.bmp'
    marine.unitImage2 = 'Marine2 48x48.bmp'
    marine.unitSpeed = 2.25
    unitList.append(marine)

    marauder = unitType()
    marauder.unitName = "Marauder"
    marauder.unitImage1 = 'Marauder1 64x64.bmp'
    marauder.unitImage2 = 'Marauder2 64x64.bmp'
    marauder.unitSpeed = 2.25
    unitList.append(marauder)

    zergling = unitType()
    zergling.unitName = "Zergling"
    zergling.unitImage1 = 'Zergling1 32x32.bmp'
    zergling.unitImage2 = 'Zergling2 32x32.bmp'
    zergling.unitSpeed = 2.9531
    unitList.append(zergling)

    roach = unitType()
    roach.unitName = "Roach"
    roach.unitImage1 = 'Roach1 64x64.bmp'
    roach.unitImage2 = 'Roach2 64x64.bmp'
    roach.unitSpeed = 2.25
    unitList.append(roach)
    
    main(animCounter, unitList)
