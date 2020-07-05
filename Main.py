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
        self.x += round(self.trajX)
        self.y += round(self.trajY)

    def changexy(self):
        self.changeinx = self.x - self.prevX
        self.changeiny = self.prevY - self.x
        self.trajectory = [self.changeinx, self.changeiny]

    def draw(self, win):
       # pygame.draw.circle(win, (255, 230, 0), (self.x, self.y), 3)
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius, self.width)

    def up(self, radius, width, color, charge):
        self.radius = 5
        self.width = 0
        self.color = (255, 230, 0)
        self.charge = 20

    def down(self, radius, width, color, charge):
        self.radius = 3
        self.width = 0
        self.color = (20, 150, 220)
        self.charge = 20

    def electron(self, radius, width, color, charge):
        self.radius = 2
        self.width = 0
        self.color = (255, 140, 0)
        self.charge = -30


def redrawGameWindow():
    win.fill([0, 0, 0])
    for quark in Quarks:
        quark.angleToTrajectory(quark.angle)
        quark.draw(win)
    pygame.display.update()


# mainloop
run = True
Quarks = []
randAngle = 0
flag = False
flag2 = True
rotDeg = 0
startTime = 0



while run:
    clock.tick(60)
    keys = pygame.key.get_pressed()
    print(rotDeg)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if run and not flag:
        rotDeg = 0
        flag = True

    if rotDeg + 1 >= 360:
        rotDeg = 0
    rotDeg += 3

    for quark in Quarks:
        if ((screenWidth - quark.radius) > quark.x > quark.radius) and ((screenHeight - quark.radius) > quark.y > quark.radius):
          #  quark.angleToTrajectory(quark.angle)
            quark.prevX = quark.x
            quark.prevY = quark.y
           # quark.changexy()
            quark.Trajectory(quark.trajX, quark.trajY)
        else:
            Quarks.pop(Quarks.index(quark))
    # Bounce at angle with vel

    if keys[pygame.K_SPACE]:
        if flag2:
            startTime = pygame.time.get_ticks()
            breed = Quark.up
        #    Quark.angleToTrajectory(Quarks[quark], rotDeg)
            Quarks.append(Quark(round(screenWidth // 2), round(screenHeight // 2), rotDeg, 5, 10, 0, (255, 230, 0), 20))  ##spawn up but not referenced yet
            flag2 = False

        if not flag2 and ((pygame.time.get_ticks() - startTime) >= 50):
            flag2 = True


    redrawGameWindow()

pygame.quit()