import pygame
import math
import time
import glob

pygame.init()

screenWidth = 1200
screenHeight = 800
win = pygame.display.set_mode((screenWidth, screenHeight))

# BASE 30
bg = 0, 0, 0
clock = pygame.time.Clock()


def momentum(aMass, bMass, aVel, bVel):
    #         10      2     5     -3
    print(str(aVel) + "  INCOMING VELOCITIES  " + str(bVel))
    GalTransform = -bVel      # == 3                                       | change sign of 2nd velocity for further use
    aVel += GalTransform      # == 5+3 = 8                                 | combine velocities
    V1 = aVel    # 8                                                       | save combined velocities

    aVel = ((aMass - bMass) / (aMass + bMass)) * V1   # 2/3 * 8  = 5.333   | Find % of mass difference over total mass,
#                                                                          | returns a negative value if hitting larger
#                                                                          | mass, and multiplies by the total available
#                                                                          | velocity.
    bVel = ((2 * aMass) / (aMass + bMass)) * V1       # 5/3 * 8  = 13.33   | multiply the mass % of mass a by 2 then
#                                                                          | multiply it by the totaled velocity
#                                                                          | for new velocity of momentum transfer
    print(str(aVel) + "  MID VELOCITIES  " + str(bVel))

    aVel -= GalTransform   # 5.33 - 3 = 2.33                                | add original impact velocity of b
    bVel -= GalTransform   # 13.33 - 3 = 10.33                              | add back original impact velocity of b
    print(str(aMass) + "  Masses  " + str(bMass))
    print(str(aVel) + "  LOOK HERE  " + str(bVel))
    return (aVel, bVel)

#Old function involving rotating the trajectory
'''
def rotate(velocity, angle):
    dist = math.hypot(velocity[0], velocity[1])
    rotatedVelocities = ([(velocity[0] * math.cos(angle) - velocity[1] * math.sin(angle)),
                          (velocity[0] * math.sin(angle) + velocity[1] * math.cos(angle))])
    #x = dist * math.cos(math.radians(angle))

    #y = dist * math.sin(math.radians(angle))


    #rotatedVelocities = ([x, y])
    #rotatedVelocities = ([((math.sqrt((dist**2)-(((math.degrees(math.sin(math.radians(angle)))) * dist) ** 2)))/dist) - ((math.sqrt((dist**2)-(((math.degrees(math.sin(math.radians(angle)))) * dist) ** 2)))/dist),  (math.sqrt((dist**2)-(-math.cos(math.radians(angle)) * dist) ** 2) / dist)])
    return rotatedVelocities


def resolveCollision(particle, otherParticle):
    #radii = particle.radius - otherParticle.radius
    xVelocityDiff = particle.velocity[0] - otherParticle.velocity[0] #+ radii
    yVelocityDiff = particle.velocity[1] - otherParticle.velocity[1] #+ radii
    xDist = abs(otherParticle.index('x') - particle.x)
    yDist = abs(otherParticle.index('y') - particle.y)

    dist = distance(particle.x, particle.y, otherParticle.index('x'), otherParticle.index('y'))

    # Prevent overlap
    #if (dist - (particle.radius + otherParticle.index('radius'))) < 0: #if balls intersect on j in list of balls
    #if (yDist * yVelocityDiff and xDist * xVelocityDiff) >= 0:
    if xVelocityDiff * xDist + yVelocityDiff * yDist <= 0: #and not particle.colliding:  # if both particles meet on x and y
        #if not particle.colliding:

        # hitAngle = findangle(particle.x, particle.y, otherParticle.index('x'), otherParticle.index('y'))
        hitAngle = -math.atan2((otherParticle.index('y')) - particle.y, otherParticle.index('x') - particle.x)
        print("real hit angle: " + str(findangle(particle.x, particle.y, otherParticle.index('x'), otherParticle.index('y'))))
        print("initial velocity: " + str(particle.velocity) + " original angle = " + str(particle.angle))




       # sendAngle = 2 * hitAngle - particle.angle + 180
       # otherSendAngle = 2 * hitAngle - otherParticle.angle + 180
       # otherParticle.angle %= 360
       # particle.angle %= 360
        particle.colliding = True
        otherParticle.colliding = True

        particle.comingback = False
        otherParticle.comingback = False

        # Grab angle between the two colliding particles
     #   hitAngle = findangle(particle.x, particle.y, otherParticle.index('x'), otherParticle.index('y'))
    #    hitAngle %= 360
       # hitAngle = -math.atan2(-otherParticle.index('y') - (-particle.y), otherParticle.index('x') - particle.x)
        print("detect overlap: hit angle = " + str(math.degrees(hitAngle)))
        print("original angles:,   1: " + str(particle.angle) + ",   2: " + str(otherParticle.angle))
        print("vel: 1, " + str(particle.velocity) + " 2, " + str(otherParticle.velocity))
        # Store mass in var for better readability in collision equation
        m1 = particle.mass
        m2 = otherParticle.index('mass')
        print("mass: 1, " + str(m2) + " 2, " + str(m1))

        # Velocity before equation
        # store list of xy velocities
        vel1 = rotate(particle.velocity, hitAngle)
        vel2 = rotate(otherParticle.velocity, hitAngle)
        print("rotated velocity1: " + str(vel1) + " new angle = " + str(math.degrees(math.atan2(vel1[1], vel1[0]))))
        print("rotated velocity2: " + str(vel2) + " new angle = " + str(math.degrees(math.atan2(vel2[1], vel2[0]))))
        # Velocity after 1d collision equation
        #v1 = [(vel1[0] * (m1 - m2) / (m1 + m2) + vel2[0] * 2 * m2 / (m1 + m2)), (vel1[1])]
        #v2 = [(vel2[0] * (m2 - m1) / (m1 + m2) + vel1[0] * 2 * m2 / (m1 + m2)), (vel2[1])]
        v1 = [(((vel1[0] * (m1 - m2)) + (vel2[0] * 2 * m2)) / (m1 + m2)), -(vel1[1])]
        v2 = [(((vel2[0] * (m1 - m2)) + (vel1[0] * 2 * m1)) / (m1 + m2)), -(vel2[1])]
        print(str(v2) + " " + str(v2[1]))
        print("adjusted velocity: " + str(v1) + " new angle = " + str(math.degrees(math.atan2(v1[1], v1[0]))))

        ## after getting new vels, translate back into angle

        # Final velocity after rotating axis back to original location

        vFinal1 = rotate(v1, -hitAngle)
        vFinal2 = rotate(v2, -hitAngle)

        print("final angle before trajToAngle = " + str(math.degrees(math.atan2(vFinal1[1], vFinal1[0]))))

        #Swap particle velocities for realistic bounce effect
        particle.velocity = vFinal1
        otherParticle.velocity = vFinal2
       # sendAngle %= 360
      #  otherSendAngle %= 360
      #  particle.angle = sendAngle
     #   otherParticle.angle = otherSendAngle
       # particle.trajectorytoAngle()
       # otherParticle.trajectorytoAngle()

        travel_distance = math.hypot(particle.velocity[0], particle.velocity[1])
        particle.speed = (travel_distance / ((abs(particle.velocity[0]) / math.cos(math.radians(particle.angle)))))
        travel_distance2 = math.hypot(particle.velocity[0], otherParticle.velocity[1])
        otherParticle.speed = (travel_distance2 / ((abs(otherParticle.velocity[0]) / math.cos(math.radians(otherParticle.angle)))))


        particle.trajectorytoAngle()
        otherParticle.trajectorytoAngle()
        print("partical velo: " + str(particle.velocity) + "vFinal1: " + str(vFinal1) + "final angle = " + str(particle.angle) + " vfinal angle: " + str(math.degrees(math.atan2(vFinal1[1], vFinal1[0]))))

     #   print(str(vFinal1) + " " + str(particle.trajectory[0]))
     #   print(str(vFinal2) + " " + str(otherParticle.trajectory[0]))
     #   print(str(vFinal1) + " " + str(particle.velocity[0]))
    #    print(str(vFinal2) + " " + str(otherParticle.velocity[0]))
    #    print("final angles: 1, " + str(particle.angle) + " 2, " + str(otherParticle.angle))

'''

class Quark(object):  #Define class/object
    def __init__(self, x, y, angle, speed, radius, width, color, charge, mass):  #method
        self.x = x
        self.y = y
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
        self.speed = speed
        self.mass = mass
        self.trajectory = [(math.cos(math.radians(self.angle))), -(math.sin(math.radians(self.angle)))] ## y should be negative to move up
        self.velocity = [self.trajectory[0] * self.speed, self.trajectory[1] * self.speed]
        self.bounce = 'ready'
        self.momentum = [self.velocity[0] * self.mass, self.velocity[1] * self.mass]
        self.flagx = False
        self.flagy = False
        #self.angle = math.degrees(math.tan(self.velocity[1] / self.velocity[0]))

    def setMomentum(self):
        self.velocity = [self.trajectory[0] * self.speed, self.trajectory[1] * self.speed]
        self.momentum = [self.velocity[0] * self.mass, self.velocity[1] * self.mass]

    def checkScreenEdge(self):
        if (((screenWidth - self.radius) < self.x) and not self.flagx) or ((self.x < self.radius) and not self.flagx):
            self.trajectory[0] *= -1
            self.setMomentum()
            self.bounce = 'ready'
            self.trajectorytoAngle()
            self.flagx = True

        if (((screenHeight - self.radius) < self.y) and not self.flagy) or ((self.y < self.radius) and not self.flagy):
            self.trajectory[1] *= -1
            self.setMomentum()
            self.bounce = 'ready'
            self.trajectorytoAngle()
            self.flagy = True

        if screenWidth - self.radius > self.x > self.radius:
            self.flagx = False
        if screenHeight - self.radius > self.y > self.radius:
            self.flagy = False


    def angleToTrajectory(self, angle):   #method
        self.trajectory[1] = -(math.sin(math.radians(self.angle)))
        self.trajectory[0] = (math.cos(math.radians(self.angle)))

    def trajectorytoAngle(self):
        self.angle = math.degrees(-math.atan2(self.momentum[1], self.momentum[0]))
        self.angle %= 360

    def Trajectory(self): ## moving dot
        self.setMomentum()
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def changexy(self):
        self.changeinx = self.x - self.prevX
        self.changeiny = self.prevY - self.x
        self.velocity = [self.changeinx * self.speed, self.changeiny * self.speed]

    def draw(self, win):
        pygame.draw.circle(win, self.color, (round(self.x), round(self.y)), self.radius, self.width)

    def index(self, variable):
        if variable == 'x':
            return float(self.x)
        if variable == 'y':
            return float(self.y)
        if variable == 'radius':
            return int(self.radius)
        if variable == 'trajX':
            return float(self.trajectory[0])
        if variable == 'trajY':
            return float(self.trajectory[1])
        if variable == 'mass':
            return int(self.mass)


class Breed(object):
    def __init__(self, radius, width, color, charge, mass, initialspeed):
        self.radius = radius
        self.width = width
        self.color = color
        self.charge = charge
        self.mass = mass
        self.initalspeed = initialspeed

    def callBreed(self):
        if breedType == "up":
            self.up()
        if breedType == "down":
            self.down()
        if breedType == "electron":
            self.electron()
        if breedType == "lowspeed":
            self.lowspeed()

    def up(self):
        self.radius = 10
        self.width = 0
        self.color = (255, 230, 0)
        self.charge = 20
        self.mass = 2
        self.initialspeed = 5

    def lowspeed(self):
        self.radius = 40
        self.width = 0
        self.color = (255, 230, 0)
        self.charge = 20
        self.mass = 100
        self.initialspeed = 3

    def down(self):
        self.radius = 8
        self.width = 0
        self.color = (20, 150, 220)
        self.charge = -10
        self.mass = 1
        self.initialspeed = 5

    def electron(self):
        self.radius = 2
        self.width = 0
        self.color = (255, 140, 0)
        self.charge = -30
        self.mass = 0.1
        self.initialspeed = 5


def distance(x1, y1, x2, y2):
    xDist = x2 - x1
    yDist = y2 - y1
    return int(math.hypot(xDist, yDist))

'''
def findangle(x1, y1, x2, y2):
    changeinx = x2 - x1
    changeiny = y1 - y2
    if changeinx < 0:
        return 180 + math.degrees(math.atan(changeiny / changeinx))
    if changeiny < 0 < changeinx:
        return 360 + math.degrees(math.atan(changeiny / changeinx))
    if 0 < (changeinx and changeiny):
        return math.degrees(math.atan(changeiny / changeinx))
    if changeiny == 0:
        if changeinx > 0:
            return 0
        else:
            return 180
    if changeinx == 0:
        if changeiny > 0:
            return 90
        else:
            return 270

def findangle180(x1, y1, x2, y2):
    changeinx = x2 - x1
    changeiny = y1 - y2
    if changeinx < 0 < changeiny:
        return math.degrees(math.atan(changeiny / changeinx))
    if (changeinx and changeiny) < 0:
        return math.degrees(math.atan(changeiny / changeinx))
    if changeiny < 0 < changeinx:
        return math.degrees(math.atan(changeiny / changeinx))
    if 0 < (changeinx and changeiny):
        return math.degrees(math.atan(changeiny / changeinx))
    if changeiny == 0:
        if changeinx > 0:
            return 0
        else:
            return 180
    if changeinx == 0:
        if changeiny > 0:
            return 90
        else:
            return 270
'''


def redrawGameWindow():
    win.fill([0, 0, 0])
    for quark in quarkList:
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
picker = Breed(7, 1, (255, 140, 0), 0, 1, 5)
list_length = 0
count = 0
totalMomentumX = 0
totalMomentumY = 0

# Checking momentum tbi
for i in range(list_length - 1):
    totalMomentumX += quarkList[i].momentum[0]
    totalMomentumY += quarkList[i].momentum[1]

while run:
    clock.tick(120)
    count += 1
    keys = pygame.key.get_pressed()
    picker.callBreed()
    time.sleep(0.01)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if run and not flag:
        rotDeg = 0
        flag = True

    if rotDeg + 1 >= 360:
        rotDeg = 0
    rotDeg += 3

    j = 0
    for quark in quarkList:
        quark.prevX = quark.x  #sets prev x for changeinx
        quark.prevY = quark.y  #sets prev y for changeiny
        quark.setMomentum()
        j = 0
        if quark.bounce == 'wait' and count % 3 == 0:
            quark.bounce = 'ready'
        quark.checkScreenEdge()
        if quark.x < -((quark.radius * 2) + 100) or quark.x > screenWidth + (quark.radius * 2) + 100 or quark.y < -((quark.radius * 2) + 100) or quark.y > screenHeight + (quark.radius * 2) + 100:
            list_length -= 1
            quarkList.pop(quarkList.index(quark))
        for j in range(0, list_length - 1):
            dist = distance(quark.x, quark.y, quarkList[j].index('x'),
                                quarkList[j].index('y'))  # distance between ball and ball[j]
            if quark == quarkList[j]:
                continue  # if ball is not == to ball its comparing against
            #if quark.x + quark.radius >= quarkList[j].x - quarkList[j].radius and quark.x - quark.radius <= quarkList[j].x + quarkList[j].radius:
            #   if quark.y + quark.radius >= quarkList[j].y - quarkList[j].radius and quark.y - quark.radius <= quarkList[j].y + quarkList[j].radius:
            if (dist - (quark.radius + quarkList[j].index('radius'))) <= 0: #if balls intersect on j in list of balls
                if quark.bounce == 'ready' or quarkList[j].bounce == 'ready':

                    values = momentum(quark.mass, quarkList[j].mass, quark.velocity[0], quarkList[j].velocity[0])

                    quark.velocity[0] = values[0]
                    quark.bounce = 'wait'
                    quark.flagx = False
                    quark.flagy = False
                    quarkList[j].velocity[0] = values[1]
                    quarkList[j].bounce = 'wait'
                    quarkList[j].flagx = False
                    quarkList[j].flagy = False

                    values = momentum(quark.mass, quarkList[j].mass, -quark.velocity[1], -quarkList[j].velocity[1])

                    quark.velocity[1] = values[0]
                    quarkList[j].velocity[1] = values[1]

                    quark.momentum[0] = quark.velocity[0] * quark.mass
                    quarkList[j].momentum[0] = quarkList[j].velocity[0] * quarkList[j].mass
                    quark.momentum[1] = quark.velocity[1] * quark.mass
                    quarkList[j].momentum[1] = quarkList[j].velocity[1] * quarkList[j].mass

                    quark.angle = math.degrees(math.atan2(quark.momentum[1], quark.momentum[0]))
                    quarkList[j].angle = math.degrees(math.atan2(quarkList[j].momentum[1], quarkList[j].momentum[0]))

                    quark.angleToTrajectory(quark.angle)
                    quarkList[j].angleToTrajectory(quarkList[j].angle)

                    quark.speed = abs((quark.velocity[0]) / (quark.trajectory[0]))
                    quarkList[j].speed = abs((quarkList[j].velocity[0]) / (quarkList[j].trajectory[0]))
                    print("velox 1: " + str(quark.velocity[0]))
                    print("velox 2: " + str(quarkList[j].velocity[0]))
                    print("speed 1: " + str(quark.speed))
                    print("speed 2: " + str(quarkList[j].speed))
            j = -1
        quark.Trajectory()
    totalMomentumX = 0
    totalMomentumY = 0
    for i in range(list_length - 1):
        totalMomentumX += quarkList[i].momentum[0]
        totalMomentumY += quarkList[i].momentum[1]


    if keys[pygame.K_1]:
        breedType = "up"
    if keys[pygame.K_2]:
        breedType = "down"
    if keys[pygame.K_3]:
        breedType = "electron"
    if keys[pygame.K_4]:
        breedType = "lowspeed"

    if keys[pygame.K_SPACE]:
        if flag2:
            startTime = pygame.time.get_ticks()
            quarkList.append(Quark(round(screenWidth // 2), round(screenHeight // 2), rotDeg, picker.initialspeed, picker.radius, picker.width, picker.color, picker.charge, picker.mass))  ##spawn up but not referenced yet
            flag2 = False
            list_length += 1

        if not flag2 and ((pygame.time.get_ticks() - startTime) >= 100):
            flag2 = True


    redrawGameWindow()
pygame.quit()