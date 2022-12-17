#################################################
# TP3
# Your name: Ruoyu Li
# Your andrew id: ruoyuli
#################################################

from cmu_112_graphics import *
import math, random, copy

# reference:
    # sandbox generation: https://www.youtube.com/watch?v=1DALsnWEJYs
    # mouseDragged: https://py.processing.org/reference/mouseDragged.html
    # numpy tutorial: https://numpy.org/doc/stable/user/whatisnumpy.html
    # inspiration - envi-met: https://www.envi-met.com/
    # https://docs.google.com/presentation/d/1SsmOONf97GHCBrZ1yMT-rOy4UAWq7BYd/edit#slide=id.p1
    # https://docs.google.com/presentation/d/18gkNE_-3ag_z3xfobpUDWJu4sxkkFO95Q-PZW5-7uc0/edit#slide=id.p
    # https://docs.google.com/presentation/d/1FcHqXwfMt2devtijqD6-CjzvTMLwaUR83GPQFXiT9M8/edit#slide=id.g11f3652bc27_2_6
    # transparency: https://www.pythonstudio.us/tkinter-reference/canvas-rectangle-objects.html
    # rain intensity classification: https://www.researchgate.net/figure/PAGASA-Rain-Rate-Classification-and-Color-Representation-of-Threshold-Lines-in-the-Rain_tbl1_327650532
    # sandbox simulation: https://www.designboom.com/technology/uc-davis-ar-sandbox-immersive-topographic-visualization-project-05-30-2016/
    # BFS searching: https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/
    # DFS searching: https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/
    # Perlin Noise: https://en.wikipedia.org/wiki/Perlin_noise
    # create terrain by Perlin Noise: https://www.youtube.com/watch?v=IKB1hWWedMk
    # Perlin Noise Parameters: https://github.com/pvigier/perlin-numpy
    # Perlin Noise with Numpy: https://pvigier.github.io/2018/06/13/perlin-noise-numpy.html
    # Perlin Noise algorithm: https://rtouti.github.io/graphics/perlin-noise-algorithm#:~:text=Perlin%20noise%20is%20a%20popular,number%20of%20inputs%20it%20gets.
    # tkinter colors: https://www.reddit.com/r/Tkinter/comments/qcuio3/a_tkinter_color_picker_and_colorblind_simulator/
    # Perlin Noise: https://weber.itn.liu.se/~stegu/simplexnoise/simplexnoise.pdf
    # Perlin Noise: https://adrianb.io/2014/08/09/perlinnoise.html
    # return 2 decimal float: https://pythonguides.com/python-print-2-decimal-places/
    # rain record logo: https://thenounproject.com/icon/file-2016646/
    # sun logo: https://thenounproject.com/icon/sun-4779442/
    # no rain logo: https://thenounproject.com/icon/cloud-677923/
    # light rain logo: https://thenounproject.com/icon/light-rain-464691/
    # moderate rain logo: https://thenounproject.com/icon/light-rain-1057057/
    # heavy rain logo: https://thenounproject.com/icon/heavy-rain-1620844/
    # storm logo: https://thenounproject.com/icon/storm-133039/
    # extreme storm logo: https://thenounproject.com/icon/stormy-weather-4059599/
    # instruction logo: https://thenounproject.com/icon/question-727767/

class Perlin: # Define Perlin Noise by OOP and Perlin Noise Algorithm
    @staticmethod
    def f(x):
            return 6 * x ** 5 - 15 * x ** 4 + 10 * x ** 3

    def __init__(self):
        self.gradient1 = [[None for j in range(5)] for i in range(4)]
        self.gradient2 = [[None for j in range(2)] for i in range(2)]
        self.gradient3 = [[None for j in range(11)] for i in range(6)]
        self.noise1 = [[None for c in range(20)] for r in range(15)]
        self.noise2 = [[None for c in range(20)] for r in range(15)]
        self.noise3 = [[None for c in range(20)] for r in range(15)]
        self.noise = [[None for c in range(20)] for r in range(15)]

    def getGradient(self): # a grid of random gradient vectors
        for i1 in range(4):
            for j1 in range(5):
                gcrNum1 = random.random()
                gcrX1 = math.cos(2 * math.pi * gcrNum1)
                gcrY1 = math.sin(2 * math.pi * gcrNum1)
                self.gradient1[i1][j1] = (gcrX1, gcrY1) # vector length = 1
        for i2 in range(2):
            for j2 in range(2):
                gcrNum2 = random.random()
                gcrX2 = math.cos(2 * math.pi * gcrNum2)
                gcrY2 = math.sin(2 * math.pi * gcrNum2)
                self.gradient2[i2][j2] = (gcrX2, gcrY2) # vector length = 1
        for i3 in range(6):
            for j3 in range(11):
                gcrNum3 = random.random()
                gcrX3 = math.cos(2 * math.pi * gcrNum3)
                gcrY3 = math.sin(2 * math.pi * gcrNum3)
                self.gradient3[i3][j3] = (gcrX3, gcrY3) # vector length = 1
        return self.gradient1, self.gradient2, self.gradient3

    def getNoise(self): # get each value
        self.gradient1, self.gradient2, self.gradient3 = self.getGradient()
        # operation 1 in a 4 * 3 grid
        for i in range(3):
            for j in range(4):
                # create a cell of random gradient w/ 5*5 goal points in it
                g00 = self.gradient1[i][j]
                g10 = self.gradient1[i+1][j]
                g01 = self.gradient1[i][j+1]
                g11 = self.gradient1[i+1][j+1]
                # get each corner point's noise to each point by dot products
                delta1 = 20 // 4
                delta2 = 15 // 3
                for r in range(delta2*i, delta2*(i+1)):
                    for c in range(delta1*j, delta1*(j+1)):
                        u = 1/delta2 * ((r + 1) % delta2)
                        v = 1/delta1 * ((c + 1) % delta1)
                        n00 = g00[0] * u + g00[1] * v
                        n10 = g10[0] * (u - 1) + g10[1] * v
                        n01 = g01[0] * u + g01[1] * (v - 1)
                        n11 = g11[0] * (u - 1) + g11[1] * (v - 1)
                        # get goal point noise by linear interpolate
                        np0 = n00 * (1 - self.f(u)) + n10 * self.f(u)
                        np1 = n01 * (1 - self.f(u)) + n11 * self.f(u)
                        np = np0 * (1 - self.f(v)) + np1 * self.f(v)
                        self.noise1[r][c] = np
        # operation 2 in a 1*1 grid
        g00 = self.gradient2[0][0]
        g10 = self.gradient2[1][0]
        g01 = self.gradient2[0][1]
        g11 = self.gradient2[1][1]
        for r in range(15):
            for c in range(20):
                u = 1/15 * r
                v = 1/20 * c
                n00 = g00[0] * u + g00[1] * v
                n10 = g10[0] * (u - 1) + g10[1] * v
                n01 = g01[0] * u + g01[1] * (v - 1)
                n11 = g11[0] * (u - 1) + g11[1] * (v - 1)
                # get goal point noise by linear interpolate
                np0 = n00 * (1 - self.f(u)) + n10 * self.f(u)
                np1 = n01 * (1 - self.f(u)) + n11 * self.f(u)
                np = np0 * (1 - self.f(v)) + np1 * self.f(v)
                self.noise2[r][c] = np
        # operation 3 in a 10 * 5 grid
        for i in range(5):
            for j in range(10):
                g00 = self.gradient3[i][j]
                g10 = self.gradient3[i+1][j]
                g01 = self.gradient3[i][j+1]
                g11 = self.gradient3[i+1][j+1]
                delta1 = 20 // 10
                delta2 = 15 // 5
                for r in range(delta2*i, delta2*(i+1)):
                    for c in range(delta1*j, delta1*(j+1)):
                        u = 1/delta2 * ((r + 1) % delta2)
                        v = 1/delta1 * ((c + 1) % delta1)
                        n00 = g00[0] * u + g00[1] * v
                        n10 = g10[0] * (u - 1) + g10[1] * v
                        n01 = g01[0] * u + g01[1] * (v - 1)
                        n11 = g11[0] * (u - 1) + g11[1] * (v - 1)
                        # get goal point noise by linear interpolate
                        np0 = n00 * (1 - self.f(u)) + n10 * self.f(u)
                        np1 = n01 * (1 - self.f(u)) + n11 * self.f(u)
                        np = np0 * (1 - self.f(v)) + np1 * self.f(v)
                        self.noise3[r][c] = np
        for r in range(15):
            for c in range(20):
                self.noise[r][c] = 3/16*self.noise1[r][c] \
                                    + 3/4*self.noise2[r][c] \
                                    + 1/16*self.noise3[r][c]
        return self.noise

def appStarted(app):
    app.game = False
    app.flat = False
    app.random = False
    app.flatButtonX = 150
    app.flatButtonY = app.height - 80
    app.randomButtonX = app.width - 150
    app.randomButtonY = app.height - 80
    app.startButtonWidth = 300
    app.startButtonHeight = 100

    app.rows = 15
    app.cols = 20

    # create a board with elevation
    app.elevationBoard = [[0 for c in range(app.cols)] for r in range(app.rows)]

    # create a board with axonX, axonY
    app.axonCellSize = int(525 / app.rows)
    app.initTopRightX = app.width / 2 + 50
    app.initTopRightY = app.height / 7 + 20
    app.topRightX = app.initTopRightX
    app.topRightY = app.initTopRightY
    app.axonAxisBoard = [[None for c in range(app.cols)] \
                        for r in range(app.rows)]
    makeAxonBasicBoard(app)
    app.axonBoard = [[None for c in range(app.cols)] for r in range(app.rows)]
    makeAxonBoard(app)

    # create a top view board
    app.topCellSize = int(200 / app.rows)
    app.margin = 38
    app.rightestX = app.width - app.margin
    app.topestY = app.margin
    app.topBoard = [[None for c in range(app.cols)] for r in range(app.rows)]
    makeTopBoard(app)

    # dList - adjacent points
    app.dList = [(-1, 0), (0, +1), (+1, 0), (0, -1)]

    # regenerate terrain - point
    app.terrainEdit = True
    # regenerate terrain - multi-points
    app.terrainMultiEdit = False
    app.buttonLeftX = 50
    app.buttonLeftY = 40
    app.buttonWidth = 200
    app.buttonHeight = 50
    app.editPoint = dict()

    # set water source point and simulate path & lake
    app.stream = False
    app.referCX = 100
    app.referCY = app.height - 50
    app.waterCR = 10
    app.waterSourcePoint = []
    app.movingX = app.referCX
    app.movingY = app.referCY
    # simulate stream path
    app.streamPath = dict()
    app.axonWaterP = dict()
    app.topWaterP = dict()
    # simulate lake - rising lake & disappearing lake
    app.lakeStartPoint = set()
    app.puddleStartPoint = set()
    app.lakeVolumn = dict()
    app.aLakePoints = dict()
    app.tLakePoints = dict()
    app.dLakeList = [(+1, -1), (+1, 0), (+1, +1), (0, +1), (-1, +1), (-1, 0), 
                    (-1, -1), (0, -1), (+1, -1)]

    app.redoWaterBX = app.rightestX - app.topCellSize * (app.cols - 1) - 45
    app.redoWaterBY = app.topestY + app.topCellSize * app.rows + 260
    app.redoWaterBWidth = 120
    app.redoWaterBHeight = 40
    app.mainMenu = False
    app.mainMenuX = app.redoWaterBX + 60
    app.mainMenuY = app.height - 75
    app.mainMenuWidth = 120
    app.mainMenuHeight = 40
    app.classification = False
    app.classBX = app.redoWaterBX
    app.classBY = app.redoWaterBY + app.redoWaterBHeight + 20
    app.colorList = ['#009a9c', '#17b79c', '#67d294', '#abeb88', '#f3ff82']
    app.classiElev = dict()

    # adjust rain intensity
    app.rain = False
    app.rainPause = False
    app.barLeftX = app.width / 3 + 180
    app.barLeftY = app.height - 50
    app.rainButtonCX = app.barLeftX
    app.rainButtonCY = app.barLeftY
    app.rainButtonWidth = 10
    app.rainButtonHeight = 20
    app.barWidth = 200
    app.barScale = []
    getRainBarScale(app)
    app.rainAdjust = False
    app.prevRainIntensity = 0
    app.currRainIntensity = 0

    # rain report
    app.intensityRecord = []
    app.recordButtonX = 100
    app.recordButtonY = 150
    app.recordOpen = False
    app.floodedRatio = 0
    # rain record logo: https://thenounproject.com/icon/file-2016646/
    app.initRainRecord = app.loadImage('rainRecordLogo.png')
    app.scaledRainRecord = app.scaleImage(app.initRainRecord, 1/13)
    
    # logo for different rain intensity
    # sun logo: https://thenounproject.com/icon/sun-4779442/
    app.initSun = app.loadImage('sunLogo.png')
    app.scaledSun = app.scaleImage(app.initSun, 1/6)
    # cloud logo: https://thenounproject.com/icon/cloud-677923/
    app.initCloud = app.loadImage('cloudLogo.png')
    app.scaledCloud = app.scaleImage(app.initCloud, 1/5)
    # light rain logo: https://thenounproject.com/icon/light-rain-464691/
    app.initLightRain = app.loadImage('lightRainLogo.png')
    app.scaledLightRain = app.scaleImage(app.initLightRain, 1/5)
    # moderate rain logo: https://thenounproject.com/icon/light-rain-1057057/
    app.initModerateRain = app.loadImage('moderateRainLogo.png')
    app.scaledModerateRain = app.scaleImage(app.initModerateRain, 1/6)
    # heavy rain logo: https://thenounproject.com/icon/heavy-rain-1620844/
    app.initHeavyRain = app.loadImage('heavyRainLogo.png')
    app.scaledHeavyRain = app.scaleImage(app.initHeavyRain, 1/5)
    # storm logo: https://thenounproject.com/icon/storm-133039/
    app.initStorm = app.loadImage('stormLogo.png')
    app.scaledStorm = app.scaleImage(app.initStorm, 1/6)
    # extreme storm logo: https://thenounproject.com/icon/stormy-weather-4059599/
    app.initExtremeStorm = app.loadImage('extremeStormLogo.png')
    app.scaledExtremeStorm = app.scaleImage(app.initExtremeStorm, 1/5)  

    app.initCapture= app.loadImage('imageForCover.png')
    app.scaledCapture = app.scaleImage(app.initCapture, 2/5)

    # instruction
    app.instruction = False
    app.instructCX = app.recordButtonX + 25
    app.instructCY = app.recordButtonY + 65
    app.instructCR = 20

    # set timer interval
    app.initTimerDelay = 1024
    app.timerDelay = app.initTimerDelay
    app.streamTimer = 0
    app.lakeTimer = 0
    app.lakeScale = 1
    app.waterTimer = 0
    app.rainTimer = 0

def makeAxonBasicBoard(app):
    for r in range(app.rows):
        for c in range(app.cols):
            topRightX = app.topRightX+r*app.axonCellSize*math.sin(math.pi/3)
            topRightY = app.topRightY+r*app.axonCellSize*math.cos(math.pi/3)
            x0 = topRightX - c * app.axonCellSize * math.sin(math.pi/3)
            y0 = topRightY + c * app.axonCellSize * math.cos(math.pi/3) 
            app.axonAxisBoard[r][c] = (x0, y0)

def makeAxonBoard(app): #make a axon board by vertices
    for r in range(app.rows):
        for c in range(app.cols):
            x0, y0 = app.axonAxisBoard[r][c]
            x = x0
            y = y0 - app.elevationBoard[r][c]
            app.axonBoard[r][c] = (x, y)

def makeTopBoard(app): # make a top view board by vertices
    for r in range(app.rows):
        for c in range(app.cols):
            x = app.rightestX - c * app.topCellSize
            y = app.topestY + r * app.topCellSize
            app.topBoard[r][c] = (x, y)

def getRainBarScale(app):
    for i in range(6):
        x = app.barLeftX + i * app.barWidth / 5
        y = app.barLeftY
        app.barScale.append((x, y))

def keyPressed(app, event): # set water source & rain
    if (app.game): 
        if (event.key == 'q'):
            app.instruction = not app.instruction
        if (event.key == 's'):
            app.saveSnapshot()
        if (app.random and event.key == 't'):
            app.topRightX = app.initTopRightX
            app.topRightY = app.initTopRightY
            createRandomTerrain(app)
            makeAxonBasicBoard(app)
            makeAxonBoard(app)
        if (event.key == 'w'):
            app.terrainEdit = not app.terrainEdit
            app.stream = not app.stream
        if (event.key == 'r' and app.recordOpen == False):
            app.rain = not app.rain
            if (app.rain):
                app.currRainIntensity = app.prevRainIntensity
                app.timerDelay = int(app.initTimerDelay / \
                                (2**app.currRainIntensity))
            else:
                app.prevRainIntensity = app.currRainIntensity
                app.currRainIntensity = 0
                app.timerDelay = app.initTimerDelay
        if (event.key == 'Right' and app.rain):
            # adjust rainIntensity by 50 - change timerDelay and intensity
            if (app.currRainIntensity +1 <= 5):
                app.currRainIntensity += 1
                app.timerDelay = int(app.timerDelay / 2)
                app.rainButtonCX += (app.barWidth / 5)
                if (app.currRainIntensity != 0):
                    index = app.currRainIntensity
                    app.intensityRecord.append((index, 0))
            else:
                app.currRainIntensity = 5
            app.prevRainIntensity = app.currRainIntensity
        if (event.key == 'Left' and app.rain):
            # adjust rainIntensity by 50 - change timerDelay and intensity
            if (app.currRainIntensity -1 >= 0):
                app.currRainIntensity -= 1
                app.timerDelay *= 2
                app.rainButtonCX -= (app.barWidth / 5)
                if (app.currRainIntensity != 0):
                    index = app.currRainIntensity
                    app.intensityRecord.append((index, 0))
            else:
                app.currRainIntensity = 0
            app.prevRainIntensity = app.currRainIntensity

def nearDots(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 <= 8

def findNearestDot(app, x, y):
    for r in range(app.rows):
        for c in range(app.cols):
            boardX, boardY = app.axonBoard[r][c]
            if (nearDots(x, y, boardX, boardY)):
                return (r, c)
    return None

def isInTheDot(x, y, x0, y0, r0):
    return (((x - x0) ** 2 + (y - y0) ** 2) ** 0.5 <= r0)

def isInMultiEditButton(app, x, y):
    return (app.buttonLeftX <= x <= (app.buttonLeftX + app.buttonWidth) and \
            app.buttonLeftY <= y <= (app.buttonLeftY + app.buttonHeight))

def isLegal(app, r, c, drow, dcol):
    rows = len(app.axonBoard)
    cols = len(app.axonBoard[0])
    return (0 <= r+drow < rows and 0 <= c+dcol < cols)

def adjacentPoints(app, r, c, y0, y):
    result = dict()
    for (drow, dcol) in app.dList:
        if isLegal(app, r, c, drow, dcol):
            x1, y1 = app.axonBoard[r+drow][c+dcol]
            y1 += (y - y0) / 2
            app.elevationBoard[r+drow][c+dcol] -= (y - y0) / 2
            result[(r+drow, c+dcol)] = (x1, y1)
    return result

def inTheRainButton(app, x, y):
    return (app.rainButtonCX - app.rainButtonWidth / 2 <= x and 
            x <= app.rainButtonCX + app.rainButtonWidth/2 and 
            app.rainButtonCY - app.rainButtonHeight / 2 <= y and 
            y <= app.rainButtonCY + app.rainButtonHeight / 2)

def nearestScale(app, x0):
    for point in app.barScale:
        x, y = point
        if (0 <= x - x0 <= app.barWidth/10 or 0 <= x0 - x < app.barWidth/10):
            return x

def inTheFlatButton(app, x, y):
    return (app.flatButtonX <= x <= app.flatButtonX + app.startButtonWidth and \
            app.flatButtonY - app.startButtonHeight <= y <= app.flatButtonY)

def inTheRandomButton(app, x, y):
    return (app.randomButtonX-app.startButtonWidth<=x<=app.randomButtonX and \
            app.randomButtonY-app.startButtonHeight<=y<=app.randomButtonY)

def createRandomTerrain(app): # random terrain generation by perlin noise
    perlinBoard = Perlin().getNoise()
    for r in range(app.rows):
        for c in range(app.cols):
            elevation = perlinBoard[r][c] * 250
            app.elevationBoard[r][c] = elevation

def inTheRedoWaterButton(app, x, y):
    return (app.redoWaterBX <= x <= app.redoWaterBX + app.redoWaterBWidth and
            app.redoWaterBY <= y <= app.redoWaterBY + app.redoWaterBHeight)

def inTheMainMenuButton(app, x, y):
    return (app.mainMenuX <= x <= app.mainMenuX+app.mainMenuWidth and 
            app.mainMenuY <= y <= app.mainMenuY+app.mainMenuHeight)

def inTheClassButton(app, x, y):
    return (app.classBX <= x <= app.classBX+40 and
            app.classBY <= y <= app.classBY+40)

def getHighestAndLowestElevation(app):
    s = set()
    for r in range(app.rows):
        for c in range(app.cols):
            elevation = app.elevationBoard[r][c]
            s.add(elevation)
    return (max(s), min(s))

def classifyElevation(app):
    app.classiElev = dict()
    maxE, minE = getHighestAndLowestElevation(app)
    interval = (maxE+1 - minE) / 5
    for r in range(app.rows):
        for c in range(app.cols):
            elevation = app.elevationBoard[r][c]
            for i in range(5):
                if (minE+i*interval <= elevation < minE+(i+1)*interval):
                    app.classiElev[(r, c)] = app.classiElev.get((r, c), i)

def createARelativeCoordinate(app):
    x1, y1 = app.axonBoard[0][0]
    x2, y2 = app.axonBoard[app.rows-1][app.cols-1]
    x0 = (x1 + x2) / 2
    y0 = (y1 + y2) / 2
    for r in range(app.rows):
        for c in range(app.cols):
            x, y = app.axonBoard[r][c]
            vX = x - x0
            vY = y - y0
            app.vAxonBoard[r][c] = (vX, vY)

def restartWaterSimulation(app):
    app.stream = False
    app.waterSourcePoint = []
    app.streamPath = dict()
    app.axonWaterP = dict()
    app.topWaterP = dict()
    app.lakeStartPoint = set()
    app.puddleStartPoint = set()
    app.lakeVolumn = dict()
    app.aLakePoints = dict()
    app.tLakePoints = dict()
    app.rain = False
    app.rainAdjust = False
    app.rainButtonCX = app.barLeftX
    app.currRainIntensity = 0
    app.prevRainIntensity = 0
    app.initTimerDelay = 512
    app.timerDelay = app.initTimerDelay
    app.streamTimer = 0
    app.lakeTimer = 0
    app.lakeScale = 1
    app.waterTimer = 0
    app.rainTimer = 0
    app.intensityRecord = []

def inTheLogo(app, x, y):
    return (app.recordButtonX <= x <= app.recordButtonX+50 and
            app.recordButtonY-25 <= y <= app.recordButtonY+25)

def nearestNum(currNum):
    lowBound = currNum // 1 / 1
    highBound = lowBound + 1
    mid = lowBound + 0.5
    if (lowBound <= currNum <= mid):
        if (abs(currNum - lowBound) < abs(currNum - mid)):
            return lowBound
        else:
            return mid
    else:
        if (abs(currNum - mid) < abs(currNum - highBound)):
            return mid
        else:
            return highBound

def inTheWords(app, x, y):
    return (app.barLeftX-160 <= x <= app.barLeftX-20 and 
            app.barLeftY-15 <= y <= app.barLeftY+15)

def inTheInstruction(app, x, y):
    return ((app.instructCX-x)**2+(app.instructCY-y)**2 <= app.instructCR**2)

def mousePressed(app, event): 
    if (not app.game): 
        if inTheFlatButton(app, event.x, event.y):
            app.game = True
            app.flat = True
        elif inTheRandomButton(app, event.x, event.y):
            app.game = True
            app.random = True
            createRandomTerrain(app)
            makeAxonBoard(app)
    else:
        # set water source
        if (isInTheDot(event.x, event.y, app.referCX, app.referCY, \
                        app.waterCR)):
            app.terrainEdit = not app.terrainEdit
            app.stream = not app.stream
        if (app.stream == True):
            if (findNearestDot(app, event.x, event.y) != None):
                r, c = findNearestDot(app, event.x, event.y)
                if ((r, c) not in app.waterSourcePoint):
                    app.waterSourcePoint.append((r, c))
                    app.waterSourcePoint.sort()
                else:
                    app.waterSourcePoint.remove((r, c))
                formStreamPathAndLake(app)
        # multi Edit
        if isInMultiEditButton(app, event.x, event.y):
            app.terrainMultiEdit = not app.terrainMultiEdit
        # terrain edit
        if (app.terrainEdit == True):
            if (findNearestDot(app, event.x, event.y) != None):
                r, c = findNearestDot(app, event.x, event.y)
                currX, currY = app.axonBoard[r][c]
                app.axonBoard[r][c] = (currX, event.y)
                app.editPoint[(r, c)] = (currX, event.y)
        # adjust rainIntensity by 5 class - change timerDelay and intensity
        if (app.rain):
            if (inTheRainButton(app, event.x, event.y)):
                app.prevRainIntensity = app.currRainIntensity
                app.rainButtonCX = event.x
                app.rainAdjust = True
        # classify the elevation
        if (inTheClassButton(app, event.x, event.y)):
            app.classification = not app.classification
            if (app.classification):
                classifyElevation(app)
        # redo all the water simulation
        if (inTheRedoWaterButton(app, event.x, event.y)):
            restartWaterSimulation(app)
        # back to main menu
        if (inTheMainMenuButton(app, event.x, event.y)):
            appStarted(app)
        # get rain record
        if (inTheLogo(app, event.x, event.y)):
            app.recordOpen = not app.recordOpen
            app.rainPause = not app.rainPause
            if (app.rainPause):
                app.prevRainIntensity = app.currRainIntensity
                app.rain = False
            else:
                if (app.prevRainIntensity != 0):
                    app.currRainIntensity = app.prevRainIntensity
                    app.rain = True
        if (inTheWords(app, event.x, event.y) and not app.recordOpen):
            app.rain = not app.rain
        if (inTheInstruction(app, event.x, event.y)):
            app.instruction = not app.instruction 

def mouseDragged(app, event): # drag the point to regenerate the terrain
    if (app.game): 
        for key in app.editPoint:
            r, c = key
            currX, currY = app.axonBoard[r][c]
            app.axonBoard[r][c] = (currX, event.y)
            app.editPoint[(r, c)] = (currX, event.y)
            app.elevationBoard[r][c] -= event.y - currY
            if (app.terrainMultiEdit):
                pointsDict = adjacentPoints(app, r, c, currY, event.y)
                for point in pointsDict:
                    currR, currC = point
                    value = pointsDict[(currR, currC)]
                    x, y = value
                    app.axonBoard[currR][currC] = (x, y)
        # adjust rainIntensity by integer - change timerDealy
        if (app.rain and app.rainAdjust == True):
            if (event.x < app.barLeftX):
                app.rainButtonCX = app.barLeftX
            elif (event.x > app.barLeftX + app.barWidth):
                app.rainButtonCX = app.barLeftX + app.barWidth
            else:
                app.rainButtonCX = nearestScale(app, event.x)

def mouseReleased(app, event):
    if (app.game): 
        if (len(app.editPoint) != 0):
            formStreamPathAndLake(app)
        app.editPoint = {}
        # adjust rainIntensity by integer - change timerDealy
        if (app.rain and app.rainAdjust == True):
            app.currRainIntensity = app.barScale.index((app.rainButtonCX, 
                                                        app.rainButtonCY))
            app.timerDelay = int(app.initTimerDelay/(2**app.currRainIntensity))
            app.rainAdjust = False
            if (app.currRainIntensity != 0 and \
                app.prevRainIntensity != app.currRainIntensity):
                index = app.currRainIntensity
                app.intensityRecord.append((index, 0))

def mouseMoved(app, event): # set water source in the map
    if (app.game):
        if (app.stream):
            app.movingX = event.x
            app.movingY = event.y

def findNextPoints(app, r, c): #find next points
    result = set()
    elevation = app.elevationBoard[r][c]
    for i in range(len(app.dList)):
        drow, dcol = app.dList[i]
        if (isLegal(app, r, c, drow, dcol)):
            newR = r + drow
            newC = c + dcol
            currElevation = app.elevationBoard[newR][newC]
            if (currElevation < elevation):
                result.add((newR, newC))
    return result

def getInitStreamPath(app):
    app.lakeStartPoint = set()
    app.streamPath = dict()
    for initPoint in app.waterSourcePoint:
        r0, c0 = initPoint
        newPoints = findNextPoints(app, r0, c0)
        if (newPoints == set()):
            app.lakeStartPoint.add((r0, c0))
        else:
            app.streamPath[initPoint] = app.streamPath.get(initPoint, newPoints)

def formEachSubstreamPath(app): # substream
    testPath = copy.deepcopy(app.streamPath)
    for prevPoint in testPath:
        pointsSet = testPath[prevPoint]
        for newPoint in pointsSet:
            newR, newC = newPoint
            if newPoint not in app.streamPath:
                newPointsSet = findNextPoints(app, newR, newC)
                if (newPointsSet == set()):
                    app.lakeStartPoint.add(newPoint)
                else:
                    app.streamPath[newPoint] = app.streamPath.get(newPoint, \
                                                                newPointsSet)
    if (len(testPath) < len(app.streamPath)):
        formEachSubstreamPath(app)

def getInitAxonWaterParticle(app):
    app.axonWaterP = dict()
    for startPoint in app.streamPath:
        r1, c1 = startPoint
        x1, y1 = app.axonBoard[r1][c1]
        pointSet = app.streamPath[startPoint]
        for endPoint in pointSet:
            r2, c2 = endPoint
            vector = (r1, c1, r2, c2)
            app.axonWaterP[vector] = app.axonWaterP.get(vector, (x1, y1))

def getInitTopWaterParticle(app):
    app.topWaterP = dict()
    for startPoint in app.streamPath:
        r1, c1 = startPoint
        x1, y1 = app.topBoard[r1][c1]
        pointSet = app.streamPath[startPoint]
        for endPoint in pointSet:
            r2, c2 = endPoint
            vector = (r1, c1, r2, c2)
            app.topWaterP[vector] = app.topWaterP.get(vector, (x1, y1))

def formStreamPathAndLake(app):
    getInitStreamPath(app)
    formEachSubstreamPath(app)
    getLowestPoints(app)
    getInitAxonWaterParticle(app)
    getInitTopWaterParticle(app)
    getEachLakeInitVolumn(app)
    formLake(app)

def isLowestPoint(app, r, c):
    elev0 = app.elevationBoard[r][c]
    for (drow, dcol) in app.dList:
        if isLegal(app, r, c, drow, dcol):
            newR = r + drow
            newC = c + dcol
            newElev = app.elevationBoard[newR][newC]
            if (newElev < elev0):
                return False
    return True

def getLowestPoints(app):
    for r in range(app.rows):
        for c in range(app.cols):
            if (isLowestPoint(app, r, c)):
                app.puddleStartPoint.add((r, c))

def countSourceStreams(app, r, c):
    count = 0
    for point in app.streamPath:
        value = app.streamPath[point]
        if ((r, c) in value):
            count += 1
    return count

def getEachLakeInitVolumn(app):
    for point in app.lakeStartPoint:
        r0, c0 = point
        streamNum = countSourceStreams(app, r0, c0)
        dElevation0 = 2 * streamNum
        app.lakeVolumn[point] = app.lakeVolumn.get(point, dElevation0)

def formLake(app): # form lake on axon board
    app.aLakePoints = dict()
    app.tLakePoints = dict()
    for point in app.lakeVolumn:
        r0, c0 = point
        dElev = app.lakeVolumn[point]
        result = formEachPuddle(app, r0, c0, dElev, dict(), dict())
        if (result != 0):
            aPoints, tPoints = result
            for aPoint in aPoints:
                aValue = aPoints[aPoint]
                app.aLakePoints[aPoint] = app.aLakePoints.get(aPoint, aValue)
            for tPoint in tPoints:
                tValue = tPoints[tPoint]
                app.tLakePoints[tPoint] = app.tLakePoints.get(tPoint, tValue)        

def formEachPuddle(app, r, c, dElev, aPoints, tPoints): # DFS lakeFill
    if ((r, c) in aPoints):
        return 0
    aX0, aY0 = app.axonBoard[r][c]
    tX0, tY0 = app.topBoard[r][c]
    elev0 = app.elevationBoard[r][c]
    aPoints[(r, c)] = aPoints.get((r, c), set())
    tPoints[(r, c)] = tPoints.get((r, c), set())
    for i in range(len(app.dLakeList)-1):
        drow1, dcol1 = app.dLakeList[i]
        drow2, dcol2 = app.dLakeList[i+1]
        if (isLegal(app, r, c, drow1, dcol1) and 
            isLegal(app, r, c, drow2, dcol2)):
            r1 = r + drow1
            c1 = c + dcol1
            r2 = r + drow2
            c2 = c + dcol2
            aX1, aY1 = app.axonBoard[r1][c1]
            tX1, tY1 = app.topBoard[r1][c1]
            elev1 = app.elevationBoard[r1][c1]
            aX2, aY2 = app.axonBoard[r2][c2]
            tX2, tY2 = app.topBoard[r2][c2]
            elev2 = app.elevationBoard[r2][c2]
            if ((elev1 - elev0) <= dElev and (elev2 - elev0) <= dElev):
                aNewResult = (aX1, aY1, aX2, aY2)
                aPoints[(r, c)].add(aNewResult)
                tNewResult = (tX1, tY1, tX2, tY2)
                tPoints[(r, c)].add(tNewResult)
                result1 = formEachPuddle(app, r1, c1, dElev/8, aPoints, tPoints)
                if (result1 != 0):
                    aPoints1, tPoints1 = result1
                    for aPoint in aPoints1:
                        aValue = aPoints1[aPoint]
                        aPoints[aPoint] = aPoints.get(aPoint, aValue)
                    for tPoint in tPoints1:
                        tValue = tPoints1[tPoint]
                        tPoints[tPoint] = tPoints.get(tPoint, tValue)   
                result2 = formEachPuddle(app, r2, c2, dElev/8, aPoints, tPoints)
                if (result2 != 0):
                    aPoints2, tPoints2 = result2
                    for aPoint in aPoints2:
                        aValue = aPoints2[aPoint]
                        aPoints[aPoint] = aPoints.get(aPoint, aValue)
                    for tPoint in tPoints2:
                        tValue = tPoints2[tPoint]
                        tPoints[tPoint] = tPoints.get(tPoint, tValue)
            elif ((elev1 - elev0) <= dElev and (elev2 - elev0) > dElev):
                anewX2 = aX0 + ((aX2 - aX0) * dElev / (elev2 - elev0))
                anewY2 = aY0 + ((aY2 - aY0) * dElev / (elev2 - elev0))
                aNewResult = (aX1, aY1, anewX2, anewY2)
                aPoints[(r, c)].add(aNewResult)
                tnewX2 = tX0 + ((tX2 - tX0) * dElev / (elev2 - elev0))
                tnewY2 = tY0 + ((tY2 - tY0) * dElev / (elev2 - elev0))
                tNewResult = (tX1, tY1, tnewX2, tnewY2)
                tPoints[(r, c)].add(tNewResult)
                result1 = formEachPuddle(app, r1, c1, dElev/8, aPoints, tPoints)
                if (result1 != 0):
                    aPoints1, tPoints1 = result1
                    for aPoint in aPoints1:
                        aValue = aPoints1[aPoint]
                        aPoints[aPoint] = aPoints.get(aPoint, aValue)
                    for tPoint in tPoints1:
                        tValue = tPoints1[tPoint]
                        tPoints[tPoint] = tPoints.get(tPoint, tValue)
            elif ((elev1 - elev0) > dElev and (elev2 - elev0) <= dElev):
                anewX1 = aX0 + ((aX1 - aX0) * dElev / (elev1 - elev0))
                anewY1 = aY0 + ((aY1 - aY0) * dElev / (elev1 - elev0))
                aNewResult = (anewX1, anewY1, aX2, aY2)
                aPoints[(r, c)].add(aNewResult)
                tnewX1 = tX0 + ((tX1 - tX0) * dElev / (elev1 - elev0))
                tnewY1 = tY0 + ((tY1 - tY0) * dElev / (elev1 - elev0))
                tNewResult = (tnewX1, tnewY1, tX2, tY2)
                tPoints[(r, c)].add(tNewResult)
                result2 = formEachPuddle(app, r2, c2, dElev/8, aPoints, tPoints)
                if (result2 != 0):
                    aPoints2, tPoints2 = result2
                    for aPoint in aPoints2:
                        aValue = aPoints2[aPoint]
                        aPoints[aPoint] = aPoints.get(aPoint, aValue)
                    for tPoint in tPoints2:
                        tValue = tPoints2[tPoint]
                        tPoints[tPoint] = tPoints.get(tPoint, tValue)
            else:
                anewX1 = aX0 + ((aX1 - aX0) * dElev / (elev1 - elev0))
                anewY1 = aY0 + ((aY1 - aY0) * dElev / (elev1 - elev0))
                anewX2 = aX0 + ((aX2 - aX0) * dElev / (elev2 - elev0))
                anewY2 = aY0 + ((aY2 - aY0) * dElev / (elev2 - elev0))
                aNewResult = (anewX1, anewY1, anewX2, anewY2)
                aPoints[(r, c)].add(aNewResult)
                tnewX1 = tX0 + ((tX1 - tX0) * dElev / (elev1 - elev0))
                tnewY1 = tY0 + ((tY1 - tY0) * dElev / (elev1 - elev0))
                tnewX2 = tX0 + ((tX2 - tX0) * dElev / (elev2 - elev0))
                tnewY2 = tY0 + ((tY2 - tY0) * dElev / (elev2 - elev0))
                tNewResult = (tnewX1, tnewY1, tnewX2, tnewY2)
                tPoints[(r, c)].add(tNewResult)
    if (aPoints[(r, c)] == set()):
        del aPoints[(r, c)]
        del tPoints[(r, c)]
        return 0
    return (aPoints, tPoints)

def getFloodedRatio(app):
    ratio = 0
    for key in app.aLakePoints:
        r, c = key
        value = app.aLakePoints[key]
        if (key == (0, 0) or key == (0, app.cols-1) or key == (app.rows-1, 0) \
            or key == (app.rows-1, app.cols-1)):
            ratio += len(value) / 2
        elif (r == 0 or r == app.rows-1 or c == 0 or c == app.cols-1):
            ratio += len(value) / 4
        else:
            ratio += len(value) / 8
    app.floodedRatio = ratio / (app.cols * app.rows) * 100

def timerFired(app): # stream flow and lake formation animation
    # stream water particle animation
    if (app.game):
        if (len(app.waterSourcePoint) > 0):
            app.streamTimer += 1
            for vector in app.axonWaterP:
                r1, c1, r2, c2 = vector
                axonX1, axonY1 = app.axonBoard[r1][c1]
                axonX2, axonY2 = app.axonBoard[r2][c2]
                topX1, topY1 = app.topBoard[r1][c1]
                topX2, topY2 = app.topBoard[r2][c2]
                newGap = (1 / 24) * app.streamTimer
                newAxonX = axonX1 - (axonX1 - axonX2) * newGap
                newAxonY = axonY1 - (axonY1 - axonY2) * newGap
                newTopX = topX1 - (topX1 - topX2) * newGap
                newTopY = topY1 - (topY1 - topY2) * newGap
                app.axonWaterP[vector] = (newAxonX, newAxonY)
                app.topWaterP[vector] = (newTopX, newTopY)
                if ((newAxonX, newAxonY) == (axonX2, axonY2)):
                    getInitAxonWaterParticle(app)
                    getInitTopWaterParticle(app)
                    app.streamTimer = 0
        # lake grows by stream & rain
        if (app.lakeVolumn != dict()): # lake w/ water source grow, others still
            app.waterTimer += 1
            if (app.waterTimer == 10):
                for point in app.lakeStartPoint:
                    app.lakeVolumn[point] += 0.02
                app.waterTimer = 0
        # update lake by rain + new marsh by rain
        if (app.rain and app.rainPause == False):
            if (app.currRainIntensity != 0):
                currIndex, currCount = app.intensityRecord[-1]
                currCount += 1/(2**currIndex)
                app.intensityRecord[-1] = (currIndex, currCount)
                getLowestPoints(app)
                app.rainTimer += 1
                if (app.rainTimer == 10):
                    for point in app.puddleStartPoint:
                        app.lakeVolumn[point] = app.lakeVolumn.get(point, 0)
                        app.lakeVolumn[point] += 0.02
                    app.rainTimer = 0
        formLake(app)
        getFloodedRatio(app)

def drawAxonGridAndLake(app, canvas):
    if (not app.classification):
        for r in range(app.rows-1):
            for c in range(app.cols-1):
                x1, y1 = app.axonBoard[r][c]
                x2, y2 = app.axonBoard[r+1][c]
                x3, y3 = app.axonBoard[r+1][c+1]
                x4, y4 = app.axonBoard[r][c+1]
                canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, 
                                        outline='black', fill='white', 
                                        stipple='gray75', width=0.8)
                if ((r, c) in app.aLakePoints):
                    x0, y0 = app.axonBoard[r][c]
                    pointsSet = app.aLakePoints[(r, c)]
                    for points in pointsSet:
                        x5, y5, x6, y6 = points
                        canvas.create_polygon(x0, y0, x5, y5, x6, y6, 
                                                fill='#c7ebea', width=0)

def drawClassifiedAxonGridAndLake(app, canvas):
    if (app.classification):
        for r in range(app.rows-1):
            for c in range(app.cols-1):
                i = app.classiElev[(r, c)]
                # classify - different color
                x1, y1 = app.axonBoard[r][c]
                x2, y2 = app.axonBoard[r+1][c]
                x3, y3 = app.axonBoard[r+1][c+1]
                x4, y4 = app.axonBoard[r][c+1]
                canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, 
                                        outline='black', fill=app.colorList[i], 
                                        stipple='gray75', width=0.8)
                if ((r, c) in app.aLakePoints):
                    x0, y0 = app.axonBoard[r][c]
                    pointsSet = app.aLakePoints[(r, c)]
                    for points in pointsSet:
                        x5, y5, x6, y6 = points
                        canvas.create_polygon(x0, y0, x5, y5, x6, y6, 
                                                fill='#c7ebea', width=0)

def drawTopGrid(app, canvas):
    for r in range(app.rows-1):
        for c in range(app.cols-1):
            x1, y1 = app.topBoard[r][c]
            x2, y2 = app.topBoard[r+1][c]
            x3, y3 = app.topBoard[r+1][c+1]
            x4, y4 = app.topBoard[r][c+1]
            canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, 
                                    outline='black', fill='white', width=0.3)

def drawClassifiedTopGrid(app, canvas):
    if (app.classification):
        for r in range(app.rows-1):
            for c in range(app.cols-1):
                i = app.classiElev[(r, c)]
                # classify - different color
                x1, y1 = app.topBoard[r][c]
                x2, y2 = app.topBoard[r+1][c]
                x3, y3 = app.topBoard[r+1][c+1]
                x4, y4 = app.topBoard[r][c+1]
                canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, 
                                        outline='black', fill=app.colorList[i], 
                                        stipple='gray75', width=0.8)

def drawMultiEditButton(app, canvas):
    if (app.terrainMultiEdit == False):
        canvas.create_rectangle(app.buttonLeftX, app.buttonLeftY, 
                                app.buttonLeftX+app.buttonWidth, 
                                app.buttonLeftY+app.buttonHeight, 
                                outline='black', fill='khaki', width=4)
        canvas.create_text(app.buttonLeftX+app.buttonWidth/2, 
                            app.buttonLeftY+app.buttonHeight/2, 
                            text='Multi Edit OFF', fill='black', 
                            font='Arial 22')
    else:
        canvas.create_rectangle(app.buttonLeftX, app.buttonLeftY, 
                                app.buttonLeftX+app.buttonWidth, 
                                app.buttonLeftY+app.buttonHeight, 
                                outline='black', fill='light salmon', width=4)
        canvas.create_text(app.buttonLeftX+app.buttonWidth/2, 
                            app.buttonLeftY+app.buttonHeight/2, 
                            text='Multi Edit ON', fill='black', 
                            font='Arial 22')

def drawAxonEditPoint(app, canvas):
    if (len(app.editPoint) > 0):
        for key in app.editPoint:
            r, c = key
            currX, currY = app.axonBoard[r][c]
            canvas.create_oval(currX-4, currY-4, currX+4, currY+4, fill='olive', 
                                width=0)

def drawTopEditPoint(app, canvas): 
    if (len(app.editPoint) > 0):
        for key in app.editPoint:
            r, c = key
            currX, currY = app.topBoard[r][c]
            canvas.create_oval(currX-4, currY-4, currX+4, currY+4, fill='olive', 
                                width=0)

def drawSourceReference(app, canvas): #reference button & text
    canvas.create_oval(app.referCX-app.waterCR, app.referCY-app.waterCR, 
                        app.referCX+app.waterCR, app.referCY+app.waterCR,
                        fill='#4ebfbd', width=0)
    canvas.create_text(app.referCX+2*app.waterCR, app.referCY, 
                        text="Water Source Start Position", 
                        anchor='w', fill='black', font='Arial 21')

def drawMovableDot(app, canvas):
    if (app.stream == True):
        canvas.create_oval(app.movingX-6, app.movingY-6, app.movingX+6, 
                            app.movingY+6, fill='#4ebfbd', width=0)

def drawAxonWaterSource(app, canvas):
    for dot in app.waterSourcePoint:
        r, c = dot
        x, y = app.axonBoard[r][c]
        canvas.create_oval(x-6, y-6, x+6, y+6, fill='#4ebfbd', width=0)

def drawTopWaterSource(app, canvas):
    for dot in app.waterSourcePoint:
        r, c = dot
        x, y = app.topBoard[r][c]
        radius = app.waterCR / 2
        canvas.create_oval(x-radius, y-radius, x+radius, y+radius, 
                            fill='#4ebfbd', width=0)

def drawAxonPaths(app, canvas):
    # draw stream paths
    for point in app.streamPath:
        r0, c0 = point
        x0, y0 = app.axonBoard[r0][c0]
        value = app.streamPath[point]
        for newPoint in value:
            r1, c1 = newPoint
            x1, y1 = app.axonBoard[r1][c1]
            canvas.create_line(x0, y0, x1, y1, fill='#9dd4d3', width=1.25)

def drawTopPaths(app, canvas):
    for point in app.streamPath:
        r0, c0 = point
        x0, y0 = app.topBoard[r0][c0]
        value = app.streamPath[point]
        for newPoint in value:
            r1, c1 = newPoint
            x1, y1 = app.topBoard[r1][c1]
            canvas.create_line(x0, y0, x1, y1, fill='#4ebfbd', width=1.25)

def drawAxonWaterParticle(app, canvas):
    for vector in app.axonWaterP:
        x, y = app.axonWaterP[vector]
        canvas.create_oval(x-3, y-3, x+3, y+3, fill='#4ebfbd', width=0)

def drawTopWaterParticle(app, canvas):
    for vector in app.topWaterP:
        x, y = app.topWaterP[vector]
        canvas.create_oval(x-1.5, y-1.5, x+1.5, y+1.5, fill='#4ebfbd', 
                            width=0)

def drawTopLake(app, canvas):
    for point0 in app.tLakePoints:
        r0, c0 = point0
        x0, y0 = app.topBoard[r0][c0]
        pointsSet = app.tLakePoints[point0]
        for points in pointsSet:
            x1, y1, x2, y2 = points
            canvas.create_polygon(x0, y0, x1, y1, x2, y2, fill='#c7ebea', 
                                    stipple='gray75', width=0)
        for (drow, dcol) in app.dList:
            if isLegal(app, r0, c0, drow, dcol):
                r1 = r0 + drow
                c1 = r0 + dcol
                x1, y1 = app.topBoard[r1][c1]
                canvas.create_polygon(x0, y0, x1, y1, fill='black', width=0.5)

def drawRainReference(app, canvas):
    # draw rain record logo
    canvas.create_rectangle(app.recordButtonX, app.recordButtonY-25, 
                            app.recordButtonX+50, app.recordButtonY+25, 
                            outline='black', fill='azure', width=2)
    canvas.create_image(app.recordButtonX+25, app.recordButtonY, 
                        image=ImageTk.PhotoImage(app.scaledRainRecord))
    canvas.create_text(160, 150, text='Flood Simulation Report', anchor='w', 
                        fill='black', font='Arial 22')
    # draw rain bar and scale
    if (app.rain):
        canvas.create_text(app.barLeftX-20, app.barLeftY, text='Rain Started!',
                            anchor='e', fill='DodgerBlue4', font='Arial 21')
    if (not app.rain):
        canvas.create_text(app.barLeftX-20, app.barLeftY, text='Rain Stopped!',
                            anchor='e', fill='dim gray', font='Arial 21')
    canvas.create_line(app.barLeftX, app.barLeftY, 
                        app.barLeftX+app.barWidth, app.barLeftY, 
                        fill='black', width=2)
    for point in app.barScale:
        cx, cy = point
        canvas.create_line(cx, cy-app.rainButtonHeight/4, cx, 
                            cy+app.rainButtonHeight/4, fill='black', width=2)
    # draw rain button
    canvas.create_rectangle(app.rainButtonCX-app.rainButtonWidth/2, 
                            app.rainButtonCY-app.rainButtonHeight/2, 
                            app.rainButtonCX+app.rainButtonWidth/2, 
                            app.rainButtonCY+app.rainButtonHeight/2,
                            outline='black', fill='white', width=1)
    # draw current rain intensity
    if (app.rain):
        currRainIntensityList = ['No Rain', 'Light Rain', 'Moderate Rain', 
                                'Heavy Rain', 'Storm', 'Extreme Storm']
        currRainName = currRainIntensityList[app.currRainIntensity]
        canvas.create_text(app.barLeftX+app.barWidth+12, app.barLeftY, 
                            text=f'Rain Level: {currRainName}', 
                            anchor='w', fill='black', font='Arial 21')
    else:
        canvas.create_text(app.barLeftX+app.barWidth+12, app.barLeftY, 
                            text='Rain Level: No Rain', 
                            anchor='w', fill='black', font='Arial 21')
        # draw the time for the current intensity and flood fill area ratio
    if (app.recordOpen):
        if (app.intensityRecord != []):
            recordNum = len(app.intensityRecord)
            canvas.create_rectangle(app.width/2-300, 
                                    app.height/2-(recordNum//2*30)-110, 
                                    app.width/2+300, 
                                    app.height/2+(recordNum//2*30)+110,
                                    fill='azure1', outline='black', width=3)
            canvas.create_text(app.width/2-250, 
                                app.height/2-(recordNum//2*30)-70, 
                                text='Rain Record', anchor='w', fill='black', 
                                font='Arial 24')
            j = 0
            for i in range(len(app.intensityRecord)):
                currRainIndex, rainCount = app.intensityRecord[i]
                rainCount = nearestNum(rainCount)
                if (rainCount != 0):
                    currRainIntensityList = ['No Rain', 'Light Rain', 
                                            'Moderate Rain', 'Heavy Rain', 
                                            'Storm', 'Extreme Storm']
                    currRain = currRainIntensityList[currRainIndex]
                    canvas.create_text(app.width/2-250, 
                                        app.height/2-(recordNum//2*30)-20+30*j, 
                                        text=f'''
{currRain} Lasted for {rainCount} Hours!''', anchor='w', fill='black', 
                                        font='Arial 20')
                    j += 1
            # draw flooded area
            ratio = app.floodedRatio
            # return a float with 2 decimal by str.format()
            ratioW2Decimal = "{:.2f}".format(ratio) 
            canvas.create_text(app.width/2-250, 
                                app.height/2+(recordNum//2*30)+70,
                                text=f'''
Currently, {ratioW2Decimal}% Land Has Been Flooded''', anchor='w', 
                                fill='black', font='Arial 24')
        else:
            canvas.create_rectangle(app.width/2-300, 
                                    app.height/2-50, 
                                    app.width/2+300, 
                                    app.height/2+50,
                                    fill='azure1', outline='black', width=3)
            canvas.create_text(app.width/2-250, 
                                app.height/2, text='''It Hasn't Rained!''', 
                                anchor='w', fill='black', 
                                font='Arial 24')

def drawRainImage(app, canvas): 
    #insert image illustrating rain -> storm by currIntensity
    if (not app.rain):
        canvas.create_image(app.width/2-250, 130, 
                            image=ImageTk.PhotoImage(app.scaledSun))
    else:
        if (app.currRainIntensity == 0):
            canvas.create_image(app.width/2-250, 130, 
                            image=ImageTk.PhotoImage(app.scaledCloud))
        elif (app.currRainIntensity == 1):
            canvas.create_image(app.width/2-250, 130, 
                            image=ImageTk.PhotoImage(app.scaledLightRain))
        elif (app.currRainIntensity == 2):
            canvas.create_image(app.width/2-250, 130, 
                            image=ImageTk.PhotoImage(app.scaledModerateRain))
        elif (app.currRainIntensity == 3):
            canvas.create_image(app.width/2-250, 130, 
                            image=ImageTk.PhotoImage(app.scaledHeavyRain))
        elif (app.currRainIntensity == 4):
            canvas.create_image(app.width/2-250, 130, 
                            image=ImageTk.PhotoImage(app.scaledStorm))
        elif (app.currRainIntensity == 5):
            canvas.create_image(app.width/2-250, 130, 
                            image=ImageTk.PhotoImage(app.scaledExtremeStorm))

def drawCover(app, canvas):
    # insert a background image of simulation capture
    canvas.create_image(app.width/2, app.height/2+5, 
                        image=ImageTk.PhotoImage(app.scaledCapture))
    canvas.create_text(app.width/2, 90, 
                        text='Water Simulation With Customized Terrain', 
                        anchor='n', fill='black', font='Nyala 60')
    flatX0 = app.flatButtonX
    flatY0 = app.flatButtonY - app.startButtonHeight
    flatX1 = app.flatButtonX + app.startButtonWidth
    flatY1 = app.flatButtonY
    canvas.create_rectangle(flatX0, flatY0, flatX1, flatY1, outline= 'black', 
                            fill='honeydew2', width=2)
    canvas.create_text(flatX0+app.startButtonHeight/2+4, 
                        flatY0+app.startButtonHeight/2, 
                        anchor='w', text='Flat Terrain Mode', fill='black', 
                        font='Helvetica 25')
    randomX0 = app.randomButtonX - app.startButtonWidth
    randomY0 = app.randomButtonY - app.startButtonHeight
    randomX1 = app.randomButtonX
    randomY1 = app.randomButtonY
    canvas.create_rectangle(randomX0, randomY0, randomX1, randomY1, 
                            outline= 'black', fill='honeydew2', width=2)
    canvas.create_text(randomX0+app.startButtonHeight/2-22, 
                        randomY0+app.startButtonHeight/2, 
                        anchor='w', text='Random Terrain Mode', fill='black', 
                        font='Helvetica 25')
    canvas.create_text(randomX0+app.startButtonHeight/2-22, 
                        randomY0+app.startButtonHeight/2, 
                        anchor='w', text='Random Terrain Mode', fill='black', 
                        font='Helvetica 25')
    canvas.create_text(flatX0+app.startButtonWidth+110, 
                        randomY0+app.startButtonHeight/2+5, 
                        anchor='w', text='Press Either Button to Get Started!', 
                        fill='black', font='Helvetica 25')

def drawElevationClassesLegend(app, canvas):
    # draw classification button
    canvas.create_text(app.classBX+50, app.classBY+20, 
                            text='Classified Elevations', anchor='w', 
                            fill='black', font='Arial 21')
    if (not app.classification):
        canvas.create_rectangle(app.classBX, app.classBY, app.classBX+40, 
                                app.classBY+40, fill='#b6cee0', outline='black', 
                                width=2)
        canvas.create_text(app.classBX+20, app.classBY+20, 
                            text='OFF', fill='black', font='Arial 16')
    else:
        canvas.create_rectangle(app.classBX, app.classBY, app.classBX+40, 
                                app.classBY+40, fill='#cae0b6', outline='black', 
                                width=2)
        canvas.create_text(app.classBX+20, app.classBY+20, 
                            text='ON', fill='black', font='Arial 16')
        # draw legend
        canvas.create_text(app.classBX, app.classBY+70, 
                            text='Lengend', anchor='w', fill='black', 
                            font='Arial 21')
        canvas.create_rectangle(app.classBX, app.classBY+90, app.classBX+50, 
                                app.classBY+110, fill=app.colorList[0], 
                                outline='black', width=1)
        canvas.create_rectangle(app.classBX+50, app.classBY+90, app.classBX+100, 
                                app.classBY+110, fill=app.colorList[1], 
                                outline='black', width=1)
        canvas.create_rectangle(app.classBX+100, app.classBY+90, 
                                app.classBX+150, app.classBY+110, 
                                fill=app.colorList[2], outline='black', width=1)
        canvas.create_rectangle(app.classBX+150, app.classBY+90, 
                                app.classBX+200, app.classBY+110, 
                                fill=app.colorList[3], outline='black', width=1)
        canvas.create_rectangle(app.classBX+200, app.classBY+90, 
                                app.classBX+250, app.classBY+110, 
                                fill=app.colorList[4], outline='black', width=1)
        canvas.create_text(app.classBX, app.classBY+125, 
                            text='Low', anchor='w', fill='black', 
                            font='Arial 16')
        canvas.create_text(app.classBX+250, app.classBY+125, 
                            text='High', anchor='e', fill='black', 
                            font='Arial 16')

def drawInstruction(app, canvas):
    canvas.create_text(160, 215, text='Help', anchor='w', 
                        fill='black', font='Arial 22')
    canvas.create_oval(app.instructCX-app.instructCR, 
                        app.instructCY-app.instructCR, 
                        app.instructCX+app.instructCR, 
                        app.instructCY+app.instructCR, fill='honeydew2', 
                        outline='black', width=3)
    canvas.create_text(app.instructCX, app.instructCY, text='?', fill='black', 
                        font='Helvetica 40')
    if (app.instruction):
        canvas.create_rectangle(app.width/2-300, app.height/2-320, 
                                app.width/2+300, app.height/2+335,
                                fill='honeydew2', outline='black', 
                                width=3)
        canvas.create_text(app.width/2-270, app.height/2-290, 
                            text='''Customize Terrain:''', anchor='w', fill='black', 
                            font='Helvetica 22 bold')
        canvas.create_text(app.width/2-260, app.height/2-290, 
                            text='''
1.Press any vertice and then drag it by z axis. Click the 'Multi Edit  
   OFF' button, then more vertices can be edited at the same time.''', 
                            anchor='nw', fill='black', font='Helvetica 18')
        canvas.create_text(app.width/2-260, app.height/2-245, 
                            text='''
2.In the 'Random Terrain Mode', press 't' to generate a new terrain.''', 
                            anchor='nw', fill='black', font='Helvetica 18')
        canvas.create_text(app.width/2-260, app.height/2-220, 
                            text='''
3.Click the button beside 'Classified Elevations', the terrain will be
   classified by the elevation with a legend.''', anchor='nw', fill='black', 
                            font='Helvetica 18')
        canvas.create_text(app.width/2-270, app.height/2-145, 
                            text='''Simulate Water Features:''', anchor='nw', 
                            fill='black', font='Helvetica 22 bold')
        canvas.create_text(app.width/2-260, app.height/2-135, 
                            text='''
1.Press 'w' or click the circle beside 'Water Source Start Position', 
   then a blue dot will move with the Mouse.''', 
                            anchor='nw', fill='black', font='Helvetica 18')
        canvas.create_text(app.width/2-260, app.height/2-90, 
                            text='''
2.Put the moving blue dot on the vertice to set the desired position 
   of the water source.''', anchor='nw', fill='black', font='Helvetica 18')
        canvas.create_text(app.width/2-260, app.height/2-45, 
                            text='''
3.After putting the water source position, streams and lakes will be 
   formed. The moving dots of streams illustrates the velocity and 
   the direction of streams.''', anchor='nw', fill='black', font='Helvetica 18')
        canvas.create_text(app.width/2-260, app.height/2+20, 
                            text='''
4.Press 'r' or click the words - 'Rain Stopped', the rain simulation
   will take place. Drag the scale bar of 'Rain Level' or press the left
   key or the right key, the rain intensity will be adjusted.''', 
                            anchor='nw', fill='black', font='Helvetica 18')
        canvas.create_text(app.width/2-260, app.height/2+85, 
                            text='''
5.Click the button beside 'Flood Simulation Report', there will pop   
   out a window demonstrating the history of past rain incidents and 
   the current flooded area ratio.''', 
                            anchor='nw', fill='black', font='Helvetica 18')
        canvas.create_text(app.width/2-260, app.height/2+150, 
                            text='''
6.Press 's', an image of the current window will be captured and 
   then saved in the folder.''', 
                            anchor='nw', fill='black', font='Helvetica 18')
        canvas.create_text(app.width/2-260, app.height/2+195, 
                            text='''
7.Click 'Clear All' button, all the data of previous water simulation 
   will be cleared.''', 
                            anchor='nw', fill='black', font='Helvetica 18')
        canvas.create_text(app.width/2-260, app.height/2+240, 
                            text='''
8.Click 'Main Menu' button, you will go back to the main menu.''', 
                            anchor='nw', fill='black', font='Helvetica 18')
        canvas.create_text(app.width/2-260, app.height/2+265, 
                            text='''
Press 'q' or Click '?' Button to Get Instructions''', 
                            anchor='nw', fill='black', font='Helvetica 21 bold')

def drawRedoWaterButton(app, canvas):
    canvas.create_rectangle(app.redoWaterBX, app.redoWaterBY, 
                            app.redoWaterBX+app.redoWaterBWidth, 
                            app.redoWaterBY+app.redoWaterBHeight, 
                            fill='LightSkyBlue4', outline='black', width=2)
    canvas.create_text(app.redoWaterBX+app.redoWaterBWidth/2, 
                        app.redoWaterBY+app.redoWaterBHeight/2, 
                        text='Clear All',
                        fill='white', font='Arial 21')

def drawBackToMainMenuButton(app, canvas):
    canvas.create_rectangle(app.mainMenuX, app.mainMenuY, 
                            app.mainMenuX+app.mainMenuWidth, 
                            app.mainMenuY+app.mainMenuHeight, 
                            fill='honeydew2', outline='black', width=2)
    canvas.create_text(app.mainMenuX+app.mainMenuWidth/2, 
                        app.mainMenuY+app.mainMenuHeight/2, text='Main Menu', 
                        fill='black', font='Arial 18')

def redrawAll(app, canvas):
    if (not app.game):
        drawCover(app, canvas)
    else:
        # draw grid
        drawTopGrid(app, canvas)
        # draw axon grid with height
        drawAxonGridAndLake(app, canvas)
        # draw different geology by elevation
        drawClassifiedAxonGridAndLake(app, canvas)
        drawClassifiedTopGrid(app, canvas)
        # draw elevation legend
        drawElevationClassesLegend(app, canvas)
        # draw multi points edit button
        drawMultiEditButton(app, canvas)
        # draw terrain edit point
        drawAxonEditPoint(app, canvas)
        drawTopEditPoint(app, canvas)
        # draw lake
        drawTopLake(app, canvas)
        # draw water source button, text & points
        drawSourceReference(app, canvas)
        drawMovableDot(app, canvas)
        # draw the routes of stream
        drawAxonPaths(app, canvas)
        drawTopPaths(app, canvas)
        # draw water particle animation
        drawAxonWaterParticle(app, canvas)
        drawTopWaterParticle(app, canvas)
        # draw water source
        drawAxonWaterSource(app, canvas)
        drawTopWaterSource(app, canvas)
        # draw rain reference
        drawRainReference(app, canvas)
        drawRainImage(app, canvas)
        # draw redo the water simulation
        drawRedoWaterButton(app, canvas)
        # draw back to main menu
        drawBackToMainMenuButton(app, canvas)
        # draw instruction
        drawInstruction(app, canvas)


def waterSimulation():
    runApp(width=1500, height=840)

waterSimulation()