import random

def generate_maze(width, height):
    # Initialize the maze with walls
    maze = [['#' for _ in range(width)] for _ in range(height)]
    
    # Carve out paths using a randomized DFS approach
    stack = []
    start_x, start_y = 1, 1
    maze[start_y][start_x] = 'S'
    stack.append((start_x, start_y))
    
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    
    while stack:
        x, y = stack[-1]
        random.shuffle(directions)
        moved = False
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < width-1 and 0 < ny < height-1 and maze[ny][nx] == '#':
                maze[ny][nx] = ' '
                maze[y + dy//2][x + dx//2] = ' '
                stack.append((nx, ny))
                moved = True
                break
        
        if not moved:
            stack.pop()
    
    # Set the goal far from the start
    goal_x, goal_y = width-2, height-2
    while maze[goal_y][goal_x] != ' ' or (goal_x == start_x and goal_y == start_y):
        goal_x = random.randint(1, width-2)
        goal_y = random.randint(1, height-2)
    maze[goal_y][goal_x] = 'G'
    
    return maze

def save_maze_to_file(maze, filename="maze.txt"):
    with open(filename, 'w') as file:
        for row in maze:
            file.write(''.join(row) + '\n')
