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
        self.isBuilding = False
        self.attackCounter = 0
        self.researchCounter = 0

        self.trueX = Type.x # created because self.rect.center does not hold
        self.trueY = Type.y # decimal values but these do
        self.rect.center = (self.trueX, self.trueY) # set starting position
        self.speed = Type.Speed # movement speed of the sprite
        self.speedX = 0 # speed in x direction
        self.speedY = 0 # speed in y direction
        try:
            self.Health = Type.unitHealth #local store of class health amount
        except:
            self.Health = 0

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
            if self.targetSprite.Health <= 0:
                self.targetSprite = None
                if self.isAttack == True:
                    self.kill()
            else:
                if self.isAttack == False:
                    actualDist = rangeCheck(self, self.targetSprite)
                    if actualDist <= (self.Type.attackType.attackRange * 50 + (self.targetSprite.Type.size)) and self.attackCounter >= (self.Type.attackType.attackCooldown * 30): #range check
                        AttackList.add(Sprite(self.Type.attackType))
                        thisAttack = getSpriteByPosition(len(AttackList) - 1, AttackList)
                        thisAttack.isAttack = True
                        thisAttack.trueX = self.trueX #sets start pos
                        thisAttack.trueY = self.trueY
                        thisAttack.targetSprite = self.targetSprite #saves target sprite for retargetting
                        thisAttack.target = self.targetSprite.rect.center #sets target
                        if self.Type.attackType.Name == "Volatile Burst":
                            self.kill()
                        self.target = None
                    elif actualDist > (self.Type.attackType.attackRange * 50 + (self.targetSprite.Type.size)):
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
    Name = ""
    x = 100
    y = 100
    size = 64
    Image1 = None
    Image2 = None
    Speed = 0.0
    Team = None
    buildTime = 0
    unitAttack = None
    unitHealth = 100
    unitFlying = False

class attackType():
    x = 100
    y = 100
    size = 32
    Image1 = None
    Image2 = None
    Speed = 10
    Name = ""
    attackDamage = 0
    attackAir = False
    attackGround = False
    attackRange = 0
    attackCooldown = 0.0

    def TakeDamage(self, Sprite):
        if Sprite.Type.unitFlying == True:
            Sprite.Health -= (self.attackDamage * self.attackAir) #multiply damamge by flying or not, to cancel out if can't hit air/ground
        else:
            Sprite.Health -= (self.attackDamage * self.attackGround)

class buildingType():
    x = 100
    y = 100
    size = 128
    unitHealth = 100
    Image1 = None
    Speed = 0
    Name = ""
    Team = None
    unitFlying = False
    isResearching = False
    researchType = None
    hotKey = [] #letters associated with the units in unitorder
    unitOrder = [] #the units which correspond to the letter of the same index in hotKeys

    def research(self, selectedObject, letter):
        keyUsed = False
        usedAt = 0
        for n in range(0, len(selectedObject.Type.hotKey)): #find index of key used, if it it
            if selectedObject.Type.hotKey[n] == letter:
                keyUsed = True
                usedAt = n
        if keyUsed == True:
            selectedObject.Type.isResearching = True #starts research/build required item, if this key is used
            for object in unitTypeList:
                if object.Name == selectedObject.Type.unitOrder[usedAt]:
                    selectedObject.Type.researchType = object #sets the research type to a unit

def getSpriteByPosition(position,group):
    for index,spr in enumerate(group):
        if (index == position):
            return spr
    return False

def approxEquals(clickedObject,x2,y2):
    if clickedObject.trueX < (x2 + (clickedObject.Type.size / 2)) and clickedObject.trueX > (x2 - (clickedObject.Type.size / 2)) and clickedObject.trueY < (y2 + (clickedObject.Type.size / 2)) and clickedObject.trueY > (y2 - (clickedObject.Type.size / 2)):
        return True
    else:
        return False

def rangeCheck(selectedObject, target):
    objPosition = Vector(selectedObject.rect.centerx, selectedObject.rect.centery)
    targetPosition = Vector(target.rect.centerx, target.rect.centery)
    vectorDist = targetPosition - objPosition
    actualDist = vectorDist.length() #finds length between units
    return actualDist
    

def main(animCounter, unitTypeList, attackTypeList, buildingTypeList):
    screenSize = [800,600]
    screen = pygame.display.set_mode((screenSize[0],screenSize[1])) #initial settings
    pygame.display.set_caption("Attack Test 2 - Auto & Building")
    background_image = pygame.image.load(os.path.join('sprites', 'TempBG 3600x600.png')).convert()
    imageSize = [3600,600]
    horCoordinate = 0 #bg scrolling vars
    verCoordinate = 0
    horVelocity = 0
    verVelocity = 0
    minVer = 0
    minHor = 0
    maxVer = imageSize[1] - screenSize[1]
    maxHor = imageSize[0] - screenSize[0]
    
    
    UnitList = pygame.sprite.OrderedUpdates() #list holding all sprites of Units
    AttackList = pygame.sprite.OrderedUpdates()
    BuildingList = pygame.sprite.OrderedUpdates()

    for object in buildingTypeList:
         # create the sprite
        BuildingList.add(Sprite(object))
        thisBuilding = getSpriteByPosition(len(BuildingList) - 1, BuildingList)
        thisBuilding.isBuilding = True

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
                        if approxEquals(object, event.pos[0], event.pos[1]):
                            selectedObject = object #set new selected sprite
                            changed = True
                    for object in BuildingList: #for all buildings too
                        if approxEquals(object, event.pos[0], event.pos[1]):
                            selectedObject = object #set new selected sprite
                            changed = True
                    if changed == False: #checks if the background was selected, and sets no selected object
                        selectedObject = None
                if event.button == 3:
                    if selectedObject != None:
                        if selectedObject.isBuilding != True:
                            attacked = False
                            for object in UnitList: #for all sprites
                                if attacked == False and approxEquals(object, event.pos[0], event.pos[1]) and object != selectedObject and object.Type.Team != selectedObject.Type.Team and (selectedObject.Type.attackType.attackAir == object.Type.unitFlying or selectedObject.Type.attackType.attackGround != object.Type.unitFlying):
                                    #check distance is less than range
                                    actualDist = rangeCheck(selectedObject, object)
                                    if actualDist <= (selectedObject.Type.attackType.attackRange * 50 + (object.Type.size)) and selectedObject.attackCounter >= (selectedObject.Type.attackType.attackCooldown * 30): #range check
                                        AttackList.add(Sprite(selectedObject.Type.attackType))
                                        thisAttack = getSpriteByPosition(len(AttackList) - 1, AttackList)
                                        thisAttack.isAttack = True
                                        thisAttack.trueX = selectedObject.trueX #sets start pos
                                        thisAttack.trueY = selectedObject.trueY
                                        thisAttack.targetSprite = object #saves target sprite for retargetting
                                        thisAttack.target = object.rect.center #sets target
                                        if selectedObject.Type.attackType.Name == "Volatile Burst":
                                            selectedObject.kill()
                                        attacked = True
                                        selectedObject.attackCounter = 0
                                        selectedObject.targetSprite = object
                                        selectedObject.target = None
                                    elif (actualDist > (selectedObject.Type.attackType.attackRange * 50 + (object.Type.size))) or (actualDist <= (selectedObject.Type.attackType.attackRange * 50 + (object.Type.size)) and selectedObject.attackCounter < (selectedObject.Type.attackType.attackCooldown * 30)):
                                        selectedObject.targetSprite = object
                                        attacked = True
                            for object in BuildingList: #for all sprites
                                if attacked == False and approxEquals(object, event.pos[0], event.pos[1]) and object != selectedObject and object.Type.Team != selectedObject.Type.Team and (selectedObject.Type.attackType.attackAir == object.Type.unitFlying or selectedObject.Type.attackType.attackGround != object.Type.unitFlying):
                                    #check distance is less than range
                                    actualDist = rangeCheck(selectedObject, object)
                                    if actualDist <= (selectedObject.Type.attackType.attackRange * 50 + (object.Type.size)) and selectedObject.attackCounter >= (selectedObject.Type.attackType.attackCooldown * 30): #range check
                                        AttackList.add(Sprite(selectedObject.Type.attackType))
                                        thisAttack = getSpriteByPosition(len(AttackList) - 1, AttackList)
                                        thisAttack.isAttack = True
                                        thisAttack.trueX = selectedObject.trueX #sets start pos
                                        thisAttack.trueY = selectedObject.trueY
                                        thisAttack.targetSprite = object #saves target sprite for retargetting
                                        thisAttack.target = object.rect.center #sets target
                                        if selectedObject.Type.attackType.Name == "Volatile Burst":
                                            selectedObject.kill()
                                        attacked = True
                                        selectedObject.attackCounter = 0
                                        selectedObject.targetSprite = object
                                        selectedObject.target = None
                                    elif (actualDist > (selectedObject.Type.attackType.attackRange * 50 + (object.Type.size))) or (actualDist <= (selectedObject.Type.attackType.attackRange * 50 + (object.Type.size)) and selectedObject.attackCounter < (selectedObject.Type.attackType.attackCooldown * 30)):
                                        selectedObject.targetSprite = object
                                        attacked = True
                            if attacked == False: #checks if nothing was attacked
                                selectedObject.target = event.pos # set the sprite.target to the mouse click position
                                selectedObject.targetSprite = None #no enemy target
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: #keydown a
                    if selectedObject != None and selectedObject.isBuilding == True and selectedObject.Type.isResearching == False:
                        selectedObject.Type.research(selectedObject, "a")
                if event.key == pygame.K_c: #keydown c
                    if selectedObject != None and selectedObject.isBuilding == True and selectedObject.Type.isResearching == False:
                        selectedObject.Type.research(selectedObject, "c")
                if event.key == pygame.K_d: #keydown d
                    if selectedObject != None and selectedObject.isBuilding == True and selectedObject.Type.isResearching == False:
                        selectedObject.Type.research(selectedObject, "d")
                if event.key == pygame.K_e: #keydown e
                    if selectedObject != None and selectedObject.isBuilding == True and selectedObject.Type.isResearching == False:
                        selectedObject.Type.research(selectedObject, "e")
                if event.key == pygame.K_h: #keydown h
                    if selectedObject != None and selectedObject.isBuilding == True and selectedObject.Type.isResearching == False:
                        selectedObject.Type.research(selectedObject, "h")
                if event.key == pygame.K_i: #keydown i
                    if selectedObject != None and selectedObject.isBuilding == True and selectedObject.Type.isResearching == False:
                        selectedObject.Type.research(selectedObject, "i")
                if event.key == pygame.K_r: #keydown r
                    if selectedObject != None and selectedObject.isBuilding == True and selectedObject.Type.isResearching == False:
                        selectedObject.Type.research(selectedObject, "r")
                if event.key == pygame.K_s: #keydown s
                    if selectedObject != None and selectedObject.isBuilding == True and selectedObject.Type.isResearching == False:
                        selectedObject.Type.research(selectedObject, "s")
                if event.key == pygame.K_t: #keydown t
                    if selectedObject != None and selectedObject.isBuilding == True and selectedObject.Type.isResearching == False:
                        selectedObject.Type.research(selectedObject, "t")
                if event.key == pygame.K_v: #keydown v
                    if selectedObject != None and selectedObject.isBuilding == True and selectedObject.Type.isResearching == False:
                        selectedObject.Type.research(selectedObject, "v")
                if event.key == pygame.K_x: #keydown x
                    if selectedObject != None and selectedObject.isBuilding == True and selectedObject.Type.isResearching == False:
                        selectedObject.Type.research(selectedObject, "x")
                if event.key == pygame.K_z: #keydown z
                    if selectedObject != None and selectedObject.isBuilding == True and selectedObject.Type.isResearching == False: #if a building and not researching
                        selectedObject.Type.research(selectedObject, "z") #research this building's z, if it has one.
                if event.key == pygame.K_ESCAPE:
                    if selectedObject != None and selectedObject.isBuilding == True and selectedObject.Type.isResearching == True:
                        selectedObject.Type.isResearching = False
                        selectedObject.researchCounter = 0
                        selectedObject.Type.researchType = None
                        originalImage = pygame.image.load(os.path.join('sprites', selectedObject.Type.Image1))
                        selectedObject.image.blit(originalImage, originalImage.get_rect())
                if event.key == pygame.K_RIGHT: #sets bg scrolling on
                    horVelocity += 10
                if event.key == pygame.K_LEFT:
                    horVelocity -= 10
                if event.key == pygame.K_UP:
                    verVelocity -= 10
                if event.key == pygame.K_DOWN:
                    verVelocity += 10
            if event.type == pygame.KEYUP: 
                if event.key == pygame.K_RIGHT:
                    horVelocity -= 10
                if event.key == pygame.K_LEFT: #sets bg scrolling off
                    horVelocity += 10
                if event.key == pygame.K_UP:
                    verVelocity += 10
                if event.key == pygame.K_DOWN:
                    verVelocity -= 10

        if horVelocity or verVelocity != 0:
            horCoordinate += horVelocity #moves bg when key held
            verCoordinate += verVelocity

            AllSprites = [UnitList, AttackList, BuildingList]#define list of all lists
            for object in AllSprites:  #move all sprites too
                for object in object:
                    if horCoordinate <= maxHor and horCoordinate >= minHor: #adjust x postition unless at edge
                        object.trueX -= horVelocity
                        if object.isBuilding == False and object.isAttack == False and object.target != None:
                            object.target = ((object.target[0] - horVelocity), object.target[1])
                    if verCoordinate <= maxVer and verCoordinate >= minVer: #adjust y position
                        object.trueY -= verVelocity
                        if object.isBuilding == False and object.isAttack == False and object.target != None:
                            object.target = ((object.target[0]), (object.target[1] - verVelocity))
                    object.rect.center = (round(object.trueX),round(object.trueY))
        
            if horCoordinate > maxHor: #stops at edges of bg
                horCoordinate = maxHor
            if horCoordinate < minHor:
                horCoordinate = minHor
            if verCoordinate > maxVer:
                verCoordinate = maxVer
            if verCoordinate < minVer:
                verCoordinate = minVer
        
        screen.fill((0,0,0))
        viewport = background_image.subsurface((horCoordinate, verCoordinate) + (800, 600))
        screen.blit(viewport, (0,0))
        
        #auto attack
        for a in UnitList:
            for object in UnitList:
                actualDist = rangeCheck(a, object)
                if (a.target == a.rect.center or a.target == None) and actualDist <= (a.Type.attackType.attackRange * 50 + (object.Type.size)) and a.attackCounter >= (a.Type.attackType.attackCooldown * 30) and a != object and a.Type.Team != object.Type.Team and (a.Type.attackType.attackAir == object.Type.unitFlying or a.Type.attackType.attackGround != object.Type.unitFlying):
                    AttackList.add(Sprite(a.Type.attackType))
                    thisAttack = getSpriteByPosition(len(AttackList) - 1, AttackList)
                    thisAttack.isAttack = True
                    thisAttack.trueX = a.trueX #sets start pos
                    thisAttack.trueY = a.trueY
                    thisAttack.targetSprite = object #saves target sprite for retargetting
                    thisAttack.target = object.rect.center #sets target
                    if a.Type.attackType.Name == "Volatile Burst":
                        a.kill()
                    a.attackCounter = 0
                    a.targetSprite = object
                    a.target = None
              
        #building collision commented out for now because poorly implemented
        '''
        for object in BuildingList: #building list collisions
            collisionList = pygame.sprite.spritecollide(object, UnitList, False) #obtain list of any hits with units
            Building = object
            for object in collisionList:
                object.target = None #stop moving
                object.rect.center = (object.trueX - 6, object.trueY - 6) #move out of collision range to allow retargeting
                if pygame.sprite.collide_rect(object, Building): #check move worked
                    object.rect.center = (object.trueX + 12, object.trueY + 12) #move in other direction to compensate
        '''        


        
        animInit = 0 #var to skip if for first run
        for counter in range(0,2):
            if counter == 0:
                thisList = UnitList
            else:
                thisList = AttackList
                for object in AttackList:
                    if approxEquals(object.targetSprite, object.trueX, object.trueY):
                        object.Type.TakeDamage(object.targetSprite) #apply damage to unit
                        if object.targetSprite.Health <= 0: #if health is gone, kill sprite
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

        

        font = pygame.font.Font(None, 36) #completion percentages
        for object in BuildingList:
            if object.Type.isResearching == True:
                originalImage = pygame.image.load(os.path.join('sprites', object.Type.Image1))
                if object.researchCounter >= (object.Type.researchType.buildTime):
                    object.Type.researchType.x = object.trueX + 96
                    object.Type.researchType.y = object.trueY + 96 #sets spawn point
                    UnitList.add(Sprite(object.Type.researchType))
                    object.researchCounter = 0
                    object.Type.researchType = None
                    object.Type.isResearching = False
                    object.image.blit(originalImage, originalImage.get_rect())
                else:
                    object.researchCounter += 1
                    object.image.blit(originalImage, originalImage.get_rect())
                    percentage = (round(((object.researchCounter / (object.Type.researchType.buildTime)) * 100)))
                    text = font.render(str(percentage) + "%", 1, (0,0,255))
                    textPos = text.get_rect(center=(100, 100))
                    object.image.blit(text, textPos)
                    
        UnitList.draw(screen) #draws sprites
        AttackList.draw(screen)
        BuildingList.draw(screen)
        
        pygame.display.flip() #draw frame
    
    pygame.quit() # for a smooth quit

if __name__ == "__main__":
    animCounter = 0
    unitTypeList = []
    attackTypeList = []
    buildingTypeList = []
    

    #building definitions
    
    gateway = buildingType()
    gateway.Name = "Gateway"
    gateway.Image1 = "Gateway 128x128.bmp"
    gateway.Team = "Protoss"
    gateway.hotKey = ["s", "z"]
    gateway.unitOrder = ["Stalker", "Zealot"]
    buildingTypeList.append(gateway)

    barracks = buildingType()
    barracks.Name = "Barracks"
    barracks.Image1 = "Barracks 128x128.bmp"
    barracks.Team = "Terran"
    barracks.hotKey = ["a", "d"]
    barracks.unitOrder = ["Marine", "Marauder"]
    barracks.x = 300
    buildingTypeList.append(barracks)

    factory = buildingType()
    factory.Name = "Factory"
    factory.Image1 = "Factory 128x128.bmp"
    factory.Team = "Terran"
    factory.hotKey = ["s","e"]
    factory.unitOrder = ["Siege Tank", "Hellion"]
    factory.x = 500
    buildingTypeList.append(factory)

    starport = buildingType()
    starport.Name = "Starport"
    starport.Image1 = "Starport 128x128.bmp"
    starport.Team = "Terran"
    starport.hotKey = ["e","v"]
    starport.unitOrder = ["Banshee", "Viking"]
    starport.x = 700
    buildingTypeList.append(starport)

    roboticsFacility = buildingType()
    roboticsFacility.Name = "Robotics Facility"
    roboticsFacility.Image1 = "Robotics 128x128.bmp"
    roboticsFacility.Team = "Protoss"
    roboticsFacility.hotKey = ["c", "i"]
    roboticsFacility.unitOrder = ["Colossus", "Immortal"]
    roboticsFacility.y = 300
    buildingTypeList.append(roboticsFacility)

    stargate = buildingType()
    stargate.Name = "Stargate"
    stargate.Image1 = "Stargate 128x128.bmp"
    stargate.Team = "Protoss"
    stargate.hotKey = ["v", "x"]
    stargate.unitOrder = ["Void Ray", "Phoenix"]
    stargate.y = 500
    buildingTypeList.append(stargate)

    spawningPool = buildingType()
    spawningPool.Name = "Spawning Pool"
    spawningPool.Image1 = "Pool 128x128.bmp"
    spawningPool.Team = "Zerg"
    spawningPool.hotKey = ["e","z"]
    spawningPool.unitOrder = ["Baneling", "Zergling"]
    spawningPool.y = 500
    spawningPool.x = 300
    buildingTypeList.append(spawningPool)

    roachWarren = buildingType()
    roachWarren.Name = "Roach Warren"
    roachWarren.Image1 = "RoachWarren 128x128.bmp"
    roachWarren.Team = "Zerg"
    roachWarren.hotKey = ["h","r"]
    roachWarren.unitOrder = ["Hydralisk", "Roach"]
    roachWarren.y = 500
    roachWarren.x = 500
    buildingTypeList.append(roachWarren)

    spire = buildingType()
    spire.Name = "Spire"
    spire.Image1 = "Spire 128x128.bmp"
    spire.Team = "Zerg"
    spire.hotKey = ["c","t"]
    spire.unitOrder = ["Corruptor", "Mutalisk"]
    spire.y = 500
    spire.x = 700
    buildingTypeList.append(spire)

    #attack definitions
    
    particleDisruptors = attackType()
    particleDisruptors.Name = "Particle Disruptors"
    particleDisruptors.Image1 = 'StalkerAttack 32x32.bmp'
    particleDisruptors.Image2 = 'StalkerAttack 32x32.bmp'
    particleDisruptors.attackDamage = 10
    particleDisruptors.attackAir = True
    particleDisruptors.attackGround = True
    particleDisruptors.attackRange = 6
    particleDisruptors.attackCooldown = 1.44
    attackTypeList.append(particleDisruptors)

    psiBlades = attackType()
    psiBlades.Name = "Psi Blades"
    psiBlades.Image1 = 'ZealotAttack 32x32.bmp'
    psiBlades.Image2 = 'ZealotAttack 32x32.bmp'
    psiBlades.attackDamage = 16
    psiBlades.attackAir = False
    psiBlades.attackGround = True
    psiBlades.attackRange = 0.1
    psiBlades.attackCooldown = 1.2
    attackTypeList.append(psiBlades)

    c14Rifle = attackType()
    c14Rifle.Size = 16
    c14Rifle.Name = "C-14 Gauss Rifle"
    c14Rifle.Image1 = 'MarineAttack1 16x16.bmp'
    c14Rifle.Image2 = 'MarineAttack2 16x16.bmp'
    c14Rifle.attackDamage = 6
    c14Rifle.attackGround = True
    c14Rifle.attackAir = True
    c14Rifle.attackRange = 5
    c14Rifle.attackCooldown = 0.8608
    attackTypeList.append(c14Rifle)

    punisherGrenades = attackType()
    punisherGrenades.Name = "Punisher Grenades"
    punisherGrenades.Image1 = 'MarauderAttack1 32x32.bmp'
    punisherGrenades.Image2 = 'MarauderAttack2 32x32.bmp'
    punisherGrenades.attackDamage = 10
    punisherGrenades.attackGround = True
    punisherGrenades.attackAir = False
    punisherGrenades.attackRange = 6
    punisherGrenades.attackCooldown = 1.5
    attackTypeList.append(punisherGrenades)

    internalFlamethrower = attackType()
    internalFlamethrower.Name = "Internal Flamethrower"
    internalFlamethrower.Image1 = 'HellionAttack1 32x64.bmp'
    internalFlamethrower.Image2 = 'HellionAttack2 32x64.bmp'
    internalFlamethrower.attackDamage = 8
    internalFlamethrower.attackGround = True
    internalFlamethrower.attackAir = False
    internalFlamethrower.attackRange = 5
    internalFlamethrower.attackCooldown = 2.5
    attackTypeList.append(internalFlamethrower)

    Cannon = attackType()
    Cannon.Name = "90mm Twin Cannon"
    Cannon.Image1 = 'SiegeTankAttack 32x32.bmp'
    Cannon.Image2 = 'SiegeTankAttack 32x32.bmp'
    Cannon.attackDamage = 10
    Cannon.attackGround = True
    Cannon.attackAir = False
    Cannon.attackRange = 7
    Cannon.attackCooldown = 1.04
    attackTypeList.append(Cannon)

    backlashRockets = attackType()
    backlashRockets.Name = "Backlash Rockets"
    backlashRockets.Image1 = 'BansheeAttack 32x32.bmp'
    backlashRockets.Image2 = 'BansheeAttack 32x32.bmp'
    backlashRockets.attackDamage = 24
    backlashRockets.attackGround = True
    backlashRockets.attackAir = False
    backlashRockets.attackRange = 6
    backlashRockets.attackCooldown = 1.25
    attackTypeList.append(backlashRockets)

    lanzerTorpedoes = attackType()
    lanzerTorpedoes.Name = "Lanzer Torpedoes"
    lanzerTorpedoes.Image1 = 'VikingAttack1 32x32.bmp'
    lanzerTorpedoes.Image2 = 'VikingAttack2 32x32.bmp'
    lanzerTorpedoes.attackDamage = 20
    lanzerTorpedoes.attackGround = False
    lanzerTorpedoes.attackAir = True
    lanzerTorpedoes.attackRange = 9
    lanzerTorpedoes.attackCooldown = 2
    attackTypeList.append(lanzerTorpedoes)

    thermalLances = attackType()
    thermalLances.Name = "Thermal Lances"
    thermalLances.Image1 = 'ColossusAttack1 32x64.bmp'
    thermalLances.Image2 = 'ColossusAttack2 32x64.bmp'
    thermalLances.attackDamage = 30
    thermalLances.attackGround = True
    thermalLances.attackAir = False
    thermalLances.attackRange = 9
    thermalLances.attackCooldown = 1.65
    attackTypeList.append(thermalLances)

    phaseDisruptors = attackType()
    phaseDisruptors.Name = "Phase Disruptors"
    phaseDisruptors.Image1 = 'ImmortalAttack 32x32.bmp'
    phaseDisruptors.Image2 = 'ImmortalAttack 32x32.bmp'
    phaseDisruptors.attackDamage = 20
    phaseDisruptors.attackGround = True
    phaseDisruptors.attackAir = False
    phaseDisruptors.attackRange = 6
    phaseDisruptors.attackCooldown = 1.45
    attackTypeList.append(phaseDisruptors)

    prismaticBeam = attackType()
    prismaticBeam.Name = "Prismatic Beam"
    prismaticBeam.Image1 = 'VoidRayAttack1 32x64.bmp'
    prismaticBeam.Image2 = 'VoidRayAttack2 32x64.bmp'
    prismaticBeam.attackDamage = 8
    prismaticBeam.attackGround = True
    prismaticBeam.attackAir = True
    prismaticBeam.attackRange = 6
    prismaticBeam.attackCooldown = 0.6
    attackTypeList.append(prismaticBeam)

    ionCannons = attackType()
    ionCannons.Name = "Ion Cannons"
    ionCannons.Image1 = 'PhoenixAttack1 32x32.bmp'
    ionCannons.Image2 = 'PhoenixAttack2 32x32.bmp'
    ionCannons.attackDamage = 10
    ionCannons.attackGround = False
    ionCannons.attackAir = True
    ionCannons.attackRange = 4
    ionCannons.attackCooldown = 1.11
    attackTypeList.append(ionCannons)

    claws = attackType()
    claws.size = 16
    claws.Name = "Claws"
    claws.Image1 = 'ZerglingAttack 16x16.bmp'
    claws.Image2 = 'ZerglingAttack 16x16.bmp'
    claws.attackDamage = 5
    claws.attackGround = True
    claws.attackAir = False
    claws.attackRange = 0.1
    claws.attackCooldown = 0.587
    attackTypeList.append(claws)

    volatileBurst = attackType()
    volatileBurst.Name = "Volatile Burst"
    volatileBurst.Image1 = 'BanelingAttack 32x32.bmp'
    volatileBurst.Image2 = 'BanelingAttack 32x32.bmp'
    volatileBurst.attackDamage = 35
    volatileBurst.attackGround = True
    volatileBurst.attackAir = False
    volatileBurst.attackRange = 0.1
    volatileBurst.attackCooldown = 0.833
    attackTypeList.append(volatileBurst)

    acidSaliva = attackType()
    acidSaliva.Name = "Acid Saliva"
    acidSaliva.Image1 = 'RoachAttack1 32x32.bmp'
    acidSaliva.Image2 = 'RoachAttack2 32x32.bmp'
    acidSaliva.attackDamage = 16
    acidSaliva.attackGround = True
    acidSaliva.attackAir = False
    acidSaliva.attackRange = 4
    acidSaliva.attackCooldown = 2
    attackTypeList.append(acidSaliva)

    needleSpines = attackType()
    needleSpines.size = 16
    needleSpines.Name = "Needle Spines"
    needleSpines.Image1 = 'HydraAttack 16x16.bmp'
    needleSpines.Image2 = 'HydraAttack 16x16.bmp'
    needleSpines.attackDamage = 12
    needleSpines.attackGround = True
    needleSpines.attackAir = True
    needleSpines.attackRange = 5
    needleSpines.attackCooldown = 0.83
    attackTypeList.append(needleSpines)

    glaiveWurm = attackType()
    glaiveWurm.Name = "Glaive Wurm"
    glaiveWurm.Image1 = 'MutaliskAttack 16x16.bmp'
    glaiveWurm.Image2 = 'MutaliskAttack 16x16.bmp'
    glaiveWurm.attackDamage = 9
    glaiveWurm.attackGround = True
    glaiveWurm.attackAir = True
    glaiveWurm.attackRange = 3
    glaiveWurm.attackCooldown = 1.5246
    attackTypeList.append(glaiveWurm)

    parasiteSpores = attackType()
    parasiteSpores.Name = "Parasite Spores"
    parasiteSpores.Image1 = 'CorruptorAttack1 32x32.bmp'
    parasiteSpores.Image2 = 'CorruptorAttack2 32x32.bmp'
    parasiteSpores.attackDamage = 14
    parasiteSpores.attackGround = False
    parasiteSpores.attackAir = True
    parasiteSpores.attackRange = 6
    parasiteSpores.attackCooldown = 1.9
    attackTypeList.append(parasiteSpores)
    
    #unit definitions
    
    stalker = unitType()
    stalker.attackType = particleDisruptors
    stalker.Name = "Stalker"
    stalker.Team = "Protoss"
    stalker.Image1 = 'Stalker1 64x64.bmp'
    stalker.Image2 = 'Stalker2 64x64.bmp'
    stalker.Speed = 2.953
    stalker.buildTime = 42
    stalker.unitHealth = 160
    unitFlying = False
    unitTypeList.append(stalker)

    zealot = unitType()
    zealot.size = 48
    zealot.attackType = psiBlades
    zealot.Name = "Zealot"
    zealot.Team = "Protoss"
    zealot.Image1 = 'Zealot1 48x48.bmp'
    zealot.Image2 = 'Zealot2 48x48.bmp'
    zealot.Speed = 2.25
    zealot.buildTime = 38
    zealot.unitHealth = 150
    zealot.unitFlying = False
    unitTypeList.append(zealot)

    marine = unitType()
    marine.size = 48
    marine.attackType = c14Rifle
    marine.Name = "Marine"
    marine.Team = "Terran"
    marine.Image1 = 'Marine1 48x48.bmp'
    marine.Image2 = 'Marine2 48x48.bmp'
    marine.Speed = 2.25
    marine.buildTime = 25
    marine.unitHealth = 45
    marine.unitFlying = False
    unitTypeList.append(marine)

    marauder = unitType()
    marauder.attackType = punisherGrenades
    marauder.Name = "Marauder"
    marauder.Team = "Terran"
    marauder.Image1 = 'Marauder1 64x64.bmp'
    marauder.Image2 = 'Marauder2 64x64.bmp'
    marauder.Speed = 2.25
    marauder.buildTime = 30
    marauder.unitHealth = 125
    marauder.unitFlying = False
    unitTypeList.append(marauder)

    hellion = unitType()
    hellion.attackType = internalFlamethrower
    hellion.Name = "Hellion"
    hellion.Team = "Terran"
    hellion.Image1 = 'Hellion1 64x64.bmp'
    hellion.Image2 = 'Hellion2 64x64.bmp'
    hellion.Speed = 4.25
    hellion.buildTime = 30
    hellion.unitHealth = 90
    hellion.unitFlying = False
    unitTypeList.append(hellion)

    tank = unitType()
    tank.attackType = Cannon
    tank.Name = "Siege Tank"
    tank.Team = "Terran"
    tank.Image1 = 'SiegeTank1 64x64.bmp'
    tank.Image2 = 'SiegeTank2 64x64.bmp'
    tank.Speed = 2.25
    tank. buildTime = 45
    tank.unitHealth = 160
    tank.unitFlying = False
    unitTypeList.append(tank)

    banshee = unitType()
    banshee.attackType = backlashRockets
    banshee.Name = "Banshee"
    banshee.Team = "Terran"
    banshee.Image1 = 'Banshee1 64x64.bmp'
    banshee.Image2 = 'Banshee2 64x64.bmp'
    banshee.Speed = 2.75
    banshee. buildTime = 60
    banshee.unitHealth = 140
    banshee.unitFlying = True
    unitTypeList.append(banshee)

    viking = unitType()
    viking.attackType = lanzerTorpedoes
    viking.Name = "Viking"
    viking.Team = "Terran"
    viking.Image1 = 'Viking1 64x64.bmp'
    viking.Image2 = 'Viking2 64x64.bmp'
    viking.Speed = 2.75
    viking.buildTime = 42
    viking.unitHealth = 125
    viking.unitFlying = True
    unitTypeList.append(viking)

    colossus = unitType()
    colossus.size = 128
    colossus.attackType = thermalLances
    colossus.Name = "Colossus"
    colossus.Team = "Protoss"
    colossus.Image1 = 'Colossus1 128x128.bmp'
    colossus.Image2 = 'Colossus2 128x128.bmp'
    colossus.Speed = 2.25
    colossus.buildTime = 75
    colossus.unitHealth = 350
    colossus.unitFlying = False
    unitTypeList.append(colossus)

    immortal = unitType()
    immortal.attackType = phaseDisruptors
    immortal.Name = "Immortal"
    immortal.Team = "Protoss"
    immortal.Image1 = 'Immortal1 64x64.bmp'
    immortal.Image2 = 'Immortal2 64x64.bmp'
    immortal.Speed = 2.25
    immortal.buildTime = 55
    immortal.unitHealth = 300
    immortal.unitFlying = False
    unitTypeList.append(immortal)

    voidRay = unitType()
    voidRay.attackType = prismaticBeam
    voidRay.Name = "Void Ray"
    voidRay.Team = "Protoss"
    voidRay.Image1 = 'VoidRay1 64x64.bmp'
    voidRay.Image2 = 'VoidRay2 64x64.bmp'
    voidRay.Speed = 2.25
    voidRay.buildTime = 60
    voidRay.unitHealth = 250
    voidRay.unitFlying = True
    unitTypeList.append(voidRay)

    phoenix = unitType()
    phoenix.attackType = ionCannons
    phoenix.Name = "Phoenix"
    phoenix.Team = "Protoss"
    phoenix.Image1 = 'Phoenix1 64x64.bmp'
    phoenix.Image2 = 'Phoenix2 64x64.bmp'
    phoenix.Speed = 4.25
    phoenix.buildTime = 35
    phoenix.unitHealth = 180
    phoenix.unitFlying = True
    unitTypeList.append(phoenix)

    zergling = unitType()
    zergling.size = 32
    zergling.attackType = claws
    zergling.Name = "Zergling"
    zergling.Team = "Zerg"
    zergling.Image1 = 'Zergling1 32x32.bmp'
    zergling.Image2 = 'Zergling2 32x32.bmp'
    zergling.Speed = 4.6991
    zergling.buildTime = 24
    zergling.unitHealth = 35
    zergling.unitFlying = False
    unitTypeList.append(zergling)

    baneling = unitType()
    baneling.size = 32
    baneling.attackType = volatileBurst
    baneling.Name = "Baneling"
    baneling.Team = "Zerg"
    baneling.Image1 = 'Baneling1 32x32.bmp'
    baneling.Image2 = 'Baneling2 32x32.bmp'
    baneling.Speed = 2.9531
    baneling.buildTime = 44
    baneling.unitHealth = 30
    baneling.unitFlying = False
    unitTypeList.append(baneling)

    roach = unitType()
    roach.attackType = acidSaliva
    roach.Name = "Roach"
    roach.Team = "Zerg"
    roach.Image1 = 'Roach1 64x64.bmp'
    roach.Image2 = 'Roach2 64x64.bmp'
    roach.Speed = 2.25
    roach.buildTime = 27
    roach.unitHealth = 145
    roach.unitFlying = False
    unitTypeList.append(roach)

    hydralisk = unitType()
    hydralisk.attackType = needleSpines
    hydralisk.Name = "Hydralisk"
    hydralisk.Team = "Zerg"
    hydralisk.Image1 = 'Hydra1 64x64.bmp'
    hydralisk.Image2 = 'Hydra2 64x64.bmp'
    hydralisk.Speed = 2.25
    hydralisk.buildTime = 33
    hydralisk.unitHealth = 80
    hydralisk.unitFlying = False
    unitTypeList.append(hydralisk)

    mutalisk = unitType()
    mutalisk.attackType = glaiveWurm
    mutalisk.Name = "Mutalisk"
    mutalisk.Team = "Zerg"
    mutalisk.Image1 = 'Mutalisk1 64x64.bmp'
    mutalisk.Image2 = 'Mutalisk2 64x64.bmp'
    mutalisk.Speed = 3.75
    mutalisk.buildTime = 33
    mutalisk.unitHealth = 120
    mutalisk.unitFlying = True
    unitTypeList.append(mutalisk)

    corruptor = unitType()
    corruptor.attackType = parasiteSpores
    corruptor.Name = "Corruptor"
    corruptor.Team = "Zerg"
    corruptor.Image1 = 'Corruptor1 64x64.bmp'
    corruptor.Image2 = 'Corruptor2 64x64.bmp'
    corruptor.Speed = 2.9531
    corruptor.buildTime = 40
    corruptor.unitHealth = 200
    corruptor.unitFlying = True
    unitTypeList.append(corruptor)
    
    main(animCounter, unitTypeList, attackTypeList, buildingTypeList)
