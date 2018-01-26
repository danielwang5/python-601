
'''def search(successors, start_state, goal_test, dfs=False):
    visited = [start_state[0]]
    visitedpath = [[start_state[0]]]

    prev = [start_state]
    curr = []

    while True:
        for item in prev:
            succ = successors(item)
            for s in succ:
                if s not in visited:
                    curr.append(s)
                    visited.append(s)
                    visitedpath.append(visitedpath[visited.index(item)] + [s])
        
        for node in curr:
            #print(node)
            if goal_test(node):
                return visitedpath[visited.index(node)]
        prev = curr
        curr = []'''

def search(successors, start_state, goal_test, dfs = False):
    if goal_test(start_state):
        return [start_state]
    else:
        agenda = [SearchNode(start_state, None)]
        visited = {start_state}
        while len(agenda) > 0:
            if dfs: # Stack
                parent = agenda.pop(-1)
            else:   # Queue
                parent = agenda.pop(0)
            for child_state in successors(parent.state):
                child = SearchNode(child_state, parent)
                if goal_test(child_state):
                    return child.path()
                if child_state not in visited:
                    agenda.append(child)
                    visited.add(child_state)
        return None
    

class SearchNode:
    def __init__(self, state, parent, cost = 0.):
        self.state = state
        self.parent = parent
    def path(self):
        p = []
        node = self
        while node:
            p.append(node.state)
            node = node.parent
        p.reverse()
        return p

def knight_successor(state):
    moves = [(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]
    board_x, board_y = (8,8)
    out = []
    x,y = state
    for dx,dy in moves:
        nx,ny = x+dx,y+dy
        if (-1<nx<board_x) and (-1<ny<board_y):
            out.append((nx,ny))
    return out

print(search(knight_successor,[(4,4)],lambda x: (2,2) == x))
