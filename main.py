import pygame
import pygame_gui
import mazegen
pygame.init()


# Variables 
W, H = 1700, 900

gapW, gapH = 350, 100

rows, columns = 71, 101

White = (255, 255, 255)
Gray = (100, 100, 100)
Black = (0, 0, 0)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)

gridW, gridH = W - 2 * gapW, H - 2 * gapH
old_columns, old_rows = 100, 70
cellW = (W - 2 * gapW) // old_columns
cellH = (H - 2 * gapH) // old_rows

# Adjust gap values to fit new grid
gapW = (W - (cellW * columns)) // 2
gapH = (H - (cellH * rows)) // 2


# Creating window and naming it, also Creating the UIManager
surface = pygame.display.set_mode((W, H))
pygame.display.set_caption('Pathfinding Visualizer') 
manager = pygame_gui.UIManager((W, H))



# Functions
def drawGridOutline():
    for col in range(columns +1):
        x = gapW + col * cellW
        pygame.draw.line(surface, Gray, (x, gapH), (x, gapH + gridH), 1)

    for row in range(rows + 1):
        y = gapH + row * cellH
        pygame.draw.line(surface, Gray, (gapW, y), (gapW + gridW, y), 1)


def drawCell(x, y, color):
    cell = pygame.Rect(x, y, cellW - 1, cellH - 1);
    pygame.draw.rect(surface, color, cell)


def drawMatrix(matrix):
    for i in range(rows):
        for j in range(columns):
            x = (j * cellW) + gapW
            y = (i * cellH) + gapH
            if matrix[i][j] == 0:
                drawCell(x, y, Black)
            elif matrix[i][j] == 1:
                drawCell(x, y, White)
            elif matrix[i][j] == 2:
                drawCell(x, y, Blue)
            elif matrix[i][j] == "S":
                drawCell(x, y, Red)
            elif matrix[i][j] == "G":
                drawCell(x, y, Green)



# Classes
class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
    

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class Maze:
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        if contents.count("S") != 1:
            raise ValueError("Maze must have exactly one start point")
        if contents.count("G") != 1:
            raise ValueError("Maze must have exactly one goal")

        contents = contents.splitlines()
        self.height = rows
        self.width = columns

        if len(contents) != self.height or any(len(line) != self.width for line in contents):
            raise ValueError("Maze dimensions do not match expected size")

        self.grid = []
        self.start = None
        self.goal = None

        for i in range(self.height):
            row = []
            for j in range(self.width):
                char = contents[i][j]
                if char == "S":
                    self.start = (i, j)
                    row.append("S")
                elif char == "G":
                    self.goal = (i, j)
                    row.append("G")
                elif char == " ":
                    row.append(0)
                else:
                    row.append(1)
            self.grid.append(row)

        self.solution = None

    def neighbors(self, state):
        """Returns valid neighboring cells (avoiding walls)."""
        row, col = state
        directions = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        valid_cells = {"S", "G", 0} 
        return [
            (action, (r, c)) for action, (r, c) in directions
            if 0 <= r < self.height and 0 <= c < self.width and self.grid[r][c] in valid_cells
        ]
    
    def solve(self):
        """Finds a solution to maze, if one exists."""
        self.num_explored = 0

        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        self.explored = set()

        while True:

            if frontier.empty():
                raise Exception("no solution")

            node = frontier.remove()
            self.num_explored += 1
            
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)

                for r, c in cells:
                    if (r, c) != self.start and (r, c) != self.goal:
                        self.grid[r][c] = 2
                        drawMatrix(self.grid)
                        pygame.display.flip()
                break 

            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)



# Buttons
startButton = pygame.Rect(gapW, gapH-50, 100, 50)
pygame_gui.elements.UIButton(relative_rect = startButton, text = "SOLVE", manager = manager)

newMaze = pygame.Rect(W - gapW - 100, gapH-50, 100, 50)
pygame_gui.elements.UIButton(relative_rect = newMaze, text = "NEW MAZE", manager = manager)


# Initializations
mazegen.save_maze_to_file(mazegen.generate_maze(columns, rows))
maze = Maze("maze.txt")
matrix = maze.grid

# Main Game Loop
clock = pygame.time.Clock()
running = True
while running:
    delta = clock.tick(60)/1000.0
    
    # Processing events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == startButton:
                maze.solve()
                #matrix = maze.grid
                #drawMatrix(matrix)
            if event.ui_element == newMaze:
                mazegen.save_maze_to_file(mazegen.generate_maze(columns, rows))
                maze = Maze("maze.txt")
                matrix = maze.grid
        manager.process_events(event)
    manager.update(delta)
    drawMatrix(matrix)
    drawGridOutline()
    manager.draw_ui(surface)
    pygame.display.flip()
