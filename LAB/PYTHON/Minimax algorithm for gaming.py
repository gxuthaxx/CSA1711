import math


def print_board(board):
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print("--+---+--")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print("--+---+--")
    print(f"{board[6]} | {board[7]} | {board[8]}")
    print()


def check_winner(board, player):
    win_positions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for pos in win_positions:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] == player:
            return True
    return False


def is_full(board):
    return all(cell != ' ' for cell in board)


def minimax(board, depth, is_maximizing):
    if check_winner(board, 'O'):
        return 10 - depth
    if check_winner(board, 'X'):
        return depth - 10
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(best_score, score)
        return best_score


def best_move(board):
    best_score = -math.inf
    move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    return move


def get_valid_move(board):
    while True:
        try:
            move = int(input("Enter position (1-9): ")) - 1
            if move < 0 or move > 8:
                print("Invalid position. Try again.")
                continue
            if board[move] != ' ':
                print("Cell already taken. Try again.")
                continue
            return move
        except ValueError:
            print("Please enter a number between 1 and 9.")


def play_game():
    board = [' '] * 9

    print("Tic Tac Toe: You are X, Computer is O")
    print_board(board)

    while True:
        move = get_valid_move(board)
        board[move] = 'X'
        print_board(board)

        if check_winner(board, 'X'):
            print("You win!")
            break
        if is_full(board):
            print("It's a draw!")
            break

        print("Computer's turn...")
        move = best_move(board)
        board[move] = 'O'
        print_board(board)

        if check_winner(board, 'O'):
            print("Computer wins!")
            break
        if is_full(board):
            print("It's a draw!")
            break


if __name__ == "__main__":
    play_game()
