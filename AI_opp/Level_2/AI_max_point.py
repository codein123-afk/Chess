import pygame
import random
import numpy
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))
from assets.image_loader import load_piece

board=[["-R","-H","-B","-Q","-K","-B","-H","-R"],
      ["-P","-P","-P","-P","-P","-P","-P","-P"],
      ["0","0","0","0","0","0","0","0"],
      ["0","0","0","0","0","0","0","0"],
      ["0","0","0","0","0","0","0","0"],
      ["0","0","0","0","0","0","0","0"],
      ["P","P","P","P","P","P","P","P"],
      ["R","H","B","Q","K","B","H","R"]]
turn_ai=False
game_over=False
winner=None
result=None
turn="White"
running=True
selected=None
promotion=False
all_possible_move=[]
cord_x= 250
cord_y = 100
width= 140
height= 320
white_king_move=False
black_king_move=False
white_left_rook_move=False
white_right_rook_move=False
black_left_rook_move=False
black_right_rook_move=False
promotion_row=None
promotion_col=None
all_moves=[]


def move(x,y,a,b):
    board[a][b]=board[x][y]
    board[x][y]="0"

def is_white(piece):
    return piece!="0" and piece[0]!="-"

def is_black(piece):
    return piece!="0" and piece[0]=="-"

def same_colour(p1,p2):
    if p1[0]=="-" and p2[0]=="-":
        return True
    if p1[0]!="-" and p2[0]!="-":
        return True
    return False

def path_clear(row_1,col_1,row_2,col_2):
    if row_1==row_2:
        for i in range(min(col_1,col_2)+1,max(col_2,col_1)):
            if board[row_1][i]!="0":
                return False
        return True
    if col_1==col_2:
        for i in range(min(row_1,row_2)+1,max(row_1,row_2)):
            if board[i][col_1]!="0":
                return False
        return True
    if row_1+col_1== row_2+col_2:
        for i in range(min(col_1,col_2)+1,max(col_1,col_2)):
            if board[row_1+col_1-i][i]!="0":
                return False
        return True
    if row_1-col_1==row_2-col_2:
        for i in range(min(col_1,col_2)+1,max(col_1,col_2)):
            if board[row_1-col_1+i][i]!="0":
                return False
        return True
    return False

def legal_move(n,row_1,col_1,row_2,col_2):
    if board[row_2][col_2]!="0":
        return False
    if n=="P":
        if col_2!=col_1:
            return False
        if row_2-row_1==-1:
            return True
        if row_1==6 and row_2==4:
            if board[5][col_1]=="0":
                return True
        return False
    if n=="-P":
        if col_1!=col_2:
            return False
        if row_2-row_1==1:
            return True
        if row_1==1 and row_2==3:
            if board[2][col_1]=="0":
                return True
        return False
    if n=="H" or n=="-H":
        if abs(row_2-row_1)==2 and abs(col_2-col_1)==1:
            return True
        if abs(row_2-row_1)==1 and abs(col_2-col_1)==2:
            return True
        return False
    if n=="B" or n=="-B":
        if row_1-col_1==row_2-col_2 or row_1+col_1==row_2+col_2:
            if path_clear(row_1,col_1,row_2,col_2):
                return True
        return False
    if n=="R" or n=="-R":
        if row_1==row_2 or col_1==col_2:
            if path_clear(row_1,col_1,row_2,col_2):
                return True
        return False
    if n=="Q" or n=="-Q":
        if row_1==row_2 or col_1==col_2 or row_1-col_1==row_2-col_2 or row_1+col_1==row_2+col_2:
            if path_clear(row_1,col_1,row_2,col_2):
                return True
        return False
    if n=="K" or n=="-K":
        if max(abs(row_1-row_2),abs(col_1-col_2))==1:
            return True
        if n=="K" and not check(row_1,col_1,"White")  :
            if (row_1,col_1)==(7,4) and (row_2,col_2)==(7,6):
                if (not white_king_move and not white_right_rook_move and board[7][5]=="0" and board[7][6]=="0" and not check(7,5,"White") and not check(7,6,'White')):
                    return True 
            if (row_1,col_1)==(7,4) and (row_2,col_2)==(7,2):
                if (not white_king_move and not white_left_rook_move and board[7][3]=="0" and board[7][2]=="0" and board[7][1]=="0" and not check(7,3,"White") and not check(7,2,"White")):
                    return True
        if n=="-K" and not check(row_1,col_1,"Black"):
            if (row_1,col_1)==(0,4) and (row_2,col_2)==(0,6):
                if (not black_king_move and not black_right_rook_move and board[0][5]=="0" and board[0][6]=="0") and not check(0,5,"Black") and not check(0,6,"Black"):
                    return True 
            if (row_1,col_1)==(0,4) and (row_2,col_2)==(0,2):
                if (not black_king_move and not black_left_rook_move and board[0][3]=="0" and board[0][2]=="0" and board[0][1]=="0" and not check(0,3,"Black") and not check(0,2,"Black")):
                    return True
        return False


def capture(n,row_1,col_1,row_2,col_2):
    if board[row_2][col_2]=="0":
        return False
    target=board[row_2][col_2]
    piece=board[row_1][col_1]
    if same_colour(piece,target):
        return False
    if n=="P":
        if row_2-row_1==-1 and abs(col_1-col_2)==1:
            return True
        return False
    if n=="-P":
        if row_2-row_1==1 and abs(col_1-col_2)==1:
            return True
        return False
    if n=="H" or n=="-H":
        if abs(row_2-row_1)==2 and abs(col_2-col_1)==1:
            return True
        if abs(row_2-row_1)==1 and abs(col_2-col_1)==2:
            return True
        return False
    if n=="B" or n=="-B":
        if row_1-col_1==row_2-col_2 or row_1+col_1==row_2+col_2:
            if path_clear(row_1,col_1,row_2,col_2):
                return True
        return False
    if n=="R" or n=="-R":
        if row_1==row_2 or col_1==col_2:
            if path_clear(row_1,col_1,row_2,col_2):
                return True
        return False
    if n=="Q" or n=="-Q":
        if row_1==row_2 or col_1==col_2 or row_1-col_1==row_2-col_2 or row_1+col_1==row_2+col_2:
            if path_clear(row_1,col_1,row_2,col_2):
                return True
        return False
    if n=="K" or n=="-K":
        if max(abs(row_1-row_2),abs(col_1-col_2))==1:
            return True
        return False

def all_legel_move(n,row_1,col_1):
    moves=[]
    for i in range(8):
        for j in range(8):
            if legal_move(n,row_1,col_1,i,j):
                piece=board[row_1][col_1]
                target=board[i][j]
                move(row_1,col_1,i,j)
                king_row,king_col=king_position(turn)
                safe=not check(king_row,king_col,turn)
                board[row_1][col_1]=piece
                board[i][j]=target
                if safe:
                    moves.append((i,j))
            if capture(n,row_1,col_1,i,j):
                piece=board[row_1][col_1]
                target=board[i][j]
                move(row_1,col_1,i,j)
                king_row,king_col=king_position(turn)
                safe=not check(king_row,king_col,turn)
                board[row_1][col_1]=piece
                board[i][j]=target
                if safe:
                    moves.append((i,j))
    return moves

def king_position(colour):
    if colour=='White':
        king="K"
    else:
        king="-K"
    for r in range(8):
        for c in range(8):
            if board[r][c]==king:
                return (r,c)

def check(row,col,colour):
    if colour=="Black":
        pawn_moves=[-1,1]
        for i in pawn_moves:
            change_row=row+1
            change_col=col+i
            if 0<=change_row<8 and 0<=change_col <8:
                if board[change_row][change_col]=="P":
                    return True
        knight_moves=[(-2,-1),(-2,1),(2,-1),(2,1),(1,-2),(1,2),(-1,-2),(-1,2)]
        for i,j in knight_moves:
            change_row=row+i
            change_col=col+j
            if 0<=change_row<8 and 0<=change_col <8:
                if board[change_row][change_col]=="H":
                    return True
        r=row-1
        while r>=0:
            piece=board[r][col]
            if piece!="0":
                if piece=="R" or piece=="Q":
                    return True
                break
            r-=1
        r=row+1
        while r<8:
            piece=board[r][col]
            if piece!="0":
                if piece=="R" or piece=="Q":
                    return True
                break
            r+=1
        c=col-1
        while c>=0:
            piece=board[row][c]
            if piece!="0":
                if piece=="R" or piece=="Q":
                    return True
                break
            c-=1
        c=col+1
        while c<8:
            piece=board[row][c]
            if piece!="0":
                if piece=="R" or piece=="Q":
                    return True
                break
            c+=1
        r=row-1
        c=col-1
        while(c>=0 and r>=0):
            piece=board[r][c]
            if piece!="0":
                if piece=="B" or piece=="Q":
                    return True
                break
            c-=1
            r-=1
        r=row+1
        c=col+1
        while(c<8 and r<8):
            piece=board[r][c]
            if piece!="0":
                if piece=="B" or piece=="Q":
                    return True
                break
            c+=1
            r+=1
        r=row-1
        c=col+1
        while(c<8 and r>=0):
            piece=board[r][c]
            if piece!="0":
                if piece=="B" or piece=="Q":
                    return True
                break
            c+=1
            r-=1
        r=row+1
        c=col-1
        while(c>=0 and r<8):
            piece=board[r][c]
            if piece!="0":
                if piece=="B" or piece=="Q":
                    return True
                break
            c-=1
            r+=1
        for change_row in [-1,0,1]:
            for change_col in [-1,0,1]:
                if change_row==0 and change_col==0:
                    continue
                r=row+change_row
                c=col+change_col
                if 0 <= r < 8 and 0 <= c < 8:
                    if board[r][c] == "K":
                        return True
        return False

    if colour=="White":
        pawn_moves=[-1,1]
        for i in pawn_moves:
            change_row=row-1
            change_col=col+i
            if 0<=change_row<8 and 0<=change_col <8:
                if board[change_row][change_col]=="-P":
                    return True
        knight_moves=[(-2,-1),(-2,1),(2,-1),(2,1),(1,-2),(1,2),(-1,-2),(-1,2)]
        for i,j in knight_moves:
            change_row=row+i
            change_col=col+j
            if 0<=change_row<8 and 0<=change_col <8:
                if board[change_row][change_col]=="-H":
                    return True
        r=row-1
        while r>=0:
            piece=board[r][col]
            if piece!="0":
                if piece=="-R" or piece=="-Q":
                    return True
                break
            r-=1
        r=row+1
        while r<8:
            piece=board[r][col]
            if piece!="0":
                if piece=="-R" or piece=="-Q":
                    return True
                break
            r+=1
        c=col-1
        while c>=0:
            piece=board[row][c]
            if piece!="0":
                if piece=="-R" or piece=="-Q":
                    return True
                break
            c-=1
        c=col+1
        while c<8:
            piece=board[row][c]
            if piece!="0":
                if piece=="-R" or piece=="-Q":
                    return True
                break
            c+=1
        r=row-1
        c=col-1
        while(c>=0 and r>=0):
            piece=board[r][c]
            if piece!="0":
                if piece=="-B" or piece=="-Q":
                    return True
                break
            c-=1
            r-=1
        r=row+1
        c=col+1
        while(c<8 and r<8):
            piece=board[r][c]
            if piece!="0":
                if piece=="-B" or piece=="-Q":
                    return True
                break
            c+=1
            r+=1
        r=row-1
        c=col+1
        while(c<8 and r>=0):
            piece=board[r][c]
            if piece!="0":
                if piece=="-B" or piece=="-Q":
                    return True
                break
            c+=1
            r-=1
        r=row+1
        c=col-1
        while(c>=0 and r<8):
            piece=board[r][c]
            if piece!="0":
                if piece=="-B" or piece=="-Q":
                    return True
                break
            c-=1
            r+=1
        for change_row in [-1,0,1]:
            for change_col in [-1,0,1]:
                if change_row==0 and change_col==0:
                    continue
                r=row+change_row
                c=col+change_col
                if 0 <= r < 8 and 0 <= c < 8:
                    if board[r][c] == "-K":
                        return True
        return False

def promotion_menu(turn):
    cord_x= 250
    cord_y = 100
    width= 140
    height= 320
    pygame.draw.rect(screen,(220,220,220),(cord_x,cord_y,width,height))
    pygame.draw.rect(screen,(0,0,0),(cord_x,cord_y,width,height),3)
    promotion_pieces_white=["Q","B","H","R"]
    promotion_pieces_Black=["-Q","-B","-H","-R"]
    if turn=="Black":
        promotion_pieces=promotion_pieces_white
    else:
        promotion_pieces=promotion_pieces_Black
    for i, piece in enumerate(promotion_pieces):
        screen.blit(pieces[piece],(cord_x+30,cord_y+i*80+10))

def restart_game():
    global board
    global game_over
    global winner
    global result
    global turn
    global selected
    global promotion
    global white_king_move
    global black_king_move
    global white_left_rook_move
    global white_right_rook_move
    global black_left_rook_move
    global black_right_rook_move
    global turn_ai

    board=[["-R","-H","-B","-Q","-K","-B","-H","-R"],
      ["-P","-P","-P","-P","-P","-P","-P","-P"],
      ["0","0","0","0","0","0","0","0"],
      ["0","0","0","0","0","0","0","0"],
      ["0","0","0","0","0","0","0","0"],
      ["0","0","0","0","0","0","0","0"],
      ["P","P","P","P","P","P","P","P"],
      ["R","H","B","Q","K","B","H","R"]]
    turn_ai=False
    game_over=False
    winner=None
    result=None
    turn="White"
    running=True
    selected=None
    promotion=False
    all_possible_move=[]
    cord_x= 250
    cord_y = 100
    width= 140
    height= 320
    white_king_move=False
    black_king_move=False
    white_left_rook_move=False
    white_right_rook_move=False
    black_left_rook_move=False
    black_right_rook_move=False

def all_move(turn):
    all_moves=[]
    for i in range(8):
        for j in range(8):
            if turn=="White":
                if board[i][j] in ["P","Q","K","B","R","H"]:
                    moves=[]
                    piece=board[i][j]
                    moves=all_legel_move(piece,i,j)
                    for r,c in moves:
                        all_moves.append((i,j,r,c))
            if turn=="Black":
                if board[i][j] in ["-P","-Q","-K","-B","-R","-H"]:
                    moves=[]
                    piece=board[i][j]
                    moves=all_legel_move(piece,i,j)
                    for r,c in moves:
                        all_moves.append((i,j,r,c))
    return all_moves

def play_move(turn):
    moves=all_move(turn)
    move=random.choice(moves)
    row_1,col_1,row_2,col_2=move
    return (row_1,col_1,row_2,col_2)

def play(first_row,first_col,row,col,turn):
                        global board
                        global game_over
                        global winner
                        global result
                        global selected
                        global promotion
                        global white_king_move
                        global black_king_move
                        global white_left_rook_move
                        global white_right_rook_move
                        global black_left_rook_move
                        global black_right_rook_move
                        global promotion_row
                        global promotion_col

                        target=board[row][col]
                        piece=board[first_row][first_col]
                        capture_piece=board[row][col]
                        if target=="0":
                            if legal_move(board[first_row][first_col],first_row,first_col,row,col):
                                move(first_row,first_col,row,col)
                                if piece=="P" and row==0:
                                    promotion=True
                                    promotion_row=row
                                    promotion_col=col
                                if piece=="-P" and row==7:
                                    promotion=True
                                    promotion_row=row
                                    promotion_col=col
                                if piece=="K":
                                    if first_col==4 and col==6:
                                        board[7][5]="R"
                                        board[7][7]="0"
                                    if first_col==4 and col==2:
                                        board[7][3]="R"
                                        board[7][0]="0"
                                    white_king_move=True
                                if piece=="-K":
                                    if first_col==4 and col==6:
                                        board[0][5]="-R"
                                        board[0][7]="0"
                                    if first_col==4 and col==2:
                                        board[0][3]="-R"
                                        board[0][0]="0"
                                    black_king_move=True
                                if piece=="R" and first_row==7 and first_col==0:
                                    white_left_rook_move=True
                                if piece=="R" and first_row==7 and first_col==7:
                                    white_right_rook_move=True
                                if piece=="-R" and first_row==0 and first_col==0:
                                    black_left_rook_move=True
                                if piece=="-R" and first_row==0 and first_col==7:
                                    black_right_rook_move=True
                                own_king_row,own_king_col=king_position(turn)
                                if check(own_king_row,own_king_col,turn):
                                    print("Your king is checked")
                                    board[first_row][first_col]=piece
                                    board[row][col]=capture_piece
                                    selected=None
                                    return False
                                return True
                        else:
                            if capture(board[first_row][first_col],first_row,first_col,row,col):
                                move(first_row,first_col,row,col)
                                if piece=="P" and row==0:
                                    promotion=True
                                    promotion_row=row
                                    promotion_col=col 
                                if piece=="-P" and row==7:
                                    promotion=True
                                    promotion_row=row
                                    promotion_col=col
                                if capture_piece=="R" and row==7 and col==0:
                                    white_left_rook_move=True
                                if capture_piece=="R" and row==7 and col==7:
                                    white_left_rook_move=True
                                if capture_piece=="-R" and row==0 and col==0:
                                    black_left_rook_move=True
                                if capture_piece=="-R" and row==0 and col==7:
                                    black_right_rook_move=True
                                own_king_row,own_king_col=king_position(turn)
                                if check(own_king_row,own_king_col,turn):
                                    print("Your king is checked")
                                    board[first_row][first_col]=piece
                                    board[row][col]=capture_piece
                                    selected=None
                                    return False
                                return True
                        return False


def evalute(board):
    score=0
    value={"P":1,"H":3,"B":3,"Q":9,"R":5,"K":0,"-P":-1,"-H":-3,"-B":-3,"-Q":-9,"-R":-5,"-K":0}
    for i in range(8):
        for j in range(8):
            if board[i][j]=="0":
                continue
            else:
                score+=value[board[i][j]]
    return score

def best_move(turn):
    moves=all_move(turn)
    if not moves:
        global game_over
        game_over=True
        return None
    first_row=0
    first_col=0
    second_row=0
    second_col=0

    if turn=="White":
        best_score=float("-inf")
    else:
        best_score=float("inf")
    for current_move in moves:
        row_1,col_1,row_2,col_2=current_move
        piece=board[row_1][col_1]
        target=board[row_2][col_2]
        move(row_1,col_1,row_2,col_2)
        score=evalute(board)
        if turn=="White" and score >best_score:
                first_row,first_col,second_row,second_col=row_1,col_1,row_2,col_2
                best_score=score
        if turn=="Black" and score<best_score:
                first_row,first_col,second_row,second_col=row_1,col_1,row_2,col_2
                best_score=score
        board[row_1][col_1]=piece
        board[row_2][col_2]=target
    return (first_row,first_col,second_row,second_col)

def undo_move(row1,col_1,row_2,col_2,capture_piece):
    piece=board[row_2][col_2]
    board[row_1][col_1]=piece
    board[row_2][col_2]=capture_piece


def minimax(depth,turn):
    if depth==0:
        return evalute(board)
    if turn=="White":
            best_score=float("-inf")
            moves_all=all_move(turn)
            for moves in moves_all:
                row_1,col_1,row_2,col_2=moves
                capture_piece=board[row_2][col_2]
                move(row_1,col_1,row_2,col_2)
                score=minimax(depth-1,"Black")
                undo_move(row_1,col_1,row_2,col_2,capture_piece)
                best_score=max(best_score,score)
            return best_score
    if turn=="Black":
            best_score=float("inf")
            moves_all=all_move(turn)
            for moves in moves_all:
                row_1,col_1,row_2,col_2=moves
                capture_piece=board[row_2][col_2]
                move(row_1,col_1,row_2,col_2)
                score=minimax(depth-1,"White")
                undo_move(row_1,col_1,row_2,col_2,capture_piece)
                best_score=min(best_score,score)
            return best_score


    










pygame.init()
WIDTH=HEIGHT=640
SQ_SIZE= WIDTH//8

pieces = {}
pieces["P"]  = load_piece("images/WP.png", SQ_SIZE)
pieces["R"]  = load_piece("images/WR.png", SQ_SIZE)
pieces["H"]  = load_piece("images/WH.png", SQ_SIZE)
pieces["B"]  = load_piece("images/WB.png", SQ_SIZE)
pieces["Q"]  = load_piece("images/WQ.png", SQ_SIZE)
pieces["K"]  = load_piece("images/WK.png", SQ_SIZE)
pieces["-P"] = load_piece("images/BP.png", SQ_SIZE)
pieces["-R"] = load_piece("images/BR.png", SQ_SIZE)
pieces["-H"] = load_piece("images/BH.png", SQ_SIZE)
pieces["-B"] = load_piece("images/BB.png", SQ_SIZE)
pieces["-Q"] = load_piece("images/BQ.png", SQ_SIZE)
pieces["-K"] = load_piece("images/BK.png", SQ_SIZE)

screen=pygame.display.set_mode((WIDTH,HEIGHT))
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)

while running:
    for row in range(8):
        for col in range(8):
            color=WHITE if (row+col)%2==0 else BLACK

            pygame.draw.rect(
                screen,
                color,
                (col * SQ_SIZE,
                 row * SQ_SIZE,
                 SQ_SIZE,
                 SQ_SIZE))
    for row in range(8):
        for col in range(8):
            square=board[row][col]
            if square!="0":
                screen.blit(
                    pieces[square],
                    (col * SQ_SIZE, row * SQ_SIZE))
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif game_over:
            if event.type==pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(pygame.mouse.get_pos()):
                    restart_game()
        else: 
            if event.type==pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                col=x//SQ_SIZE
                row=y//SQ_SIZE
                if selected is None:
                    if board[row][col]!="0":
                        if turn=="White" and is_white(board[row][col]):
                            selected=(row,col)
                            first_1=row
                            first_2=col
                            print("Selected:", selected)
                        if turn=="Black" and is_black(board[row][col]):
                            selected=(row,col)
                            first_1=row
                            first_2=col
                            print("Selected:", selected)
                else:
                    first_row,first_col=selected
                    if (row,col)==selected:
                        selected=None
                        print("Selection Canclled")
                    else:
                        if play(first_row,first_col,row,col,turn):
                            turn="Black" if turn=="White" else "White"
                            selected=None
                            turn_ai=True
    
    if turn_ai and not promotion:
        moves=all_move(turn)
        if len(moves)==0 :
            game_over=True
        else:
            row_1,col_1,row_2,col_2=best_move(turn)
            if play(row_1,col_1,row_2,col_2,turn):
                turn="Black" if turn=="White" else "White"
                selected=None
                turn_ai=False

    if game_over:
        if winner=="White":
            pygame.draw.rect(screen,(0,0,0),(0,200,640,200))
            pygame.draw.rect(screen,(0,0,0),(0,200,640,200),3)
        elif winner=="Black":
            pygame.draw.rect(screen,(255,255,255),(0,200,640,200))
            pygame.draw.rect(screen,(0,0,0),(0,200,640,200),3)
        else:
            pygame.draw.rect(screen,(220,220,220),(0,200,640,200))
            pygame.draw.rect(screen,(0,0,0),(0,200,640,200),3)
        font=pygame.font.SysFont(None,60)
        if result=="CHECKMATE":
            if winner=="White":
                text=font.render(f"{winner} Wins",True,(255,255,255))
                restart=font.render(f"Restart",True,(255,255,255))
                text_rect = text.get_rect(center=(240,250))
                restart_rect = restart.get_rect(center=(240,330))
            else:
                text=font.render(f"{winner} Wins",True,(0,0,0))
                restart=font.render(f"Restart",True,(0,0,0))
                text_rect = text.get_rect(center=(240,250))
                restart_rect = restart.get_rect(center=(240,330))
            screen.blit(text,text_rect)
            screen.blit(restart,restart_rect)
        if result=="STALEMATE":
            text=font.render(f"DRAW By STALEMATE",True,(0,0,0))
            restart=font.render(f"Restart",True,(0,0,0))
            text_rect = text.get_rect(center=(240,250))
            restart_rect = restart.get_rect(center=(240,330))
            screen.blit(text,text_rect)
            screen.blit(restart,restart_rect)

    if promotion:
        promotion_menu(turn)
        if turn=="Black":
            if event.type==pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                for i in range(4):
                    rect=pygame.Rect(cord_x,cord_y+i*80,width,80)
                    if rect.collidepoint(x, y):
                        chosen_piece = ["Q","B","H","R"][i]
                        board[promotion_row][promotion_col] = chosen_piece
                        promotion = False
        else:
            if event.type==pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                for i in range(4):
                    rect=pygame.Rect(cord_x,cord_y+i*80,width,80)
                    if rect.collidepoint(x, y):
                        chosen_piece = ["-Q","-B","-H","-R"][i]
                        board[promotion_row][promotion_col] = chosen_piece
                        promotion = False

    own_king_row,own_king_col=king_position(turn)
    if check(own_king_row,own_king_col,turn):
        pygame.draw.rect(screen,(255, 0, 0),(own_king_col * SQ_SIZE,own_king_row * SQ_SIZE,SQ_SIZE,SQ_SIZE),5)
        checkmate=True
        every_piece=[]
        for i in range(8):
            for j in range(8):
                if turn=="White":
                    if board[i][j] in ["P","R","H","B","Q","K"]:
                        every_piece.append((i,j))
                else:
                    if board[i][j] in ["-P","-R","-H","-B","-Q","-K"]:
                        every_piece.append((i,j))
        for i,j in every_piece:
            for r,c in all_legel_move(board[i][j],i,j):
                piece=board[i][j]
                capture_piece=board[r][c]
                move(i,j,r,c)
                king_row,king_col=king_position(turn)
                safe = not check(king_row,king_col,turn)
                board[i][j]=piece
                board[r][c]=capture_piece
                if safe:
                    checkmate=False
                    break
            if not checkmate:
                break
        if checkmate:
                game_over=True
                winner="White" if turn=="Black" else "Black"
                result="CHECKMATE"
    else:
        move_possible=False
        every_piece=[]
        for i in range(8):
            for j in range(8):
                if turn=="White":
                    if board[i][j] in ["P","R","H","B","Q","K"]:
                        every_piece.append((i,j))
                else:
                    if board[i][j] in ["-P","-R","-H","-B","-Q","-K"]:
                        every_piece.append((i,j))
        for i,j in every_piece:
            for r,c in all_legel_move(board[i][j],i,j):
                piece=board[i][j]
                capture_piece=board[r][c]
                move(i,j,r,c)
                king_row,king_col=king_position(turn)   
                safe = not check(king_row,king_col,turn)
                board[i][j]=piece
                board[r][c]=capture_piece
                if safe:
                    move_possible=True
                    break
            if move_possible:
                break
        if not move_possible:
            game_over=True
            winner=None
            result="STALEMATE"

    if selected is not None:
        sel_row,sel_col=selected
        pygame.draw.rect(
        screen,
        (0, 255, 0), (sel_col * SQ_SIZE,sel_row * SQ_SIZE,SQ_SIZE,SQ_SIZE),4)

        all_possible_move=all_legel_move(board[sel_row][sel_col],sel_row,sel_col)
        for r,c in all_possible_move:
            center_x = c * SQ_SIZE + SQ_SIZE // 2
            center_y = r * SQ_SIZE + SQ_SIZE // 2
            pygame.draw.circle(screen,(255, 255, 255),(center_x, center_y),8)
        
    pygame.display.flip()

pygame.quit()
