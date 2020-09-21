from PIL import Image, ImageDraw
from pathlib import Path
import imageio
import natsort

def sortp(image_list1):
    image_list2 = []
    image_list3 = []
    image_list4 = []

    for i in image_list1:
        image_list2.append(i.stem)

    image_list3 = natsort.natsorted(image_list2, reverse=False)

    for i in image_list3:
        i = str(i)+ ".png"
        image_list4.append(Path('./photo', i))
    return image_list4

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        
class Frontier():
    def __init__(self):
        self.frontier = []
        
    def add(self, node):
        self.frontier.append(node)
        
    def isEmpty(self):
        return len(self.frontier) is 0
    
    def isContain(self, state):
        for node in self.frontier:
            if node.state == state:
                return True
            else:
                return False
    
    def select(self):
        if self.isEmpty():
            raise Exception("the frontier is empty")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class DFS():
    def __init__(self,filename):
        with open(filename) as f:
            env = f.read()
        if "A" not in env:
            raise Exception("There isn't a starting point")
        if "X" not in env:
            raise Exception("There isn't a goal")
        env = env.splitlines()
        self.height = len(env)
        self.width = max(len(line) for line in env)
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if env[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif env[i][j] == "X":
                        self.goal = (i, j)
                        row.append(False)
                    elif env[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        self.solution = None
    
    def show(self, scene=None):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("G", end="")
                elif solution is not None and (i, j) in solution[:scene]:
                    print("x", end="")
                else:
                    print(" ", end="")
            print()
        print()
    
    def nextpath(self, state):
        row, col = state
        choices = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in choices:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result
        
    def solve(self):
        self.num_explored = 0
        
        start = Node(state=self.start, parent=None, action=None)
        frontier = Frontier()
        frontier.add(start)

        self.explored = []

        while True:
            if frontier.isEmpty():
                raise Exception("no solution")

            node = frontier.select()
            self.num_explored += 1
            
            if node.state == self.goal:
                actions = []
                states = []
                while node.parent is not None:
                    actions.append(node.action)
                    states.append(node.state)
                    node = node.parent
                actions.reverse()
                states.reverse()
                self.solution = (actions, states)
                return

            self.explored.append(node.state)

            for action, state in self.nextpath(node.state):
                if not frontier.isContain(state) and state not in self.explored:
                    path = Node(state=state, parent=node, action=action)
                    frontier.add(path)
    
    def map_generate(self, filename, show_solution=True, show_explored=False, scene=None):
        cell_size = 50
        cell_border = 2

        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                if col:
                    fill = (20, 20, 20)

                elif (i, j) == self.start:
                    fill = (229, 9, 20)

                elif (i, j) == self.goal:
                    fill = (220, 235, 113)

                elif solution is not None and show_solution and (i, j) in solution[:scene]:
                    fill = (128, 128, 128)

                elif solution is not None and show_explored and (i, j) in self.explored[:scene]:
                    fill = (212, 97, 85)

                else:
                    fill = (237, 240, 252)

                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)
        
agent = DFS('map.txt')
agent.solve()
for i in range(agent.num_explored):
    agent.map_generate('photo/' + str(i) + '.png',show_explored=True,scene=i)
image_path = Path('photo')
images = list(image_path.glob('*.png'))
images = sortp(images)
image_list = []
for file_name in images:
    image_list.append(imageio.imread(file_name))
imageio.mimwrite('animated_dfs.gif', image_list)