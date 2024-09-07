def _is_safe(original_board, board, row, col, queens_in_colors, n):
    # Check this row on left side
    for i in range(col):
        if board[row][i] == 'Q':
            return False

    # Check upper diagonal on left side
    if col - 1 >= 0 and row - 1 >= 0:
        if board[row-1][col-1] == "Q":
            return False

    if col - 1 >= 0 and row + 1 < n:
        if board[row+1][col-1] == "Q":
            return False

    for i in range(row):
        if board[i][col] == "Q":
            return False

    # same color shouldnt have one
    current_color = original_board[row][col]
    if queens_in_colors[current_color]:
        return False

    return True

def _solve(original_board, board, col, queens_in_colors, n):
    if col >= n:
        return True

    # Consider this column and try placing queens in all rows one by one
    for i in range(n):
        if _is_safe(original_board, board, i, col, queens_in_colors, n):
            board[i][col] = 'Q'
            queens_in_colors[original_board[i][col]] = True 

            # Recur to place the rest of the queens
            if _solve(original_board, board, col + 1, queens_in_colors, n):
                return True

            # If placing queen at board[i][col] doesn't lead to a solution, then backtrack
            board[i][col] = original_board[i][col]
            queens_in_colors[original_board[i][col]] = False

    return False

def solve_n_queens(board):
    import copy
    copy_board = copy.deepcopy(board)
    queens_in_colors = {str(i): False for i in range(1, len(board)+1)}
    
    if not _solve(board, copy_board, 0, queens_in_colors, len(board)):
        print("Unable to find solution")
    else:
        print("|" + "|\n|".join([",".join(r) for r in board]) + "|")
        print("======================================")
        print("|" + "|\n|".join([",".join(r) for r in copy_board]) + "|")
    return copy_board