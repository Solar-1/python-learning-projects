import math


def Vector(b=0, c=0, e=0):
    return {'x': b, 'y': c, 'z': e}

def vecToTuple(v):
    return (v['x'], v['y'])

def tupleToVec(t):
    return Vector(*t)

nilVec = Vector(0, 0, 0)

def removeNaN(x):
    return 0 if math.isnan(x) or abs(x) == math.inf else x

def clamp(a, b, c):
    return min(max(a, b), c)

def addVecs(A, B):
    return Vector(A['x'] + B['x'], A['y'] + B['y'], A['z'] + B['z'])

def subVecs(A, B):
    return Vector(A['x'] - B['x'], A['y'] - B['y'], A['z'] - B['z'])

def divVecs(A, R):
    return vecScaleN(A, 1/R)

def vecLength(S):
    return (S['x'] ** 2 + S['y'] ** 2 + S['z'] ** 2) ** 0.5

def dist(a, b):
    return vecLength(subVecs(a, b))

def sign(x):
	return -1 if x < 0 else 1

delDict = {}
def deltaVec(vec, id):
    delDict[id] = delDict.get(id, Vector(0, 0, 0))
    out = subVecs(vec, delDict[id])
    delDict[id] = vec
    return out

def smoothVec(targetVec, currentVec, constant):
    return addVecs(vecScaleN(currentVec, 1-constant), vecScaleN(targetVec, constant))

def vecScale(A, B):
    return Vector(A['x'] * B['x'], A['y'] * B['y'], A['z'] * B['z'])

def vecScaleN(A, n):
    return Vector(A['x'] * n, A['y'] * n, A['z'] * n)

def normalize(S):
    length = vecLength(S)
    if length != 0:
        return divVecs(S, length)
    else:
        return S  # Return the zero vector if input vector is zero

def crossProd(a, b):
    return Vector(a['y'] * b['z'] - a['z'] * b['y'], a['z'] * b['x'] - a['x'] * b['z'], a['x'] * b['y'] - a['y'] * b['x'])

def dotProd(a, b):
    return a['x'] * b['x'] + a['y'] * b['y'] + a['z'] * b['z']

def linePlaneIntersection(linePos, lineVec, planePos, planeNormal):
    planePos = planePos or nilVec
    planeDotNormal = dotProd(planeNormal, planePos)
    lineDotNormal = dotProd(planeNormal, linePos)
    lineDotLineVec = dotProd(planeNormal, lineVec)
    
    scaleFactor = (planeDotNormal - lineDotNormal) / lineDotLineVec
    
    scaledLineVec = vecScaleN(lineVec, scaleFactor)
    
    return addVecs(linePos, scaledLineVec)

def reflect(vector, normal):
    projPlane = normal
    tang = projectVectorOnPlane(vector, projPlane)
    ort = subVecs(vector, tang)
    return subVecs(tang, ort)

def projectVectorOnPlane(vec, plane, planePos=None):
    planePos = planePos or nilVec
    return linePlaneIntersection(vec, plane, planePos, plane)

def projectVectorOnLine(vector, lineVector):
    dir = normalize(lineVector)
    return vecScaleN(dir, dotProd(vector, lineVector) / vecLength(lineVector))

def vecFromEuler(yawangle, pitchangle, distance = 1):
     c = distance
     plane = (math.cos(pitchangle) * c)
     return Vector(
         (math.sin(yawangle) * plane),
         (math.cos(yawangle) * plane),
         (math.sin(pitchangle) * c)
     )

def vecToEuler(vec):
 	return Vector(
 		math.acos(normalize(Vector(vec["x"], vec["y"], 0))["y"]) * sign(vec["x"]),
 		math.asin(normalize(vec)["z"]), 
 		0
 	)