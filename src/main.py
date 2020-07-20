#!/usr/sbin/python

import numpy as np
import math
import time
import sys
import os

if "--help" in sys.argv or "-h" in sys.argv:
    print("A two player Connect Four terminal application game")
    exit()
elif "-i" in sys.argv:
    print("This application was created by Gabriel Wong for a Coder Academy project")
    exit()

TERMX, TERMY = os.get_terminal_size()

# Center lines in terminal
def centred(*lines):
    for line in lines:
        yield line.center(TERMX)

# Print line centered in terminal.
def print_centred(line):
    print(*centred(line))

# Terminal application introduction screen
def intro_screen():
    print_centred("\n" * ((TERMY - 6 - 5) // 2)) 
    print_centred(" ██████╗ ██████╗ ███╗   ██╗███╗   ██╗███████╗ ██████╗████████╗    ███████╗ ██████╗ ██╗   ██╗██████╗ ")
    print_centred("██╔════╝██╔═══██╗████╗  ██║████╗  ██║██╔════╝██╔════╝╚══██╔══╝    ██╔════╝██╔═══██╗██║   ██║██╔══██╗")
    print_centred("██║     ██║   ██║██╔██╗ ██║██╔██╗ ██║█████╗  ██║        ██║       █████╗  ██║   ██║██║   ██║██████╔╝")
    print_centred("██║     ██║   ██║██║╚██╗██║██║╚██╗██║██╔══╝  ██║        ██║       ██╔══╝  ██║   ██║██║   ██║██╔══██╗")
    print_centred("╚██████╗╚██████╔╝██║ ╚████║██║ ╚████║███████╗╚██████╗   ██║       ██║     ╚██████╔╝╚██████╔╝██║  ██║")
    print_centred(" ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝ ╚═════╝   ╚═╝       ╚═╝      ╚═════╝  ╚═════╝ ╚═╝  ╚═╝")
    print_centred("By Gabriel Wong")
    print_centred("")
    print_centred("Welcome to Connect Four: a classic two-player strategy game")
    print_centred("")
    print_centred("Object: Connect four of your checkers in a row (horizontally, vertically or diagonally) while preventing")
    print_centred("your opponent from doing the same. But, look out - your opponent can sneak up on you and win the game!")
    print_centred("")
    print_centred("Press Enter to continue")
    new = input(("").center(TERMX // 2))

# Create empty board array (represented by 0s) using numpy
def create_board():
    board = np.zeros((6, 7), dtype=np.uint8)
    return board

# Display Game Board User Interface (UI)
def show(board):           
    os.system("clear || cls")  
    
    # Characters for a game piece
    cells = [" ", "●", "○"]
    
    print_centred("\n" * ((TERMY - 11) // 2)) 
    print_centred("  1   2   3   4   5   6   7 ")
    for row in reversed(board):
        print_centred("+---" * 6 + "+---+")
        print_centred("| " + " | ".join([cells[u] for u in row]) + " |") 
    print_centred("+---" * 6 + "+---+")
    print_centred("")
    print_centred("")
    print_centred("")

def drop_piece(board, row, column, piece):
    board[row][column] = piece

def is_valid_location(board, column):
    return board[5][column] == 0

def get_next_open_row(board, column):
    ROW_COUNT = 6
    for r in range(ROW_COUNT):
        if board[r][column] == 0:
            return r

# Check how many checkers are in column for animate_piece_drop function
def checkers_in_column(board,column):
    ROW_COUNT = 6
    count = 5
    for r in range(ROW_COUNT):
        if board[r][column] == 1 or board[r][column] == 2:
            count -= 1
    return count

# Animation of piece falling into place to simulate a real connect 4 game
def animate_piece_drop(board, column, piece):
    board_copy = board.copy()
    for row in (range(6 - (checkers_in_column(board,column))-1,6))[::-1]:
        board_copy[row, column] = piece
        show(board_copy)
        board_copy[row, column] = 0
        time.sleep(.08)

# Animation of board being cleared to simulate a real connect 4 board being cleared
def animate_clear_board(board):
    ROW_COUNT = 6
    board_copy = board.copy()
    for row in range(ROW_COUNT):
        board_copy = np.roll(board_copy, -7, axis=0)
        board_copy[5] = [0,0,0,0,0,0,0]
        show(board_copy)
        time.sleep(0.08)

# Check if a winning move (4 in a row) is achieved
def winning_move(board, piece):
    ROW_COUNT = 6
    COLUMN_COUNT = 7
    # Check for horizontal 4 in a row for win:
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check for vertical 4 in a row for win:
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check for upward sloping diagonal 4 in a row for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    
    # Check for downward sloping diagonal 4 in a row for win
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


# Main game while loop to continue until user quits
def main_game_loop():
    # Set game variables for the Connect 4 game while loop
    game = True
    turn = 1

    # Initalise empty board for first game
    board = create_board()

    # Show empty board for first game
    show(board)
    
    while game is True: 
        
        ROW_COUNT = 6
        COLUMN_COUNT = 7

        # Player 1's turn and empty space in board exists
        if turn % 2 == 1 and 0 in board:
            print_centred("Player 1 (White)'s turn. Enter in a number between 1 to 7.") 
                    
            # Error handling/try and except block for values that are not between 1 to 7.
            while True:
                try:
                    column = int(input("".center(TERMX // 2)))-1
                    if column > 6 or column < 0:
                        print_centred("This is not a valid number. Please enter a valid number between 1 to 7")
                    else:
                        break
                except ValueError:
                    print_centred("This is not a number. Please enter a valid number between 1 to 7")                    
            
            # Check if column input has any empty spaces available  
            if is_valid_location(board, column):
                
                # Assign row next open row available in column
                row = get_next_open_row(board, column)
                
                # Show animation of piece falling into position, like in real life
                animate_piece_drop(board, column, 1)
                
                # Insert player's piece into the board array
                drop_piece(board,row, column, 1)

                # Once piece added to board, check for any winning 4 in a row condition i.e. horizontally, vertically, upward diagonal, downward diagonal
                if winning_move(board, 1):
                    print_centred("Player 1 (White) wins")
                    print_centred("")
                    print_centred("Do you want to play again? (Y/N)")
                    
                    # Error handling/try and except block for input that is not Y or N.
                    while True:
                        try:
                            game_restart = input("".center(TERMX // 2)).upper()
                            if game_restart == "Y":
                                
                                # Show animation of board being cleared like in real life
                                animate_clear_board(board)

                                # Create new empty board
                                board = create_board()
                                break
                            elif game_restart == "N":
                                game = False
                                break
                            else:
                                print_centred("This is not a valid letter. Please enter Y or N")
                        except ValueError:
                            print_centred("This is not a valid letter. Please enter Y or N") 

        # Player 2's turn and empty space in board exists
        elif turn % 2 == 0 and 0 in board:
            print_centred("Player 2 (Black)'s turn. Enter in a number between 1 to 7.") 
            
            # Error handling/try and except block for values that are not between 1 to 7.
            while True:
                try:
                    column = int(input("".center(TERMX // 2)))-1
                    if column > 6 or column < 0:
                        print_centred("This is not a valid number. Please enter a valid number between 1 to 7")
                    else:
                        break
                except ValueError:
                    print_centred("This is not a number. Please enter a valid number between 1 to 7")

            # Check if column input has any empty spaces available  
            if is_valid_location(board, column):
                
                # Assign row next open row available in column
                row = get_next_open_row(board, column)
                
                #show animation of piece falling into position, like in real life
                animate_piece_drop(board, column, 2)

                # Insert player's piece into the board array
                drop_piece(board,row, column, 2)

                # Once piece added to board, check for any winning 4 in a row condition i.e. horizontally, vertically, upward diagonal, downward diagonal
                if winning_move(board, 2):
                    print_centred("Player 2 (Black) wins")
                    print_centred("")
                    print_centred("Do you want to play again? (Y/N)")

                    # Error handling/try and except block for input that is not Y or N.
                    while True:
                        try:
                            game_restart = input("".center(TERMX // 2)).upper()
                            if game_restart == "Y":
                                
                                # Show animation of board being cleared like in real life
                                animate_clear_board(board)

                                # Create new empty board
                                board = create_board()
                                break
                            elif game_restart == "N":
                                game = False
                                break
                            else:
                                print_centred("This is not a valid letter. Please enter Y or N")
                        except ValueError:
                            print_centred("This is not a valid letter. Please enter Y or N") 
        
        #Else condition for when there are no empty spaces left in the board and it's a draw              
        else:
            print_centred("It's a draw!")
            print_centred("")
            print_centred("Do you want to play again? Please enter Y or N")
            
            # Error handling/try and except block for input that is not Y or N.
            while True:
                try:
                    game_restart = input("".center(TERMX // 2)).upper()
                    if game_restart == "Y":
                        
                        # Show animation of board being cleared
                        animate_clear_board(board)
                        
                        # Create new empty board
                        board = create_board()
                        break
                    
                    elif game_restart == "N":
                        game = False
                    else:
                        print_centred("This is not a valid letter. Please enter Y or N")
        
                except ValueError:
                    print_centred("This is not a valid letter. Please enter Y or N") 

        # Update screen with player's move            
        show(board)

        # Allows players to alternate turns by incrementing turn by one each time 
        turn = turn + 1

# Initiate introduction screen function   
intro_screen()

# Initiate main game loop function
main_game_loop()

# Exit text when user exits the game
print_centred("Thanks for playing!")