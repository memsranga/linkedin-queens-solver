import cv2 as cv
import numpy as np
import math
from backtracking import solve_n_queens

def extract_grid(file_name):
    original = cv.imread(file_name)
    cv.imwrite("solution/original.png", original)

    gray = cv.cvtColor(original, cv.COLOR_BGR2GRAY)

    contours, _ = cv.findContours(gray, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv.contourArea, reverse=True)

    # try to fix the 1
    x, y, w, h = cv.boundingRect(contours[1])

    # Crop the grid area from the image
    grid = original[y:y+h, x:x+w]

    cv.imwrite("solution/grid.png", grid)

    gray = cv.cvtColor(grid, cv.COLOR_BGR2GRAY)
    cv.imwrite("solution/gray-grid.png", gray)

    contours, _ = cv.findContours(gray, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv.contourArea)

    total_cells = len(contours) - 2
    grid_size = int(math.sqrt(total_cells))
    if total_cells != grid_size**2:
        print("Unable to detect full grid! Aborting")

    cell_width = w // grid_size
    cell_height = h // grid_size

    colors = []

    board = []
    color_index = 1
    color_map = {}
    reverse_color_map = {}
    padding = 10
    for i in range(grid_size):
        row = []
        for j in range(grid_size):
            # Calculate cell coordinates
            cell_x = j * cell_width
            cell_y = i * cell_height
    
            padding = 15
            cell = grid[cell_y+padding:cell_y+cell_height-padding, cell_x+padding:cell_x+cell_width-padding]
            
            # Get the average color of the cell
            avg_color = cell.mean(axis=0).mean(axis=0)
            avg_color = avg_color.astype(int)
            avg_color = tuple(avg_color)
            
            # Append the color in RGB format
            # row_colors.append(tuple(avg_color))
            if avg_color not in color_map:
                color_map[avg_color] = str(color_index)
                reverse_color_map[str(color_index)] = avg_color
                color_index += 1
            row.append(color_map[avg_color])
            
        board.append(row)

    # print("|" + "|\n|".join([",".join(r) for r in board]) + "|")

    # print(len(color_map), grid_size)

    solved_board = solve_n_queens(board)
                
    
    if len(color_map) != grid_size:
        print("Too many colors detected! Aborting")



    # recreating grid
    output_image = np.ones((h,w,3), dtype="uint8")

    border_size = 1
    letter_height = 10

    for i in range(grid_size):
        for j in range(grid_size):
            # Calculate the position of each cell
            cell_x = j * cell_width
            cell_y = i * cell_height
            # color = (int(colors[i][j][0]), int(colors[i][j][1]), int(colors[i][j][2]))
            color_pick = reverse_color_map.get(board[i][j])
            color = (int(color_pick[0]), int(color_pick[1]), int(color_pick[2]))
            
            
            
            output_image = cv.rectangle(output_image, (cell_x + border_size, cell_y + border_size), (cell_x + cell_width - border_size, cell_y + cell_height - border_size), color, thickness=-1)
            output_image = cv.line(output_image, (cell_x, cell_y), (cell_x + cell_width, cell_y ), (0,0,0), thickness=1)
            if solved_board[i][j] == "Q":
                output_image = cv.putText(output_image, "Q", (cell_x + cell_width // 2 - letter_height, cell_y + cell_height // 2 + letter_height), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,0), lineType=cv.LINE_AA, thickness=2)
            # else: 
            #     output_image = cv.putText(output_image, "X", (cell_x + cell_width // 2 - letter_height, cell_y + cell_height // 2 + letter_height), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,0), thickness=2)


    cv.imwrite("solution/solve.png", output_image)

extract_grid("queens/3.png")