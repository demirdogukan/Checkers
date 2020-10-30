class gameState:
    def __init__(self):
        self.board = [
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["rp", "rp", "rp", "rp", "rp", "rp", "rp", "rp"],
         ["rp", "rp", "rp", "rp", "rp", "rp", "rp", "rp"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
         ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
         ["--", "--", "--", "--", "--", "--", "--", "--"]]
        self.redMove = True
        self.pieceMoveDict = {
                            'p': self.pawn_move,
                            'kn': self.king_move}

    # Update the Game Board
    def make_move(self, Move):
        
        self.board[Move.startRow][Move.startColumn] = '--'
        self.board[Move.endRow][Move.endColumn] = Move.piecesMove

        # remove target
        if abs(Move.startRow - Move.endRow) == 2 or abs(Move.startColumn - Move.endColumn) == 2:
            self.removeTarget(Move)
        else:
            self.redMove = not self.redMove

        if Move.isPawnPromoted():
            Move.promotePawn()
            print("Pawn Promoted.........")
        
        print("Turn : %s"%self.redMove)
        print("(%s, %s) moved to (%s, %s) positions..."%(Move.startRow, Move.startColumn, Move.endRow, Move.endColumn))

    def removeTarget(self, Move):
        targetRow, targetColumn = (Move.startRow + Move.endRow) // 2, (Move.startColumn + Move.endColumn) // 2     
        self.board[targetRow][targetColumn] = '--'
        
    def pawn_move(self, r, c, moves):
        if self.redMove:
            if r + 1 <= 7:
                if self.board[r + 1][c] == 'bp':
                    moves.append(Move((r, c), (r + 2, c), self.board))
                    return

                elif self.board[r + 1][c] == '--':
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    
            if c - 1 >= 0:
                if self.board[r][c - 1] == 'bp':
                    moves.append(Move((r, c), (r, c - 2), self.board))
                    return

                elif self.board[r][c - 1] == '--':
                    moves.append(Move((r, c), (r, c - 1), self.board))
                
            if c + 1 <= 7:
                if self.board[r][c + 1] == 'bp':
                    moves.append(Move((r, c), (r, c + 2), self.board))
                    return
                elif self.board[r][c + 1] == '--':
                    moves.append(Move((r, c), (r, c + 1), self.board))
        else:
            if r - 1 >= 0:
                if self.board[r - 1][c] == 'rp':
                    moves.append(Move((r, c), (r - 2, c), self.board))
                    return
                elif self.board[r - 1][c] == '--':
                    moves.append(Move((r, c), (r - 1, c), self.board))

            if c + 1 <= 7:
                if self.board[r][c + 1] == 'rp':
                    moves.append(Move((r, c), (r, c + 2), self.board))
                    return
                elif self.board[r][c + 1] == '--':
                    moves.append(Move((r, c), (r, c + 1), self.board))

            if c - 1 >= 0:
                if self.board[r][c - 1] == 'rp':
                    moves.append(Move((r, c), (r, c - 2), self.board))
                    return
                elif self.board[r][c - 1] == '--':
                    moves.append(Move((r, c), (r, c - 1), self.board))

    def king_move(self, r, c, moves):
        pass

    def checkPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if ((turn == 'r' and self.redMove) or 
                    (turn == 'b' and not self.redMove)):
                    piece = self.board[r][c][1:]
                    self.pieceMoveDict[piece](r, c, moves)
        return moves

class Move:
    def __init__(self, startsq, endsq, board):
        self.startRow, self.startColumn = startsq[0], startsq[1]
        self.endRow, self.endColumn = endsq[0], endsq[1] 
        self.piecesMove = board[self.startRow][self.startColumn]
        self.MoveID = self.startRow * 1000 + self.startColumn * 100 + self.endRow * 10 + self.endColumn
        self.board = board
                             
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.MoveID == other.MoveID
        return False

    def isPawnPromoted(self):
        if (self.piecesMove == 'rp' and self.endRow == 7) or (self.piecesMove == 'bp' and self.endRow == 0):
            return True

    def promotePawn(self):
        self.board[self.endRow][self.endColumn] = 'kn'

    