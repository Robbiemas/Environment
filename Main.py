import pygame
import math
import glob

pygame.init()

screenWidth = 1200
screenHeight = 800
win = pygame.display.set_mode((screenWidth, screenHeight))

# BASE 30
bg = 0, 0, 0
clock = pygame.time.Clock()

# class rotator(int):
#  def init(self, angle):
#    self.angle = angle

#  def angle(self):
#     self.angle += 6
#     self.angle %= 360

class Quark(object):  #Define class/object
    def __init__(self, x, y, angle, vel, radius, width, color, charge):  #method
        self.x = x
        self.y = y
        self.trajectory = []
        self.angle = angle
        self.radius = radius
        self.charge = charge
        self.color = color
        self.width = width
        self.angle %= 360
        self.prevX = 0
        self.prevY = 0
        self.changeinx = 0
        self.changeiny = 0
        self.vel = vel
        self.trajX = 0
        self.trajY = 0
        self.justSpawned = False

    def angleToTrajectory(self, angle):   #method
        self.trajY = -(math.sin(math.radians(self.angle)) * self.vel)
        self.trajX = (math.cos(math.radians(self.angle)) * self.vel)

    def trajectorytoAngle(self, trajX, trajY):
        if self.changeinx < 0:
            self.angle = 180 + math.atan(self.changeiny/self.changeinx)
        if self.changeiny < 0 < self.changeinx:
            self.angle = 360 + math.atan(self.changeiny / self.changeinx)
        if 0 < (self.changeinx and self.changeiny):
            self.angle = math.atan(self.changeiny / self.changeinx)

    def Trajectory(self, trajX, trajY): ## moving dot
        self.x += self.trajX
        self.y += self.trajY

    def changexy(self):
        self.changeinx = self.x - self.prevX
        self.changeiny = self.prevY - self.x
        self.trajectory = [self.changeinx, self.changeiny]

    def draw(self, win):
       # pygame.draw.circle(win, (255, 230, 0), (self.x, self.y), 3)
        pygame.draw.circle(win, self.color, (round(self.x), round(self.y)), self.radius, self.width)









class Breed(object):
    def __init__(self, radius, width, color, charge):
     #   radius = 7
      #  width = 1
      #  color = (255, 140, 0)
      #  charge = 0
        self.radius = radius
        self.width = width
        self.color = color
        self.charge = charge

    def callBreed(self):
        if breedType == "up":
            self.up()
        if breedType == "down":
            self.down()
        if breedType == "electron":
            self.electron()

    def up(self):
        self.radius = 5
        self.width = 0
        self.color = (255, 230, 0)
        self.charge = 20

    def down(self):
        self.radius = 4
        self.width = 0
        self.color = (20, 150, 220)
        self.charge = -10

    def electron(self):
        self.radius = 2
        self.width = 0
        self.color = (255, 140, 0)
        self.charge = -30


def redrawGameWindow():
    win.fill([0, 0, 0])
    for quark in quarkList:
        quark.angleToTrajectory(quark.angle)
        quark.draw(win)
    pygame.display.update()



# mainloop
run = True
quarkList = []
randAngle = 0
flag = False
flag2 = True
rotDeg = 0
startTime = 0
breedType = "up"
picker = Breed(7, 1, (255, 140, 0), 0)



while run:
    clock.tick(60)
    keys = pygame.key.get_pressed()
    print(rotDeg)
    picker.callBreed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if run and not flag:
        rotDeg = 0
        flag = True

    if rotDeg + 1 >= 360:
        rotDeg = 0
    rotDeg += 3

    for quark in quarkList:
        quark.prevX = quark.x  #sets prev x for changeinx
        quark.prevY = quark.y  #sets prev y for changeiny
        if ((screenWidth - quark.radius) > quark.x > quark.radius) and ((screenHeight - quark.radius) > quark.y > quark.radius):
          #  quark.angleToTrajectory(quark.angle)

           # quark.changexy()
            quark.Trajectory(quark.trajX, quark.trajY)  #writes new xy location
        else:

            if quark.y >= (screenHeight - quark.radius):
                quark.angle %= 180
                quark.angle = 180 - quark.angle
                quark.angleToTrajectory(quark.angle)
                quark.Trajectory(quark.trajX, quark.trajY)
            elif quark.y <= (quark.radius):
                quark.angle %= 360
                quark.angle = 360 - quark.angle
                quark.angleToTrajectory(quark.angle)
                quark.Trajectory(quark.trajX, quark.trajY)
            elif quark.x >= (screenWidth - quark.radius):
                quark.angle %= 360
                quark.angle = 180 + (360 - quark.angle)
                quark.angleToTrajectory(quark.angle)
                quark.Trajectory(quark.trajX, quark.trajY)
            elif quark.x <= (quark.radius):
                quark.angle %= 360
                quark.angle = 180 - quark.angle
                quark.angleToTrajectory(quark.angle)
                quark.Trajectory(quark.trajX, quark.trajY)
            else:
                quarkList.pop(quarkList.index(quark))
    # Bounce at angle with vel
    if keys[pygame.K_1]:
        breedType = "up"
    if keys[pygame.K_2]:
        breedType = "down"
    if keys[pygame.K_3]:
        breedType = "electron"

    if keys[pygame.K_SPACE]:
        if flag2:
            startTime = pygame.time.get_ticks()
        #    Quark.angleToTrajectory(quarkList[quark], rotDeg)
            quarkList.append(Quark(round(screenWidth // 2), round(screenHeight // 2), rotDeg, 5, picker.radius, picker.width, picker.color, picker.charge))  ##spawn up but not referenced yet
            flag2 = False

        if not flag2 and ((pygame.time.get_ticks() - startTime) >= 50):
            flag2 = True


    redrawGameWindow()

pygame.quit()