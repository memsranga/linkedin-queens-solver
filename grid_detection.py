import cv2 as cv
import numpy as np
import math
# from backtracking import solve_n_queens
# from linear_programming import solve_n_queens
from llm_agent import solve_n_queens
import time

def extract_grid(file_name):
    start = time.perf_counter()

    # Read the input image
    original = cv.imread(file_name)
    # Save the original image for reference
    cv.imwrite("solution/original.png", original)

    # Convert the image to grayscale for easier contour detection
    gray = cv.cvtColor(original, cv.COLOR_BGR2GRAY)

    # Find contours in the grayscale image
    contours, _ = cv.findContours(gray, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    # Sort contours by area in descending order
    contours = sorted(contours, key=cv.contourArea, reverse=True)

    # Extract the bounding box of the puzzle grid (usually the second largest contour)
    x, y, w, h = cv.boundingRect(contours[1])

    # Crop the grid area from the original image
    grid = original[y:y+h, x:x+w]
    # Save the cropped grid image
    cv.imwrite("solution/grid.png", grid)

    # Convert the cropped grid to grayscale
    gray = cv.cvtColor(grid, cv.COLOR_BGR2GRAY)
    # Save the grayscale grid image
    cv.imwrite("solution/gray-grid.png", gray)

    # Find contours again within the cropped grayscale grid
    contours, _ = cv.findContours(gray, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    # Sort contours by area
    contours = sorted(contours, key=cv.contourArea)

    # Calculate the total number of cells and the grid size
    total_cells = len(contours) - 2
    grid_size = int(math.sqrt(total_cells))
    if total_cells != grid_size**2:
        print("Unable to detect full grid! Aborting")

    # Calculate the width and height of each cell
    cell_width = w // grid_size
    cell_height = h // grid_size

    # Initialize variables to store colors and board configuration
    colors = []
    board = []
    color_index = 1
    color_map = {}
    reverse_color_map = {}
    padding = 10

    # Iterate through each cell in the grid to extract colors
    for i in range(grid_size):
        row = []
        for j in range(grid_size):
            # Calculate cell coordinates with padding
            cell_x = j * cell_width
            cell_y = i * cell_height
            padding = 15
            cell = grid[cell_y+padding:cell_y+cell_height-padding, cell_x+padding:cell_x+cell_width-padding]
            
            # Get the average color of the cell
            avg_color = cell.mean(axis=0).mean(axis=0)
            avg_color = avg_color.astype(int)
            avg_color = tuple(avg_color)
            
            # Map each unique color to an index
            if avg_color not in color_map:
                color_map[avg_color] = str(color_index)
                reverse_color_map[str(color_index)] = avg_color
                color_index += 1
            row.append(color_map[avg_color])
            
        # Append the row to the board configuration
        board.append(row)

    # Solve the N-Queens problem using the extracted board configuration
    solved_board = solve_n_queens(board)
                
    # Check if the number of detected colors matches the grid size; abort if mismatched
    if len(color_map) != grid_size:
        print("Too many colors detected! Aborting")

    # Create a blank output image to recreate the grid
    output_image = np.ones((h, w, 3), dtype="uint8")

    # Define border and letter sizes for grid elements
    border_size = 1
    letter_height = 10

    # Iterate through each cell to draw the grid and place queens
    for i in range(grid_size):
        for j in range(grid_size):
            # Calculate the position of each cell
            cell_x = j * cell_width
            cell_y = i * cell_height
            # Get the color for the current cell from the reverse color map
            color_pick = reverse_color_map.get(board[i][j])
            color = (int(color_pick[0]), int(color_pick[1]), int(color_pick[2]))
            
            # Draw the cell with the appropriate color
            output_image = cv.rectangle(
                output_image, 
                (cell_x + border_size, cell_y + border_size), 
                (cell_x + cell_width - border_size, cell_y + cell_height - border_size), 
                color, 
                thickness=-1
            )
            # Draw grid lines between the cells
            output_image = cv.line(
                output_image, 
                (cell_x, cell_y), 
                (cell_x + cell_width, cell_y), 
                (0, 0, 0), 
                thickness=1
            )
            # Draw the letter "Q" if the cell contains a queen
            if solved_board[i][j] == "Q":
                output_image = cv.putText(
                    output_image, 
                    "Q", 
                    (cell_x + cell_width // 2 - letter_height, cell_y + cell_height // 2 + letter_height), 
                    cv.FONT_HERSHEY_COMPLEX, 
                    1, 
                    (0, 0, 0), 
                    lineType=cv.LINE_AA, 
                    thickness=2
                )

    # Save the final output image with the solved board displayed
    cv.imwrite("solution/solve.png", output_image)

    end = time.perf_counter()
    elapsed = end - start
    print(f'Time taken: {elapsed:.6f} seconds')

# Run the grid extraction and solving process on the provided image file
extract_grid("queens/3.png")
