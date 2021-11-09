from itertools import chain

class Piece:
    def __init__(self):
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0
        self.front = 0
        self.back = 0
        self.data = ""
    
    def isNextTo(self, piece):
        if self.left == piece.right:
            return 1
        elif self.right == piece.left:
            return 2
        elif self.top == piece.bottom:
            return 3
        elif self.bottom == piece.top:
            return 4
        elif self.front == piece.back:
            return 5
        elif self.back == piece.front:
            return 6
        else:
            return 0

class SubPuzzle:
    def __init__(self, initPiece):
        self.pieces = [[[initPiece]]]
    
    def allPieces(self):
        return chain(self.pieces)
    
    def _getIndex(self, piece):
        b = False
        coords = (-1, -1, -1)
        for z in range(len(self.pieces)):
            for y in range(len(self.pieces)):
                for x in range(len(self.pieces)):
                    if self.pieces[x][y][z] == piece:
                        coords = (x, y, z)
                        b = True
                        break
                if b:
                    break
            if b:
                break
        return coords

    def __findNewSize(self, p1, sub1, p2, sub2, direction):
        positionP1 = sub1._getIndex(p1)
        positionP2 = sub2._getIndex(p2)

        if direction in [1, 2]:
            if direction == 1:
                widthRight = len(sub1.pieces[0][0]) - positionP1[0]
                widthLeft = len(sub2.pieces[0][0]) - (positionP2[0] + 1)
            else:
                widthRight = len(sub2.pieces[0][0]) - positionP2[0]
                widthLeft = len(sub1.pieces[0][0]) - (positionP1[0] + 1)

            width = widthLeft + widthRight
            width = len(sub1.pieces[0][0]) if width < len(sub1.pieces[0][0]) else width
            width = len(sub2.pieces[0][0]) if width < len(sub2.pieces[0][0]) else width
                
            heightBottomP1 = len(sub1.pieces[0]) - (positionP1[1] + 1)
            heightBottomP2 = len(sub2.pieces[0]) - (positionP2[1] + 1)
            heightBottom = heightBottomP1 if heightBottomP2 > heightBottomP2 else heightBottomP2
            heightTopP1 = len(sub1.pieces[0]) - (heightBottomP1 + 1)
            heightTopP2 = len(sub2.pieces[0]) - (heightBottomP2 + 1)
            heightTop = heightTopP1 if heightTopP1 > heightTopP2 else heightTopP2
            height = heightTop + heightBottom + 1

            depthBackP1 = len(sub1.pieces) - (positionP1[2] + 1)
            depthBackP2 = len(sub2.pieces) - (positionP2[2] + 1)
            depthBack = depthBackP1 if depthBackP2 > depthBackP2 else depthBackP2
            depthFront1 = len(sub1.pieces) - (depthBackP1 + 1)
            depthFront1 = len(sub2.pieces) - (depthBackP2 + 1)
            depthFront = depthFront1 if depthFront1 > depthFront1 else depthFront1
            depth = depthFront + depthBack + 1
        match direction:
            case 3:
                pass
            case 4:
                pass
            case 5:
                pass
            case 6:
                pass

        return width, height, depth

    def tryInterlock(self, sub):
        for p1 in self.allPieces():
            for p2 in sub.allPieces():
                isNext = p1.isNextTo(p2)
                if isNext:
                    # Get new dimensions
                    newSize = self.__findNewSize(p1, self.pieces, p2, sub.pieces, isNext)
                    # Trouver la dimension du nouveau tableau en 3D -> Utiliser isNextTo