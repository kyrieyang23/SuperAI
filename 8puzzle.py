import copy
class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        
class FrontierBFS():
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
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Puzzle():
    def __init__(self, filename):
        with open(filename) as f:
            env = f.read()
        for i in ['0','1','2','3','4','5','6','7','8']:
            if i not in env:
                raise Exception("Environment haven't been set")
        env = env.splitlines()
        self.height = len(env)
        self.width = max(len(line) for line in env)
        self.walls = []
        self.goal = {(1,1):'1',(1,2):'2',(1,3):'3',(2,1):'8',(2,2):'0',
                     (2,3):'4',(3,1):'7',(3,2):'6',(3,3):'5',}
        self.position = {}
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if env[i][j] in ['0','1','2','3','4','5','6','7','8','9']:
                        self.position[(i,j)] = env[i][j]
                        row.append(False)
                    elif env[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        self.solution = None
        
    def show(self, scene=-1, showStart=True):
        solution = self.solution[1] if self.solution is not None else None
        print()
        if showStart == True:
            print("start")
            for i, row in enumerate(self.walls):
                for j, col in enumerate(row):
                    if col:
                        print("█", end="")
                    elif (i,j) in list(self.position.keys()):
                        print(self.position[(i,j)], end="")
                    else:
                        print(" ", end="")
                print()
            print()
        if solution[scene] is not None:
            print("state scene " + str(scene+1))
            for i, row in enumerate(self.walls):
                for j, col in enumerate(row):
                    if col:
                        print("█", end="")
                    elif (i,j) in list(solution[scene].keys()):
                        print(solution[scene][(i,j)], end="")
                    else:
                        print(" ", end="")
                print()
        print()
    
    def nextaction(self, state):
        count = 0
        for i in list(state.keys()):
            if state[i] == '0':            
                row, col = list(state.keys())[count]
            count += 1
        choices = [
            ("down", (row - 1, col)),
            ("up", (row + 1, col)),
            ("right", (row, col - 1)),
            ("left", (row, col + 1))
        ]
        result = []
        for action, (r, c) in choices:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                newstate = copy.deepcopy(state)
                newstate[(row,col)] = newstate[(r,c)] 
                newstate[(r,c)] = '0'
                result.append((action, newstate))
        return result
    
    def solve(self):
        self.num_explored = 0
        
        start = Node(state=self.position, parent=None, action=None)
        frontier = FrontierBFS()
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

            for action, state in self.nextaction(node.state):
                if not frontier.isContain(state) and state not in self.explored:
                    slide = Node(state=state, parent=node, action=action)
                    frontier.add(slide)
agent = Puzzle('8puzzle.txt')
agent.solve()
showstart = True
for i in range(len(agent.solution[1])):
    agent.show(i,showstart)
    print("v")
    showstart = False
print("Done")
 
        
        
        
        
        
        
        
        
        
        