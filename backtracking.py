def _is_safe(original_board, board, row, col, queens_in_colors, n):
    # Check the left side of the current row for any queens
    for i in range(col):
        if board[row][i] == 'Q':
            return False

    # Check the upper diagonal on the left side for any queens
    if col - 1 >= 0 and row - 1 >= 0:
        if board[row-1][col-1] == "Q":
            return False

    # Check the lower diagonal on the left side for any queens
    if col - 1 >= 0 and row + 1 < n:
        if board[row+1][col-1] == "Q":
            return False

    # Check the column above the current row for any queens
    for i in range(row):
        if board[i][col] == "Q":
            return False

    # Ensure no queen is placed in the same color region
    current_color = original_board[row][col]
    if queens_in_colors[current_color]:
        return False

    # Return True if all checks are passed, making it safe to place a queen
    return True

def _solve(original_board, board, col, queens_in_colors, n):
    # Base case: If all queens are placed successfully, return True
    if col >= n:
        return True

    # Try placing a queen in each row of the current column
    for i in range(n):
        # Check if placing a queen at (i, col) is safe
        if _is_safe(original_board, board, i, col, queens_in_colors, n):
            # Place the queen at (i, col)
            board[i][col] = 'Q'
            # Mark the color as having a queen placed
            queens_in_colors[original_board[i][col]] = True 

            # Recur to place queens in the next column
            if _solve(original_board, board, col + 1, queens_in_colors, n):
                return True

            # Backtrack: Remove the queen and unmark the color if placing queen doesn't lead to a solution
            board[i][col] = original_board[i][col]
            queens_in_colors[original_board[i][col]] = False

    # If no placement is possible in this column, return False
    return False

def solve_n_queens(board):
    import copy
    # Create a deep copy of the board to preserve the original
    copy_board = copy.deepcopy(board)
    # Initialize a dictionary to track which colors have queens placed
    queens_in_colors = {str(i): False for i in range(1, len(board)+1)}
    
    # Attempt to solve the N-Queens problem using the copied board
    if not _solve(board, copy_board, 0, queens_in_colors, len(board)):
        print("Unable to find solution")
    else:
        # Print the original board configuration and the solved board
        print("|" + "|\n|".join([",".join(r) for r in board]) + "|")
        print("======================================")
        print("|" + "|\n|".join([",".join(r) for r in copy_board]) + "|")
    
    # Return the solved board
    return copy_board
