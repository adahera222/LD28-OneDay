#####  Color Palette by Color Scheme Designer
#####  Palette URL: http://colorschemedesigner.com/#3i51Tw0w0w0w0
#####  Color Space: RGB; 
# *** Primary Color:
# 
#    var. 1 = #009999 = rgb(0,153,153) #Empty
#    var. 2 = #1D7373 = rgb(29,115,115)
#    var. 3 = #006363 = rgb(0,99,99) #Solid
#    var. 4 = #33CCCC = rgb(51,204,204)
#    var. 5 = #5CCCCC = rgb(92,204,204)
# 
# *** Secondary Color A:
# 
#    var. 1 = #1240AB = rgb(18,64,171) #Past player
#    var. 2 = #2A4480 = rgb(42,68,128)
#    var. 3 = #06266F = rgb(6,38,111) #Player
#    var. 4 = #4671D5 = rgb(70,113,213)
#    var. 5 = #6C8CD5 = rgb(108,140,213)
# 
# *** Secondary Color B:
# 
#    var. 1 = #00CC00 = rgb(0,204,0)
#    var. 2 = #269926 = rgb(38,153,38)
#    var. 3 = #008500 = rgb(0,133,0)
#    var. 4 = #39E639 = rgb(57,230,57)
#    var. 5 = #67E667 = rgb(103,230,103)
#####  Generated by Color Scheme Designer (c) Petr Stanicek 2002-2010

import pygame, time, pprint

pygame.display.init()
screen = pygame.display.set_mode((576, 576))
Clock = pygame.time.Clock()

running = True

D_UP = -1
D_DOWN = 1
D_RIGHT = 2
D_LEFT = -2

MAT_SOLID = 1
MAT_EMPTY = 0

COL_SOLID = (0,99,99)
COL_EMPTY = (0,153,153)
COL_PLAYER = (6,38,111)
COL_PPLAYER = (18,64,171)

class World(object):
    def __init__(self,gsize,sp,mh):
        self.gridsize = gsize #Avaliable sizes: 1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24, 32, 36, 48, 64, 72, 96, 144, 192, 288
        self.spawnpoint = sp
        self.grid = []
        for i in xrange(576/gsize):
            self.grid.append([0]*(576/gsize))
        
        self.maxhistory = mh
        self.ticks = 0
    
    def isOpen(self,x,y):
        if x < 0 or x >= len(self.grid) or y < 0 or y >= len(self.grid):
            return False
            
        if self.grid[x][y] == MAT_EMPTY:
            return True
        else:
            return False
    
    def draw(self,surf):
        for x in xrange(len(self.grid)):
            for y in xrange(len(self.grid)):
                if self.grid[x][y] == MAT_SOLID:
                    col = COL_SOLID
                elif self.grid[x][y] == MAT_EMPTY:
                    col = COL_EMPTY
                pygame.draw.rect(surf,col,((x*self.gridsize,y*self.gridsize),(self.gridsize,self.gridsize)))
        
    def tick(self):
        self.ticks += 1

class Player(object):
    def __init__(self, world):
        self.world = world
        self.curpos = world.spawnpoint
        self.history = [self.curpos]
        self.maxhistory = self.world.maxhistory
        self.isShadow = False
    
    def move(self,d):
        nx,ny = self.curpos
        if d == D_UP or d == D_DOWN:
            ny += (d/abs(d))
        elif d == D_RIGHT or d == D_LEFT:
            nx += (d/abs(d))
        
        if not self.world.isOpen(nx,ny):
            return False
        else:
            self.curpos = (nx,ny)
            self.history.append(self.curpos)
            if not self.isShadow and len(self.history)-1 == self.maxhistory:
                self.isShadow = True
                
            return True
    
    def draw(self,surf,iscurrent):
        if iscurrent:
            col = COL_PLAYER
        else:
            col = COL_PPLAYER
        cx,cy = self.curpos
        gs = self.world.gridsize
        pygame.draw.rect(surf,col,((cx*gs,cy*gs),(gs,gs)))
    
    def seek(self, i):
        i = min(len(self.history)-1,max(0,i)) #Constrain
        print i
        self.curpos = self.history[i]
    
    def sync(self):
        if self.isShadow:
            localtick = world.ticks%self.maxhistory
            self.seek(localtick)

world = World(24,(2,2),3)
curplr = Player(world)
players = [curplr]

world.grid[5][4] = MAT_SOLID

def moveCurPlayer(d):
    global curplr, players, world
    move_succeeded = curplr.move(d) 
    if not move_succeeded:
        return False
    
    world.tick()
    pygame.display.set_caption(str(world.ticks))
    
    if curplr.isShadow:
        curplr = Player(world)
        players.append(curplr)
    
    for plr in players:
        plr.sync()
    
    return True

while running:
    Clock.tick(60)
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = False
        
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            running = False
        
        elif event.key == pygame.K_s:
            stime = time.time()
            pygame.image.save(screen, "Screenshot_%d.png" % stime)
            print "Wrote Screenshot_%d.png" % stime
        
        elif event.key == pygame.K_UP:
            moveCurPlayer(D_UP)
        elif event.key == pygame.K_DOWN:
            moveCurPlayer(D_DOWN)
        elif event.key == pygame.K_RIGHT:
            moveCurPlayer(D_RIGHT)
        elif event.key == pygame.K_LEFT:
            moveCurPlayer(D_LEFT)
    
    screen.fill((0,0,0))
    world.draw(screen)
    for plr in players:
        plr.draw(screen,plr is curplr)
    
    pygame.display.update()