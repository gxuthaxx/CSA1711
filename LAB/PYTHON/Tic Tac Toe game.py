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
    current_player = 'X'

    print("Tic Tac Toe")
    print_board(board)

    while True:
        print(f"Player {current_player}'s turn")
        move = get_valid_move(board)
        board[move] = current_player

        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} wins!")
            break

        if is_full(board):
            print("It's a draw!")
            break

        current_player = 'O' if current_player == 'X' else 'X'


if __name__ == "__main__":
    play_game()
