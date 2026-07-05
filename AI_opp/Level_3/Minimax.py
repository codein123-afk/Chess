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
TT={}
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
nodes=0
tt_hits=0
white_castled=False
black_castled=False
pawn_table = [[0,0,0,0,0,0,0,0],
        [5,5,5,5,5,5,5,5],
        [1,1,2,3,3,2,1,1],
        [0.5,0.5,1,2.5,2.5,1,0.5,0.5],
        [0,0,0,2,2,0,0,0],
        [0.5,-0.5,-1,0,0,-1,-0.5,0.5],
        [0.5,1,1,-2,-2,1,1,0.5],
        [0,0,0,0,0,0,0,0]]

knight_table = [
        [-5,-4,-3,-3,-3,-3,-4,-5],
        [-4,-2, 0, 0, 0, 0,-2,-4],
        [-3, 0, 1, 1.5,1.5,1, 0,-3],
        [-3, 0.5,1.5,2,2,1.5,0.5,-3],
        [-3, 0,1.5,2,2,1.5,0,-3],
        [-3, 0.5,1,1.5,1.5,1,0.5,-3],
        [-4,-2,0,0.5,0.5,0,-2,-4],
        [-5,-4,-3,-3,-3,-3,-4,-5]]

bishop_table=[[-2,-1,-1,-1,-1,-1,-1,-2],
        [-1,0,0,0,0,0,0,-1],
        [-1,0,0.5,1,1,0.5,0,-1],
        [-1,0.5,0.5,1,1,0.5,0.5,-1],
        [-1,0,1,1,1,1,0,-1],
        [-1,1,1,1,1,1,1,-1],
        [-1,0.5,0,0,0,0,0.5,-1],
        [-2,-1,-1,-1,-1,-1,-1,-2]]

rook_table = [[0,0,0,0,0,0,0,0],
        [0.5,1,1,1,1,1,1,0.5],
        [-0.5,0,0,0,0,0,0,-0.5],
        [-0.5,0,0,0,0,0,0,-0.5],
        [-0.5,0,0,0,0,0,0,-0.5],
        [-0.5,0,0,0,0,0,0,-0.5],
        [-0.5,0,0,0,0,0,0,-0.5],
        [0,0,0,0.5,0.5,0,0,0]]

queen_table = [[-2,-1,-1,-0.5,-0.5,-1,-1,-2],
        [-1,0,0,0,0,0,0,-1],
        [-1,0,0.5,0.5,0.5,0.5,0,-1],
        [-0.5,0,0.5,0.5,0.5,0.5,0,-0.5],
        [0,0,0.5,0.5,0.5,0.5,0,-0.5],
        [-1,0.5,0.5,0.5,0.5,0.5,0,-1],
        [-1,0,0.5,0,0,0,0,-1],
        [-2,-1,-1,-0.5,-0.5,-1,-1,-2]]

     
king_table = [[-3,-4,-4,-5,-5,-4,-4,-3],
        [-3,-4,-4,-5,-5,-4,-4,-3],
        [-3,-4,-4,-5,-5,-4,-4,-3],
        [-3,-4,-4,-5,-5,-4,-4,-3],
        [-2,-3,-3,-4,-4,-3,-3,-2],
        [-1,-2,-2,-2,-2,-2,-2,-1],
        [2,2,0,0,0,0,2,2],
        [2,3,1,0,0,1,3,2]]

king_endgame_table = [[-5,-4,-3,-2,-2,-3,-4,-5],
[-3,-2,-1, 0, 0,-1,-2,-3],
[-3,-1, 2, 3, 3, 2,-1,-3],
[-3,-1, 3, 4, 4, 3,-1,-3],
[-3,-1, 3, 4, 4, 3,-1,-3],
[-3,-1, 2, 3, 3, 2,-1,-3],
[-3,-3, 0, 0, 0, 0,-3,-3],
[-5,-3,-3,-3,-3,-3,-3,-5]]

passed_pawn_bonus = [0.0,1,0.8,0.5,0.3,0.2,0.1,0.0 ]
piece_index = {"P":0,"H":1,"B":2,"R":3,"Q":4,"K":5,"-P":6,"-H":7,"-B":8,"-R":9,"-Q":10,"-K":11}
random.seed(0)
zobrist = [[random.getrandbits(64)
            for _ in range(64)]
            for _ in range(12)]

MAX_DEPTH = 10
killer_moves = [[None, None] for _ in range(MAX_DEPTH + 1)]
EXACT = 0
LOWERBOUND = 1
UPPERBOUND = 2

trained_value={ 
    "white_material":0.8588,"black_material":-0.8428,
    "passed_pawn_white":1.3985,"passed_pawn_black":-1.4104,
    "score_board":0.1055,"pawn_structure":0.7655,
    "king_safety_white":0.4499,"king_safety_black":0.7732,
    "white_bishop_pair":0.6582,"black_bishop_pair":-0.7652,
    "white_check":0.5000,"black_check":-0.5000,
    "white_castled":0.2445,"black_castled":-0.2301}


def move(x,y,a,b):
    global board_hash
    piece=board[x][y]
    capture_piece=board[a][b]
    board_hash^=zobrist[piece_index[piece]][x*8+y]
    if capture_piece != "0":
        board_hash ^= zobrist[piece_index[capture_piece]][a*8+b]
    board[a][b]=board[x][y]
    board[x][y]="0"
    board_hash ^= zobrist[piece_index[piece]][a*8+b]

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
            return board[row_2][col_2]=="0"
        if row_1==6 and row_2==4:
                return board[5][col_1] == "0" and board[4][col_1] == "0"
        return False
    if n=="-P":
        if col_1!=col_2:
            return False
        if row_2-row_1==1:
            return board[row_2][col_2]=="0"
        if row_1==1 and row_2==3:
            return board[2][col_1] == "0" and board[3][col_1] == "0"
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
    if target == "K" or target == "-K":
        return False
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

def all_legel_move(n,row_1,col_1,colour):
    moves=[]
    for i in range(8):
        for j in range(8):
            if legal_move(n,row_1,col_1,i,j):
                piece=board[row_1][col_1]
                target=board[i][j]
                move(row_1,col_1,i,j)
                king_row,king_col=king_position(colour)
                safe=not check(king_row,king_col,colour)
                board[row_1][col_1]=piece
                board[i][j]=target
                if safe:
                    moves.append((i,j))
            if capture(n,row_1,col_1,i,j):
                piece=board[row_1][col_1]
                target=board[i][j]
                move(row_1,col_1,i,j)
                king_row,king_col=king_position(colour)
                safe=not check(king_row,king_col,colour)
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
                    moves=all_legel_move(piece,i,j,turn)
                    for r,c in moves:
                        all_moves.append((i,j,r,c))
            if turn=="Black":
                if board[i][j] in ["-P","-Q","-K","-B","-R","-H"]:
                    moves=[]
                    piece=board[i][j]
                    moves=all_legel_move(piece,i,j,turn)
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
                                    if turn_ai:
                                        board[row][col] = "Q"
                                        promotion = False
                                    else:
                                        promotion = True
                                        promotion_row = row
                                        promotion_col = col
                                if piece=="-P" and row==7:
                                    if turn_ai:
                                        board[row][col] = "-Q"
                                        promotion = False
                                    else:
                                        promotion = True
                                        promotion_row = row
                                        promotion_col = col
                                if piece=="K":
                                    if first_col==4 and col==6:
                                        board[7][5]="R"
                                        board[7][7]="0"
                                        white_castled=True
                                    if first_col==4 and col==2:
                                        board[7][3]="R"
                                        board[7][0]="0"
                                        white_castled=True
                                    white_king_move=True
                                if piece=="-K":
                                    if first_col==4 and col==6:
                                        board[0][5]="-R"
                                        board[0][7]="0"
                                        black_castled=True
                                    if first_col==4 and col==2:
                                        board[0][3]="-R"
                                        board[0][0]="0"
                                        black_castled=True
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

def board_position(piece,row,col,is_endgame):
    score=0
    table={"P":pawn_table,"Q":queen_table,"B":bishop_table,"H":knight_table,"R":rook_table,"K":king_table,
    "-P":pawn_table,"-Q":queen_table,"-B":bishop_table,"-H":knight_table,"-R":rook_table,"-K":king_table
    }
    if piece=="P":
            score=table[piece][row][col]
            return score
    if piece=="-P":
            score=-table[piece][7-row][col]
            return score

    if piece=="H":
            score=table[piece][row][col]
            return score
    if piece=="-H":
            score=-table[piece][7-row][col]
            return score

    if piece=="B":
            score=table[piece][row][col]
            return score
    if piece=="-B":
            score=-table[piece][7-row][col]
            return score

    if piece=="R":
            score=table[piece][row][col]
            return score
    if piece=="-R":
            score=-table[piece][7-row][col]
            return score
    
    if piece=="Q":
            score=table[piece][row][col]
            return score
    if piece=="-Q":
            score=-table[piece][7-row][col]
            return score    
    if piece=="K":
            if is_endgame:
                score=king_endgame_table[row][col]
            else:
                score=table[piece][row][col]
            return score
    if piece=="-K":
            if is_endgame:
                score-=king_endgame_table[7-row][col]
            else:
                score=-table[piece][7-row][col]
            return score

def passed_pawn(row,col,turn):
        if turn=="White":
            for r in range(row-1,-1,-1):
                if col==0:
                    for c in [col,col+1]:
                        if board[r][c]=="-P":
                            return False
                elif col==7:
                    for c in [col-1,col]:
                        if board[r][c]=="-P":
                            return False
                else:    
                    for c in [col-1,col,col+1]:
                        if board[r][c]=="-P":
                            return False
            return True
        if turn=="Black":
            for r in range(row+1,8):
                if col==0:
                    for c in [col,col+1]:
                        if board[r][c]=="P":
                            return False
                elif col==7:
                    for c in [col-1,col]:
                        if board[r][c]=="P":
                            return False
                else:    
                    for c in [col-1,col,col+1]:
                        if board[r][c]=="P":
                            return False
            return True

def Pawn_structure(white_rook,black_rook,white_pawn,black_pawn):
        score=0
        for c in range(8):
            if white_pawn[c]>=2:
                score-=0.2 * (white_pawn[c] - 1)
            if black_pawn[c]>=2:
                score+=0.2*(black_pawn[c]-1)
            if white_pawn[c]!=0:
                if c==0:
                    if white_pawn[c+1]==0:
                        score-=0.2*white_pawn[c]
                elif c==7:
                    if white_pawn[c-1]==0:
                        score-=0.2*white_pawn[c]
                else:
                    if white_pawn[c+1]==0 and white_pawn[c-1]==0:
                        score-=0.2*white_pawn[c]
            if black_pawn[c]!=0:
                if c==0:
                    if black_pawn[c+1]==0:
                        score+=0.2*black_pawn[c]
                elif c==7:
                    if black_pawn[c-1]==0:
                        score+=0.2*black_pawn[c]
                else:
                    if black_pawn[c+1]==0 and black_pawn[c-1]==0:
                        score+=0.2*black_pawn[c]
        for row,col in white_rook:
                if white_pawn[col]==0:
                        if black_pawn[col]==0:
                            score+=0.25
                        else:
                            score+=0.12
        for row,col in black_rook:
                if black_pawn[col]==0:
                        if white_pawn[col]==0:
                            score-=0.25
                        else:
                            score-=0.12
        return (score)                
   
def king_saftey(turn,white_pawn,black_pawn):
    score=0
    king_row,king_col=king_position(turn)
    if turn=="White":
        if king_row>0:
            if king_col==0:
                for i in range(2):
                    if board[king_row-1][king_col+i]=="P":
                        score+=0.1
            elif king_col==7:
                for i in range(2):
                    if board[king_row-1][king_col-i]=="P":
                        score+=0.1
            else:
                for i in [king_col-1,king_col,king_col+1]:
                    if board[king_row-1][i]=="P":
                        score+=0.1
        if white_pawn[king_col] == 0:
            score -= 0.2
        if white_pawn[king_col] == 0 and black_pawn[king_col] == 0:
            score -= 0.2
    if turn=="Black":
        if king_row<7:
            if king_col==0:
                for i in range(2):
                    if board[king_row+1][king_col+i]=="-P":
                        score-=0.1
            elif king_col==7:
                for i in range(2):
                    if board[king_row+1][king_col-i]=="-P":
                        score-=0.1
            else:
                for i in [king_col-1,king_col,king_col+1]:
                    if board[king_row+1][i]=="-P":
                        score-=0.1
        if black_pawn[king_col] == 0:
            score += 0.2
        if white_pawn[king_col] == 0 and black_pawn[king_col] == 0:
            score += 0.2
    return score

def endgame():
    value=0
    pieces={"Q":9,"R":5,"B":3,"H":3,"P":0,"K":0,"-Q":9,"-R":5,"-B":3,"-H":3,"-P":0,"-K":0}
    for r in range(8):
        for c in range(8):
            piece=board[r][c]
            if piece!="0":
                value+=pieces[piece]
    return value<18

def capture_moves(turn):
    moves=[]
    for i in range(8):
        for j in range(8):
            piece=board[i][j]
            if piece=="0":
                continue
            if turn=="White" and not is_white(piece):
                continue
            if turn=="Black" and not is_black(piece):
                continue
            legel=all_legel_move(piece,i,j,turn)
            for r, c in legel:
                if board[r][c]!="0":
                    moves.append((i,j,r,c))
    return moves

def quiescene(alpha,beta,turn):
    global nodes
    nodes+=1
    standard_score=evalute(board)
    if turn=="White":
        if standard_score>=beta:
            return beta
        alpha=max(alpha,standard_score)
    else:
        if standard_score<=alpha:
            return alpha
        beta=min(standard_score,beta)
    moves=capture_moves(turn)
    moves.sort(key=lambda x: move_score(*x), reverse=True)
    next_turn = "Black" if turn == "White" else "White"
    for row1, col1, row2, col2 in moves:
        capture_piece = board[row2][col2]
        moved_piece = board[row1][col1]
        move(row1, col1, row2, col2)
        score = quiescene(alpha, beta, next_turn)
        undo_move(row1, col1, row2, col2, capture_piece, moved_piece)
        if turn == "White":
            alpha = max(alpha, score)
            if alpha >= beta:
                return beta
        else:
            beta = min(beta, score)
            if beta <= alpha:
                return alpha
    return alpha if turn == "White" else beta

def compute_hash():
    h=0
    for r in range(8):
        for c in range(8):
            piece=board[r][c]
            if piece=="0":
                continue 
            square=8*r+c
            h^=zobrist[piece_index[piece]][square]
    return h

def evalute(board):
    score_board=0
    passed_pawn_white=0
    passed_pawn_black=0
    black_material=0
    white_material=0
    white_bishop = 0
    black_bishop = 0
    white_check = 0
    black_check = 0
    white_bishop_pair = 0
    black_bishop_pair = 0
    white_castled_feature=0
    black_castled_feature=0
    white_value={"P":1,"H":3,"B":3,"Q":9,"R":5,"K":1}
    black_value={"-P":1,"-H":3,"-B":3,"-Q":9,"-R":5,"-K":1}
    white_rook=[]
    black_rook=[]
    black_pawn=[0]*8
    white_pawn=[0]*8
    is_endgame=endgame()
    for i in range(8):
        for j in range(8):
            piece=board[i][j]
            if board[i][j]=="0":
                continue
            else:
                if piece in white_value:
                    white_material+=white_value[piece]
                    if board[i][j]=="R":
                        white_rook.append((i,j))
                    if board[i][j]=="B":
                        white_bishop+=1
                    if board[i][j]=="P":
                        white_pawn[j]+=1
                        if passed_pawn(i,j,"White"):
                            passed_pawn_white+=passed_pawn_bonus[i]
                if piece in black_value:
                    black_material+=black_value[piece]
                    if board[i][j]=="-R":
                        black_rook.append((i,j))
                    if board[i][j]=="-B":
                        black_bishop+=1
                    if board[i][j]=="-P":
                        black_pawn[j]+=1
                        if passed_pawn(i,j,"Black"):
                            passed_pawn_black+=passed_pawn_bonus[7-i]
                score_board+=board_position(board[i][j],i,j,is_endgame)   
               
    pawn_structure_score=Pawn_structure(white_rook,black_rook,white_pawn,black_pawn)
    king_saftey_white_score=king_saftey("White",white_pawn,black_pawn)
    king_saftey_black_score=king_saftey("Black",white_pawn,black_pawn)
    black_row,black_col=king_position("Black")
    if white_bishop==2:
        white_bishop_pair=1
    if black_bishop==2:
        black_bishop_pair=1
    if check(black_row,black_col,"Black"):
        black_check=1
    white_row,white_col=king_position("White")
    if check(white_row,white_col,"White"):
        white_check=1
    if white_castled:
        white_castled_feature=1
    if black_castled:
        black_castled_feature=1
    score=white_material*trained_value["white_material"]+black_material*trained_value["black_material"]+passed_pawn_white*trained_value["passed_pawn_white"]
    + passed_pawn_white*trained_value["passed_pawn_black"]+score_board*trained_value["score_board"]+pawn_structure_score*trained_value["pawn_structure"]
    + king_saftey_white_score*trained_value["king_safety_white"] + king_saftey_black_score*trained_value["king_safety_black"] + white_bishop_pair*trained_value["white_bishop_pair"]
    + black_bishop_pair*trained_value["black_bishop_pair"] + white_check*trained_value["white_check"]+black_check*trained_value["black_check"]
    + white_castled_feature*trained_value["white_castled"]+ black_castled_feature*trained_value["black_castled"]

    return score


def undo_move(row_1,col_1,row_2,col_2,capture_piece,moved_piece):
    global board_hash
    board_hash ^= zobrist[piece_index[moved_piece]][row_2*8+col_2]
    board_hash^=zobrist[piece_index[moved_piece]][row_1*8+col_1]
    if capture_piece != "0":
        board_hash ^= zobrist[piece_index[moved_piece]][row_2*8+col_2]
    board[row_1][col_1]=moved_piece
    board[row_2][col_2]=capture_piece

def move_score(row_1,col_1,row_2,col_2):
    piece=board[row_2][col_2]
    value={"P":1,"H":3,"B":3,"Q":9,"R":5,"K":100,"-P":1,"-H":3,"-B":3,"-Q":9,"-R":5,"-K":100,"0":0 }
    return value[piece]

def order_move(moves_all,depth,tt_move):
    moves_all.sort(key=lambda m: move_score(*m),reverse=True)
    for killer in killer_moves[depth]:
            if killer is not None and killer in moves_all:
                moves_all.remove(killer)
                moves_all.insert(0, killer)
    if tt_move is not None and tt_move in moves_all:
        moves_all.remove(tt_move)
        moves_all.insert(0, tt_move)
    return moves_all

def minimax(depth,turn,alpha,beta,null_allowed=True):
    global nodes
    global tt_hits
    global board_hash
    alpha_original = alpha  
    beta_original = beta
    nodes+=1
    if depth==0:
        return quiescene(alpha,beta,turn)
    key = (board_hash,turn,white_king_move,
        black_king_move,white_left_rook_move,
        white_right_rook_move,black_left_rook_move
        ,black_right_rook_move)
    entry = TT.get(key)
    tt_move = None
    if entry is not None:
        stored_depth, stored_score ,flag,tt_move= entry
        if stored_depth >= depth:
            if flag==EXACT:   
                tt_hits += 1
                return stored_score
            elif flag == LOWERBOUND:
                alpha = max(alpha, stored_score)
            elif flag == UPPERBOUND:
                beta = min(beta, stored_score)
            if alpha >= beta:
                tt_hits += 1
                return stored_score
    if turn=="White":
            best_score = float("-inf")
            best_move = None

            moves_all=all_move(turn)
            if len(moves_all)==0:
                pos = king_position("White")
                if pos is None:
                    print("WHITE KING MISSING")
                    for row in board:
                        print(row)
                    return -10000
                king_row, king_col = pos
                if check(king_row,king_col,"White"):
                    return -10000-depth
                return 0
            moves_all=order_move(moves_all,depth,tt_move)
            #if depth >= 3 and null_allowed and not endgame():
            #    king_row, king_col = king_position("White")
            #    if not check(king_row, king_col, "White"):
            #        null_score=minimax(depth - 3,"Black",beta-1,beta,False)
            #        if null_score >= beta:
            #            return beta
            for moves in moves_all:
                row_1,col_1,row_2,col_2=moves
                capture_piece=board[row_2][col_2]
                promotion=False
                original_piece=board[row_1][col_1]
                move(row_1,col_1,row_2,col_2)
                if original_piece=="P" and row_2==0:
                    board_hash ^= zobrist[piece_index["P"]][row_2*8 + col_2]
                    board[row_2][col_2]="Q"
                    board_hash ^= zobrist[piece_index["Q"]][row_2*8 + col_2]
                    promotion=True
                score=minimax(depth-1,"Black",alpha,beta,True)
                if promotion:
                    board_hash ^= zobrist[piece_index["Q"]][row_2*8 + col_2]
                    board[row_2][col_2] = original_piece
                    board_hash ^= zobrist[piece_index["P"]][row_2*8 + col_2]
                    promotion=False
                undo_move(row_1,col_1,row_2,col_2,capture_piece,original_piece)

                if score > best_score:
                    best_score = score
                    best_move = moves
                alpha = max(alpha, best_score)
                if beta<=alpha:
                    if capture_piece == "0":
                        if killer_moves[depth][0] != moves:
                            killer_moves[depth][1] = killer_moves[depth][0]
                            killer_moves[depth][0] = moves
                    break
            if best_score <= alpha_original:   
                    flag = UPPERBOUND
            elif best_score >= beta_original:
                    flag = LOWERBOUND
            else:
                    flag = EXACT
            TT[key] = (depth, best_score, flag,best_move)
            return best_score
    if turn=="Black":
            best_score = float("inf")
            best_move = None
            moves_all=all_move(turn)
            if len(moves_all)==0:
                pos = king_position("Black")
                if pos is None:
                    print("Black KING MISSING")
                    for row in board:
                        print(row)
                    return -10000
                king_row, king_col = pos
                if check(king_row,king_col,"Black"):
                    return 10000+depth
                return 0
            moves_all=order_move(moves_all,depth,tt_move)
            #if depth >= 3 and null_allowed and not endgame():
            #    king_row, king_col = king_position("Black")
            #    if not check(king_row, king_col, "Black"):
            #        null_score=minimax(depth - 3,"White",alpha,alpha+1,False)
            #        if null_score <= alpha:
            #            return alpha
            for moves in moves_all:
                row_1,col_1,row_2,col_2=moves
                capture_piece=board[row_2][col_2]
                promotion=False
                original_piece=board[row_1][col_1]
                move(row_1,col_1,row_2,col_2)
                if original_piece=="-P" and row_2==7:
                    board_hash ^= zobrist[piece_index["-P"]][row_2*8 + col_2]
                    board[row_2][col_2]="-Q"
                    board_hash ^= zobrist[piece_index["-Q"]][row_2*8 + col_2]
                    promotion=True
                score=minimax(depth-1,"White",alpha,beta,True)
                if promotion:
                    board_hash ^= zobrist[piece_index["-Q"]][row_2*8 + col_2]
                    board[row_2][col_2] = original_piece
                    board_hash ^= zobrist[piece_index["-P"]][row_2*8 + col_2]
                    promotion=False
                undo_move(row_1,col_1,row_2,col_2,capture_piece,original_piece)
                if score < best_score:
                    best_score = score
                    best_move = moves
                beta = min(beta, best_score)
                if beta<=alpha:
                    if capture_piece == "0":
                        if killer_moves[depth][0] != moves:
                            killer_moves[depth][1] = killer_moves[depth][0]
                            killer_moves[depth][0] = moves
                    break
            if best_score <= alpha_original:   
                    flag = UPPERBOUND
            elif best_score >= beta_original:
                    flag = LOWERBOUND
            else:
                    flag = EXACT
            TT[key] = (depth, best_score, flag,best_move)
            return best_score

def best_move(depth,turn):
    final_move=None
    for current_depth in range(1,depth+1):
        first_row=0
        first_col=0
        second_row=0
        second_col=0
        moves_all=all_move(turn)
        moves_all.sort(key=lambda m: move_score(*m), reverse=True)
        if final_move is not None and final_move in moves_all:
            moves_all.remove(final_move)
            moves_all.insert(0, final_move)
        if not moves_all:
            global game_over
            game_over=True
            return None
        if turn=="White":
            best_score=float("-inf") 
            for moves in moves_all:
                row_1,col_1,row_2,col_2=moves
                capture_piece=board[row_2][col_2]
                move(row_1,col_1,row_2,col_2)
                promotion = False
                original_piece=board[row_1][col_1]
                piece = board[row_2][col_2]
                if piece == "P" and row_2 == 0:
                    board[row_2][col_2] = "Q"
                    promotion = True
                score=minimax(current_depth-1,"Black",float("-inf"),float('inf'),True)
                if promotion:
                    board[row_2][col_2] = piece
                    promotion=False
                undo_move(row_1,col_1,row_2,col_2,capture_piece,original_piece)
                if score > best_score:
                    best_score = score
                    final_move = (row_1, col_1, row_2, col_2)
        if turn=="Black":
            best_score=float("inf") 
            for moves in moves_all:
                row_1,col_1,row_2,col_2=moves
                capture_piece=board[row_2][col_2]
                original_piece=board[row_1][col_1]
                move(row_1,col_1,row_2,col_2)
                promotion = False
                piece = board[row_2][col_2]
                if piece == "-P" and row_2 == 7:
                    board[row_2][col_2] = "-Q"
                    promotion = True
                score=minimax(current_depth-1,"White",float("-inf"),float('inf'),True)
                if promotion:
                    board[row_2][col_2] = piece
                    promotion=False
                undo_move(row_1,col_1,row_2,col_2,capture_piece,original_piece)
                if score < best_score:
                    best_score = score
                    final_move = (row_1, col_1, row_2, col_2)
        print(f"Depth {current_depth} | "f"Score {best_score:.2f} | "f"Move {final_move}")
    return final_move

def extract_features(board):
    score_board=0
    passed_pawn_white=0
    passed_pawn_black=0
    black_material=0
    white_material=0
    white_bishop = 0
    black_bishop = 0
    white_check = 0
    black_check = 0
    white_bishop_pair = 0
    black_bishop_pair = 0
    white_castled_feature=0
    black_castled_feature=0
    white_value={"P":1,"H":3,"B":3,"Q":9,"R":5,"K":1}
    black_value={"-P":1,"-H":3,"-B":3,"-Q":9,"-R":5,"-K":1}
    white_rook=[]
    black_rook=[]
    black_pawn=[0]*8
    white_pawn=[0]*8
    is_endgame=endgame()
    for i in range(8):
        for j in range(8):
            piece=board[i][j]
            if board[i][j]=="0":
                continue
            else:
                if piece in white_value:
                    white_material+=white_value[piece]
                    if board[i][j]=="R":
                        white_rook.append((i,j))
                    if board[i][j]=="B":
                        white_bishop+=1
                    if board[i][j]=="P":
                        white_pawn[j]+=1
                        if passed_pawn(i,j,"White"):
                            passed_pawn_white+=passed_pawn_bonus[i]
                if piece in black_value:
                    black_material+=black_value[piece]
                    if board[i][j]=="-R":
                        black_rook.append((i,j))
                    if board[i][j]=="-B":
                        black_bishop+=1
                    if board[i][j]=="-P":
                        black_pawn[j]+=1
                        if passed_pawn(i,j,"Black"):
                            passed_pawn_black+=passed_pawn_bonus[7-i]
                score_board+=board_position(board[i][j],i,j,is_endgame)   
               
    pawn_structure_score=Pawn_structure(white_rook,black_rook,white_pawn,black_pawn)
    king_saftey_white_score=king_saftey("White",white_pawn,black_pawn)
    king_saftey_black_score=king_saftey("Black",white_pawn,black_pawn)
    black_row,black_col=king_position("Black")
    if white_bishop==2:
        white_bishop_pair=1
    if black_bishop==2:
        black_bishop_pair=1
    if check(black_row,black_col,"Black"):
        black_check=1
    white_row,white_col=king_position("White")
    if check(white_row,white_col,"White"):
        white_check=1
    if white_castled:
        white_castled_feature=1
    if black_castled:
        black_castled_feature=1
    return (white_material,black_material,passed_pawn_white,passed_pawn_black,score_board,pawn_structure_score,
            king_saftey_white_score,king_saftey_black_score,white_bishop_pair,black_bishop_pair,white_check,
            black_check,white_castled_feature,black_castled_feature)


board_hash = compute_hash()
print(board_hash)
old_hash = board_hash
capture_piece = board[4][4]
moved_piece = board[6][4]
move(6, 4, 4, 4)
undo_move(6, 4, 4, 4, capture_piece, moved_piece)
print(old_hash == board_hash)



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
            nodes=0
            row_1,col_1,row_2,col_2=best_move(4,turn)
            print(nodes)
            print("TT hits:", tt_hits)
            print("TT size:", len(TT))
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
            for r,c in all_legel_move(board[i][j],i,j,turn):
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
            for r,c in all_legel_move(board[i][j],i,j,turn):
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

        all_possible_move=all_legel_move(board[sel_row][sel_col],sel_row,sel_col,turn)
        for r,c in all_possible_move:
            center_x = c * SQ_SIZE + SQ_SIZE // 2
            center_y = r * SQ_SIZE + SQ_SIZE // 2
            pygame.draw.circle(screen,(255, 255, 255),(center_x, center_y),8)
        
    pygame.display.flip()

pygame.quit()
