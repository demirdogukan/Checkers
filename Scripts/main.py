import pygame as py
from  GameEngine import gameState
from GameEngine import Move

class Game:
    # Private Components
    width, height = 512, 512
    size = 8
    SQ_SIZE = 512 // size
    WIN = py.display.set_mode((width, height))
    run = True
    colors = [py.Color(104, 55, 37), py.Color(200, 158, 106)]
    RED_PIECE = py.transform.scale(py.image.load(f"Assets/red.png"), (SQ_SIZE, SQ_SIZE))
    BLACK_PIECE = py.transform.scale(py.image.load(f"Assets/black.png"), (SQ_SIZE, SQ_SIZE))
    CROWN = py.transform.scale(py.image.load(f"Assets/crown.png"), (32, 32))
    clock = py.time.Clock()
    board_img = py.transform.scale(py.image.load(f"Assets/board2.jpg"), (512, 512))  

    def __init__(self):
        self.gameState = gameState()
        self.validMoves = self.gameState.checkPossibleMoves()
        self.currentClickPositions = ()
        self.clicks_of_player = []
        self.isValidMove = False
        self.Start()

    def Start(self):       
        while self.run:
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.run = False

                elif event.type == py.MOUSEBUTTONDOWN:
                    row, column = self._GetClickposition()

                    if self.currentClickPositions == (row, column):
                        self._ClearMoves()
                    else: # store moves
                        self.currentClickPositions = (row, column)
                        self.clicks_of_player.append(self.currentClickPositions)
    
                    if len(self.clicks_of_player) == 2:
                        _move = Move(self.clicks_of_player[0], self.clicks_of_player[1], self.gameState.board)
                        if _move in self.validMoves:
                            self._makeMove(_move)
                        self._ClearMoves()

            if self.isValidMove:
                self.validMoves = self.gameState.checkPossibleMoves()
                self.isMovingValid = False

            self._Draw()
            self.clock.tick(60)
            py.display.flip()
            
    # Private 
    def _makeMove(self, _move):
        self.isValidMove = True
        self.gameState.make_move(_move)

    def _ClearMoves(self):
        self.clicks_of_player = []
        self.currentClickPositions = ()

    def _GetClickposition(self):
        position = py.mouse.get_pos()
        row = position[1] // self.SQ_SIZE
        column = position[0] // self.SQ_SIZE
        return (row, column)

    def _Draw(self):
        self._DrawBoard()
        self._DrawPiece()
        py.display.update()

    def _DrawBoard(self):
        for r in range(self.size):
            for c in range(self.size):
                color = self.colors[(r + c) % 2]
                py.draw.rect(self.WIN, color, (c * self.SQ_SIZE, r * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))
                
    def _DrawPiece(self):
        for r in range(self.size):
            for c in range(self.size):
                # red pawn, black pawn, red king, black king
                if self.gameState.board[r][c] == "rp":
                    self.WIN.blit(self.RED_PIECE, (c * self.SQ_SIZE, r * self.SQ_SIZE))
                if self.gameState.board[r][c] == "bp":
                    self.WIN.blit(self.BLACK_PIECE, (c * self.SQ_SIZE, r * self.SQ_SIZE))
                if self.gameState.board[r][c] == 'rkn':
                     self.WIN.blit(self.RED_PIECE, (c * self.SQ_SIZE, r * self.SQ_SIZE))
                     self.WIN.blit(self.CROWN, (c * self.SQ_SIZE + 20, r * self.SQ_SIZE + 15))
                if self.gameState.board[r][c] == 'bkn':
                     self.WIN.blit(self.BLACK_PIECE, (c * self.SQ_SIZE, r * self.SQ_SIZE))
                     self.WIN.blit(self.CROWN, (c * self.SQ_SIZE + 20, r * self.SQ_SIZE + 15)) 

if __name__ == "__main__":
    _main = Game()
     