import pygame
import random
import math
from collections import Counter
from src.vector_operations import *
# Initialize pygame
pygame.init()

nilVec = Vector(0,0)
pi2 = math.pi * 2

def roundToNearest(x, y):
    return round(x / y) * y

def scaleTuple(input, factor):
    return tuple(element * factor for element in input)

def changeColors(index, type = 0):
    if not hasattr(changeColors, "time"):
        changeColors.time = 0  # Initialize time if it doesn't exist
    
    color_list = list(ballColors[index])
    frequency = 0.1  # Adjust the frequency as needed
    amplitude = 127.5  # Adjust the amplitude as needed
    
    # Update each color component using a sine wave
    color_list[0] = int((math.sin(frequency * changeColors.time) * amplitude + 127.5) % 256)
    color_list[1] = int((math.sin(frequency * changeColors.time + math.pi/2) * amplitude + 127.5) % 256)
    color_list[2] = int((math.sin(frequency * changeColors.time + math.pi) * amplitude + 127.5) % 256)
    
    
    ballColors[index] = tuple(color_list)
    
    if type == 1:    
        endpoint = addVecs(vecScaleN(subVecs(ballPositions[index], circleCenter), circleRadius / dist(ballPositions[index], circleCenter)),circleCenter)
        connectingLines.append([scaleTuple(ballColors[index],0.5),index,vecToTuple(endpoint)])
        # Increment time for the next call
    changeColors.time += 1

def processList(list):
    if not list:
        return None,None,None,None
    counter = Counter(list)

    mostCommon, mostCommonCount = counter.most_common(1)[0]

    leastCommon, leastCommonCount = counter.most_common()[-1]

    return mostCommon, mostCommonCount, leastCommon, leastCommonCount
   
def removeClipping(index):
    pos = ballPositions[i]
    centerDistance = dist(pos, circleCenter)
    if centerDistance >= circleRadius - ballRadius:
        displacement = vecScaleN(divVecs(subVecs(pos,circleCenter),centerDistance),circleRadius - ballRadius)
        ballPositions[index] = addVecs(circleCenter,displacement)  

def lineAngle(line):
    #round to the nearest segment
    angle = vecToEuler(subVecs(tupleToVec(connectingLines[i][2]),circleCenter))
    rounding =  pi2 / (pi2 / math.atan2(lineThickness, circleRadius))
    return roundToNearest(angle["x"],rounding)
  
tick = 0
collisionCount = 0
g = Vector(0,0.098)
def updateBall(pos, vel, index):
    global tick, collisionCount
    centerDistance = dist(pos, circleCenter)
    if tick <= 1:
        vel = vecScaleN(normalize(Vector(random.randint(-10, 10), random.randint(-10, 10))), startingVel)
    vel = addVecs(vel, g)
    if centerDistance >= circleRadius - ballRadius:
        tangent = normalize(subVecs(pos, circleCenter))
        vel = vecScaleN(reflect(vel, tangent),1.01)
        collisionCount += 1
        changeColors(index,1)
    for i in range(len(ballPositions)):
        if dist(ballPositions[i], pos) <= 2 * ballRadius and i != index:
            collisionCount += 1
            # impulse/momentum calculation
            initialVel = vel
            initialAdjacentVel = ballVelocities[i]
            collisionNormal = normalize(subVecs(pos, ballPositions[i]))
            relativeVel = subVecs(initialVel, initialAdjacentVel)
            relativeVelNorm = dotProd(relativeVel, collisionNormal)
            if relativeVelNorm < 0:  # Check if balls are moving towards each other
                impulse = vecScaleN(collisionNormal, -relativeVelNorm)
                initialVel = addVecs(initialVel, impulse)
                initialAdjacentVel = subVecs(initialAdjacentVel, impulse)
                changeColors(index)
            # Update velocities
            vel = initialVel
            ballVelocities[i] = initialAdjacentVel
            break
    tick += 1
    return vel

# Set up the screen
screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Simulation")

# Colors
black = (0, 0, 0)
white = (255,255,255)

#initial speed
startingVel = 10

# Circle parameters
ballRadius = 55
circleCenter = Vector(screenWidth // 2, screenHeight // 2)
circleRadius = (min(screenWidth, screenHeight) // 3) - 2
lineThickness = 2

ballCount = 2
ballPositions = [nilVec] * ballCount
ballVelocities = [nilVec] * ballCount
startingVelocities = [nilVec] * ballCount
ballColors = [nilVec] * ballCount
connectingLines = []

font = pygame.font.SysFont(None, 36)

# Main loop
for i in range(ballCount):
    ballPositions[i] = addVecs(circleCenter,Vector(random.randint(-175,175),0))
    ballColors[i] = (255,0,0)
     
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(black)  # Fill the screen with black color
    lineAngles = []
    for i in range(len(connectingLines)):
        pygame.draw.line(screen,connectingLines[i][0],vecToTuple(ballPositions[connectingLines[i][1]]),connectingLines[i][2],lineThickness)
        lineAngles.append(lineAngle(i))
    for i in range(ballCount):
        ballVelocities[i] = updateBall(ballPositions[i],ballVelocities[i],i)
    
        # update position
        ballPositions[i] = addVecs(ballPositions[i],ballVelocities[i])
        
        #prevent the ball from glitching through the circle
        removeClipping(i)
        
        pygame.draw.circle(screen, ballColors[i], (int(ballPositions[i]["x"]), int(ballPositions[i]["y"])), ballRadius)
        
    pygame.draw.circle(screen, white, (circleCenter['x'], circleCenter['y']), circleRadius, 4)    

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    mostCommonAngle, angleCount1, leastCommonAngle, angleCount2 = processList(lineAngles)
    
    print(f"Most Common: {mostCommonAngle} for {angleCount1} Least Common: {leastCommonAngle} for {angleCount2}")
            
    collisionLabel = font.render(f"Collision Count: {collisionCount}", True, (255, 255, 255))  # Text, antialiasing, color
    
    text_width, text_height = collisionLabel.get_size()
    text_x = (screenWidth - text_width) // 2

    screen.blit(collisionLabel, (text_x, 525))  

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
