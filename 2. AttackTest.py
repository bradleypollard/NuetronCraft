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
    
    def __init__(self, Type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('sprites', Type.Image1))
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255,255,255))
        self.Type = Type
        self.isAttack = False
        self.attackCounter = 0

        self.trueX = Type.x # created because self.rect.center does not hold
        self.trueY = Type.y # decimal values but these do
        self.rect.center = (self.trueX, self.trueY) # set starting position
        self.speed = Type.Speed # movement speed of the sprite
        self.speedX = 0 # speed in x direction
        self.speedY = 0 # speed in y direction

        self.targetSprite = None #start with no sprite targetted (for attacks only)
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
        

    def updatePosition(self, AttackList):
        '''
        Function:
            gets direction to move then applies
            the distance to the sprite.center
            ()
        Parameters:
            - self
        '''
        
        if self.targetSprite != None:
            if self.targetSprite.Type.unitHealth <= 0:
                self.targetSprite = None
                if self.isAttack == True:
                    self.kill()
            else:
                if self.isAttack == False:
                    actualDist = rangeCheck(self, self.targetSprite)
                    if actualDist <= (self.Type.attackType.attackRange * 100 + 50) and self.attackCounter >= (self.Type.attackType.attackCooldown * 30): #range check
                        AttackList.add(Sprite(self.Type.attackType))
                        thisAttack = getSpriteByPosition(len(AttackList) - 1, AttackList)
                        thisAttack.isAttack = True
                        thisAttack.trueX = self.trueX #sets start pos
                        thisAttack.trueY = self.trueY
                        thisAttack.targetSprite = self.targetSprite #saves target sprite for retargetting
                        thisAttack.target = self.targetSprite.rect.center #sets target
                        self.target = None
                    elif actualDist > (self.Type.attackType.attackRange * 100 + 50):
                        self.target = self.targetSprite.rect.center
                else:
                    self.target = self.targetSprite.rect.center
                
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
        return AttackList        
                
    def updateAnim(self, animCounter):
        if animCounter >= 15 and animCounter <= 29:
            self.image = pygame.image.load(os.path.join('sprites', self.Type.Image2))
            self.image.set_colorkey((255,255,255)) #half the time use sprite 2
            animCounter += 1
        elif animCounter >= 0 and animCounter <= 14:
            self.image = pygame.image.load(os.path.join('sprites', self.Type.Image1))
            self.image.set_colorkey((255,255,255)) #otherwise use 1
            animCounter += 1
        else:
            animCounter = 0
            self.image = pygame.image.load(os.path.join('sprites', self.Type.Image1))
            self.image.set_colorkey((255,255,255)) #reset counter, and use 1
        return animCounter

class unitType():
    unitName = ""
    x = 100
    y = 100
    Image1 = None
    Image2 = None
    Speed = 0.0
    unitAttack = None
    unitHealth = 0
    unitFlying = False

class attackType():
    x = 100
    y = 100
    Image1 = None
    Image2 = None
    Speed = 10
    attackName = ""
    attackDamage = 0
    attackAir = False
    attackGround = False
    attackRange = 0
    attackCooldown = 0.0

    def TakeDamage(self, unitType):
        if unitType.unitFlying == True:
            unitType.unitHealth -= (self.attackDamage * self.attackAir)
        else:
            unitType.unitHealth -= (self.attackDamage * self.attackGround)

def getSpriteByPosition(position,group):
    for index,spr in enumerate(group):
        if (index == position):
            return spr
    return False

def approxEquals(x1,x2,y1,y2):
    if x1 < (x2 + 24) and x1 > (x2 - 24) and y1 < (y2 + 24) and y1 > (y2 - 24):
        return True
    else:
        return False

def rangeCheck(selectedObject, target):
    objPosition = Vector(selectedObject.rect.centerx, selectedObject.rect.centery)
    targetPosition = Vector(target.rect.centerx, target.rect.centery)
    vectorDist = targetPosition - objPosition
    actualDist = vectorDist.length() #finds length between units
    return actualDist
    

def main(animCounter, unitTypeList, attackTypeList):

    screen = pygame.display.set_mode((640,480)) #initial settings
    pygame.display.set_caption("Attack Test 1")
    background_color = pygame.Surface(screen.get_size()).convert()
    background_color.fill((21,22,32))
    
    UnitList = pygame.sprite.Group() #list holding all sprites of Units
    AttackList = pygame.sprite.OrderedUpdates()

    for object in unitTypeList:
         # create the sprite
        UnitList.add(Sprite(object))

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
                    for object in UnitList: #for all sprites
                        if approxEquals(object.trueX, event.pos[0], object.trueY, event.pos[1]):
                            selectedObject = object #set new selected sprite
                            changed = True
                    if changed == False: #checks if nothing was selected
                        selectedObject = None
                if event.button == 3:
                    if selectedObject != None:
                        attacked = False
                        for object in UnitList: #for all sprites
                            if attacked == False and approxEquals(object.trueX, event.pos[0], object.trueY, event.pos[1]) and object != selectedObject:
                                #check distance is less than range
                                actualDist = rangeCheck(selectedObject, object)
                                if actualDist <= (selectedObject.Type.attackType.attackRange * 100 + 50) and selectedObject.attackCounter >= (selectedObject.Type.attackType.attackCooldown * 30): #range check
                                    AttackList.add(Sprite(selectedObject.Type.attackType))
                                    thisAttack = getSpriteByPosition(len(AttackList) - 1, AttackList)
                                    thisAttack.isAttack = True
                                    thisAttack.trueX = selectedObject.trueX #sets start pos
                                    thisAttack.trueY = selectedObject.trueY
                                    thisAttack.targetSprite = object #saves target sprite for retargetting
                                    thisAttack.target = object.rect.center #sets target
                                    attacked = True
                                    selectedObject.attackCounter = 0
                                    selectedObject.targetSprite = object
                                    selectedObject.target = None
                                elif actualDist <= (selectedObject.Type.attackType.attackRange * 100 + 50) and selectedObject.attackCounter < (selectedObject.Type.attackType.attackCooldown * 30):
                                    attacked = True
                                    print(selectedObject.attackCounter)
                                    print(object.Type.attackType.attackCooldown * 30)
                                elif actualDist > (selectedObject.Type.attackType.attackRange * 100 + 50):
                                    selectedObject.targetSprite = object
                                    attacked = True
                        if attacked == False: #checks if nothing was attacked 
                            selectedObject.target = event.pos # set the sprite.target to the mouse click position
                            selectedObject.targetSprite = None #no enemy target

        screen.blit(background_color, (0,0))

        animInit = 0 #var to skip if for first run
        for counter in range(0,2):
            if counter == 0:
                thisList = UnitList
            else:
                thisList = AttackList
                for object in AttackList:
                    if approxEquals(object.trueX, object.targetSprite.trueX, object.trueY, object.targetSprite.trueY):
                        object.Type.TakeDamage(object.targetSprite.Type) #apply damage to unit
                        if object.targetSprite.Type.unitHealth <= 0: #if health is gone, kill sprite
                            object.targetSprite.kill()
                        object.kill() #stops rendering upon collision
            for object in thisList:
                if animInit == 1:
                    animCounter -= 1 #resets animCounter each run, after first, to avoid speeding up
                animCounter = object.updateAnim(animCounter)
                animInit = 1
                if object.isAttack == False:
                    if object.attackCounter >= (object.Type.attackType.attackCooldown * 30) and object.targetSprite == None: #leaves counter at max
                        object.attackCounter = object.attackCounter
                    elif object.attackCounter >= (object.Type.attackType.attackCooldown * 30): #resets if attacking
                        object.attackCounter = 0
                    else:
                        object.attackCounter += 1
                AttackList = object.updatePosition(AttackList) #updates position of all sprites

        UnitList.draw(screen) #draws sprites
        AttackList.draw(screen)
        
        pygame.display.flip() #draw frame
    
    pygame.quit() # for a smooth quit

if __name__ == "__main__":
    animCounter = 0
    unitTypeList = []
    attackTypeList = []

    #attack definitions
    particleDisruptors = attackType()
    particleDisruptors.attackName = "Particle Disruptors"
    particleDisruptors.Image1 = 'StalkerAttack 32x32.bmp'
    particleDisruptors.Image2 = 'StalkerAttack 32x32.bmp'
    particleDisruptors.attackDamage = 10
    particleDisruptors.attackAir = True
    particleDisruptors.attackGround = True
    particleDisruptors.attackRange = 6
    particleDisruptors.attackCooldown = 1.44
    attackTypeList.append(particleDisruptors)

    psiBlades = attackType()
    psiBlades.attackname = "Psi Blades"
    psiBlades.Image1 = 'ZealotAttack 32x32.bmp'
    psiBlades.Image2 = 'ZealotAttack 32x32.bmp'
    psiBlades.attackDamage = 16
    psiBlades.attackAir = False
    psiBlades.attackGround = True
    psiBlades.attackRange = 0.1
    psiBlades.attackCooldown = 1.2
    attackTypeList.append(psiBlades)

    c14Rifle = attackType()
    c14Rifle.attackName = "C-14 Gauss Rifle"
    c14Rifle.Image1 = 'MarineAttack1 16x16.bmp'
    c14Rifle.Image2 = 'MarineAttack2 16x16.bmp'
    c14Rifle.attackDamage = 6
    c14Rifle.attackGround = True
    c14Rifle.attackAir = True
    c14Rifle.attackRange = 5
    c14Rifle.attackCooldown = 0.8608
    attackTypeList.append(c14Rifle)

    #unit definitions
    stalker = unitType()
    stalker.attackType = particleDisruptors
    stalker.y = 380
    stalker.unitName = "Stalker"
    stalker.Image1 = 'Stalker1 64x64.bmp'
    stalker.Image2 = 'Stalker2 64x64.bmp'
    stalker.Speed = 2.953
    stalker.unitHealth = 160
    unitFlying = False
    unitTypeList.append(stalker)

    zealot = unitType()
    zealot.attackType = psiBlades
    zealot.x = 540
    zealot.unitName = "Zealot"
    zealot.Image1 = 'Zealot1 48x48.bmp'
    zealot.Image2 = 'Zealot2 48x48.bmp'
    zealot.Speed = 2.25
    zealot.unitHealth = 150
    zealot.unitFlying = False
    unitTypeList.append(zealot)

    marine = unitType()
    marine.attackType = c14Rifle
    marine.x = 320
    marine.y = 240
    marine.unitName = "Marine"
    marine.Image1 = 'Marine1 48x48.bmp'
    marine.Image2 = 'Marine2 48x48.bmp'
    marine.Speed = 2.25
    marine.unitHealth = 45
    marine.unitFlying = False
    unitTypeList.append(marine)
    
    main(animCounter, unitTypeList, attackTypeList)
