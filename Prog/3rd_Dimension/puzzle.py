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
    
    def tryInterlock(self, sub):
        for p1 in self.allPieces():
            for p2 in sub.allPieces():
                if p1.isNextTo(p1):
                    pass # Assembler 2 SubPuzzle (mais ptn c'est chiant wola)