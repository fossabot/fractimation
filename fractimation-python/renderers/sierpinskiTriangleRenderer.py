import numpy
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

class sierpinskiTriangleRenderer(object):
    """Fractal Renderer for Sierpinski Triangle"""

    _width = _height = None
    _eligibleRects = _trianglesCache = None
    _cachePreheated = _trianglesAddedToAxes = False
    _lineWidths = None
    _currentFrameNumber =  None

    def __init__(self, lineWidths, eligibleRects=None):
        self.initialize(lineWidths, eligibleRects)

    def initialize(self, lineWidths, eligibleRects=None):
        self._trianglesCache = { }
        self._trianglesAddedToAxes = False
        self._cachePreheated = False
        self._currentFrameNumber = 1

        self._lineWidths = lineWidths

        if eligibleRects == None:
            eligibleRects = [ rectangleDimensions(0, 0, 1, 1) ]
        self._eligibleRects = eligibleRects

        initialPatches = [ ]
        for eligibleRect in eligibleRects:
            trianglePoints = self.calculateTrianglePoints(eligibleRect)
            newPatch = Polygon(trianglePoints, fill=False, lineWidth=lineWidths[0])
            initialPatches.append(newPatch)

        initialPatchCollection = PatchCollection(initialPatches, True)
        initialPatchCollection.set_visible(False)
        self._trianglesCache.update({ 0 : initialPatchCollection })

    def preheatCache(self, maxIterations):
        if self._cachePreheated:
            return

        for iterationCounter in range(1, maxIterations):
            self.iterate(iterationCounter, lineWidths[iterationCounter])

        self._cachePreheated = True

    def calculateTrianglePoints(self, rectangle):
        halfWidth = rectangle._width * 0.5
        
        trianglePoints = [
                            [ rectangle._x, rectangle._y ],
                            [ rectangle._x + halfWidth, rectangle._y + rectangle._height ],
                            [ rectangle._x + rectangle._width, rectangle._y ]
                         ]
        return trianglePoints

    def calculateSubdivisions(self, rectangle):
        quarterWidth = rectangle._width * 0.25
        halfWidth = rectangle._width * 0.5
        halfHeight = rectangle._height * 0.5

        topSubdivision = rectangleDimensions(rectangle._x + quarterWidth,
                                             rectangle._y + halfHeight,
                                             halfWidth, halfHeight)
        leftSubdivision = rectangleDimensions(rectangle._x,
                                              rectangle._y,
                                              halfWidth, halfHeight)
        rightSubdivision = rectangleDimensions(rectangle._x + halfWidth,
                                               rectangle._y,
                                               halfWidth, halfHeight)

        return [ topSubdivision, leftSubdivision, rightSubdivision ]

    def iterate(self, iterationIndex, lineWidth):
        newEligibleRects = [ ]
        newTrianglePatches = [ ]

        for eligibleRect in self._eligibleRects:
            subdivisions = self.calculateSubdivisions(eligibleRect)

            for newRect in subdivisions:
                trianglePoints = self.calculateTrianglePoints(newRect)
                newPatch = Polygon(trianglePoints, fill=False, lineWidth=lineWidth)
                newTrianglePatches.append(newPatch)

            newEligibleRects.extend(subdivisions)

        iterationPatchCollection = PatchCollection(newTrianglePatches, True)
        iterationPatchCollection.set_visible(False)
        self._trianglesCache.update({ iterationIndex : iterationPatchCollection })

        self._eligibleRects = newEligibleRects
        self._currentFrameNumber = iterationIndex + 1

    def render(self, frameNumber, axes):
        if not self._trianglesAddedToAxes:
            for frameCounter in range(0, len(self._trianglesCache)):
                frameTriangles = self._trianglesCache[frameCounter]
                axes.add_collection(frameTriangles)
            self._trianglesAddedToAxes = True
        
        if not frameNumber in self._trianglesCache:
            for frameCounter in range(self._currentFrameNumber, frameNumber + 1):
                self.iterate(frameCounter, self._lineWidths[frameCounter])

                frameTriangles = self._trianglesCache[frameCounter]
                axes.add_collection(frameTriangles)

        for frameCounter in range(0, len(self._trianglesCache)):
            frameTriangles = self._trianglesCache[frameCounter]
            frameTriangles.set_visible(frameCounter <= frameNumber)

class rectangleDimensions(object):
    _x = _y = None
    _width = _height = None

    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height