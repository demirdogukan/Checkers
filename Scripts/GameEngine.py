class gameState:
    """
        TO DO->
        1- implement is target on the way of the king
        2- update remove target function for king 
    """
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
        self.redPieceTurn = True
        self.pieceMoveDict = {
                            'p': self.pawn_move,
                            'kn': self.king_move}

    # replace the Game Board
    def make_move(self, Move):
        self.board[Move.startRow][Move.startColumn] = '--'
        self.board[Move.endRow][Move.endColumn] = Move.piecesMove

        if Move.piecesMove[1] == 'p': 
            # it's just only for pawn 
            if not self.isTargetCloseToPawn(Move):
                # target must not be nearby
                self.redPieceTurn = not self.redPieceTurn
        elif Move.piecesMove[-1] == 'n':
            self.isTargetCloseToKing(Move)

        if abs(Move.startRow - Move.endRow) == 2 or abs(Move.startColumn - Move.endColumn) == 2:
            self.removeTarget(Move)

        if Move.canPawnPromote():
            if Move.piecesMove[0] == 'r':
                self.redPieceTurn = not self.redPieceTurn
            elif Move.piecesMove[0] == 'b':
                self.redPieceTurn = not self.redPieceTurn
            Move.promotePawn()
            print("Pawn is promoted....", self.redPieceTurn)
        
        print("(%s, %s) moved to (%s, %s) positions..."%(Move.startRow, Move.startColumn, Move.endRow, Move.endColumn))

    def isTargetCloseToPawn(self, Move):
        if self.redPieceTurn:
            if Move.startRow + 1 <= 7 and Move.endRow + 1 <= 7:
                if self.board[Move.startRow + 1][Move.startColumn][0] == 'b' and self.board[Move.endRow + 1][Move.endColumn] != '--':
                    return True
            elif Move.startColumn + 1 <= 7 and Move.startColumn - 1 >= 0:
                if self.board[Move.startRow][Move.startColumn + 1][0] == 'b' or self.board[Move.startRow][Move.startColumn - 1][0] == 'b':
                    return True
        else:
            if Move.startRow - 1 >= 0 and Move.endRow - 1 >= 0:
                if self.board[Move.startRow - 1][Move.startColumn][0] == 'r' and self.board[Move.endRow - 1][Move.endColumn] != '--':
                    return True
            elif Move.startColumn + 1 <= 7 and Move.startColumn - 1 >= 0:
                if self.board[Move.startRow][Move.startColumn + 1][0] == 'r' or self.board[Move.startRow][Move.startColumn - 1][0] == 'r':
                    return True
        return False

    def removeTargetForKing(self, Move):
        pass

    def isTargetCloseToKing(self, Move):
        _directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        for direction in _directions:
            for i in range(1, 8):
                endRow  = Move.startRow + direction[0] * i
                endColumn =  Move.startColumn + direction[1] * i
                if 0 <= endRow <= 7 and 0 <= endColumn <= 7:
                    endPiece = self.board[endRow][endColumn]
                    if self.redPieceTurn:
                        if endPiece[0] == 'b':
                            return True
                    else:
                        if endPiece[0] == 'r':
                           return True 
        return False        

    def removeTarget(self, Move):
        targetRow, targetColumn = (Move.startRow + Move.endRow) // 2, (Move.startColumn + Move.endColumn) // 2     
        self.board[targetRow][targetColumn] = '--'
                    
    def pawn_move(self, r, c, moves):
        if self.redPieceTurn:
            if r + 1 <= 7:
                if self.board[r + 1][c][0] == 'b':
                    moves.append(Move((r, c), (r + 2, c), self.board))
                elif self.board[r + 1][c] == '--':
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    
            if c - 1 >= 0:
                if self.board[r][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r, c - 2), self.board))
                elif self.board[r][c - 1] == '--':
                    moves.append(Move((r, c), (r, c - 1), self.board))
                
            if c + 1 <= 7:
                if self.board[r][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r, c + 2), self.board))
                elif self.board[r][c + 1] == '--':
                    moves.append(Move((r, c), (r, c + 1), self.board))
        else:
            if r - 1 >= 0:
                if self.board[r - 1][c][0] == 'r':
                    moves.append(Move((r, c), (r - 2, c), self.board))
                elif self.board[r - 1][c] == '--':
                    moves.append(Move((r, c), (r - 1, c), self.board))

            if c + 1 <= 7:
                if self.board[r][c + 1][0] == 'r':
                    moves.append(Move((r, c), (r, c + 2), self.board))
                elif self.board[r][c + 1] == '--':
                    moves.append(Move((r, c), (r, c + 1), self.board))

            if c - 1 >= 0:
                if self.board[r][c - 1][0] == 'r':
                    moves.append(Move((r, c), (r, c - 2), self.board))
                elif self.board[r][c - 1] == '--':
                    moves.append(Move((r, c), (r, c - 1), self.board))

    def king_move(self, r, c, moves):
        _directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        for direction in _directions:
            for i in range(1, 8):
                endRow  = r + direction[0] * i
                endColumn = c + direction[1] * i
                if 0 <= endRow <= 7 and 0 <= endColumn <= 7:
                    endPiece = self.board[endRow][endColumn]
                    if endPiece == 'rp':
                        moves.append(Move((r, c), (endRow + 1, endColumn), self.board))
                    elif endPiece == 'bp':
                        moves.append(Move((r, c), (endRow + 1, endColumn), self.board))
                    elif endPiece == '--':
                        moves.append(Move((r, c), (endRow, endColumn), self.board))
                    else:
                        break
                else:
                    break

    def checkPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if ((turn == 'r' and self.redPieceTurn) or 
                    (turn == 'b' and not self.redPieceTurn)):
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

    def canPawnPromote(self):
        if (self.piecesMove == 'rp' and self.endRow == 7) or (self.piecesMove == 'bp' and self.endRow == 0):
            return True

    def promotePawn(self):
        self.board[self.endRow][self.endColumn] = "rkn" if self.piecesMove[0] == 'r' else "bkn"
        

    