import sys
import random
from csp import *

def constraint(v):
    for i in neighbors:
        if v == i:
            raise ValueError("Not a Kenken puzzle")

def add(args):
    if (None in args):
        return None
    total = 0
    for arg in args:
        total += arg
    return total

def sub(args):
    if (None in args):
        return None
    return abs(args[0]-args[1])

def mult(args):
    if (None in args):
        return None
    product = 1
    for arg in args:
        product *= arg
    return product

def div(args):
    if (None in args):
        return None
    temp = float(args[0]) / float(args[1])
    if (temp > 1):
        return temp
    else:
        return 1/temp

def nothing(args):
    if (None in args):
        return None
    return args[0]


class Constraint:
    def __init__(self, f, bSize, result, cords):
        self.cells = []
        self.func = f
        self.target = result
        for c in cords:
            self.cells.append(c[0] * bSize + c[1])


def parseConstraint(line, bSize):
    tokens = line.split()
    if (tokens[1] == "add"):
        func = add
    elif (tokens[1] == "sub"):
        func = sub
    elif (tokens[1] == "mult"):
        func = mult
    elif (tokens[1] == "div"):
        func = div
    elif (tokens[1] == "''"):
        func = nothing
    else:
        raise NameError("Could not parse function in constraint: " + tokens[0])

    try:
        if (int(tokens[2])%1 != 0.0):
            raise NameError("line: " + line + "...Error: evaluation result must be a whole number")
        else:
            result = int(tokens[2])
    except ValueError:
        raise ValueError("line: " + line + "...Error: " + tokens[2] + " is not a number")

    coords = []
    tokens[0] = tokens[0][1:-1]
    strcords = tokens[0].split("),(")
    for coord in strcords:
        coord = coord.replace(")", "").replace("(", "")
        coord = coord.split(",")
        try:
            coord = (int(coord[0]), int(coord[1]))
        except ValueError:
            raise ValueError("line: " + line + "...Error: " + str(coord) + " does not appear to be a valid coordinate")
        coords.append(coord)
    c = Constraint(func, bSize, result, coords)
    return c

boardSize = 0

def kenken_constraint(A, a, B, b):
    if(A==B): return True
    if(int(A/boardSize) == int(B/boardSize)) or (A % boardSize == B % boardSize):
        return a != b
    return True


class Kenken(CSP):
    consts = []

    def __init__(self, n):
        ttl = n * n
        dom = {}
        ngh = {}
        for i in range(ttl):
            dom[i] = list(range(1,n+1))
        for i in range(ttl):
            ngh[i] = range(ttl)
        CSP.__init__(self, list(range(ttl)), dom, ngh, kenken_constraint)

    def AddConstraint(self, c):
        self.consts.append(c)

    def CheckAssignment(self, c, var, val, assignment):
        values = []
        for cell in c.cells:
            if(cell == var):
                v = val
            else:
                v = assignment.get(cell, None)
            if(v is None):
                return 0
            values.append(v)

        result = int(c.func(values))
        if(c.target == result):
            return 0
        return len(values) - 1

    def nconflicts(self, var, val, assignment):
        tmp = 0

        for v in self.neighbors[var]:
            for c in self.consts:
                for cell in c.cells:
                    if(cell == v and v in assignment):
                        tmp += self.CheckAssignment(c, var, val, assignment)

        return CSP.nconflicts(self, var, val, assignment) + tmp



def main(kenkenFileName):
    global boardSize
    lines = []
    try:
        kkFile = open(kenkenFileName)
    except IOError:
        raise IOError("Error: could not find KenKen file '" + sys.argv[1] + "'")

    kenkenLines = [line.strip() for line in kkFile.readlines() if line is not '']
    if (float(kenkenLines[0]) % 1 != 0):
        raise NameError("line: " + kenkenLines[0] + "...Error: board size must be an integer")

    boardSize = int(kenkenLines[0])
    kenken = Kenken(boardSize)
    for line in kenkenLines[1:]:
        kenken.AddConstraint(parseConstraint(line, boardSize))

    res = backtracking_search(kenken) 
    #res = backtracking_search(kenken, select_unassigned_variable=mrv) 
    #res = backtracking_search(kenken, inference=forward_checking)
    #res = backtracking_search(kenken, select_unassigned_variable=mrv, inference=forward_checking)
    #res = backtracking_search(kenken, inference=mac)
    #res = min_conflicts(kenken)
    if res is None:
        print("None") 
    else:
        for r in res: 
            v = res[r]
            if r % boardSize == 0:
                sys.stdout.write("\n")
            if(v<10):
                 sys.stdout.write(" ")
            sys.stdout.write(str(v) + " ")
        sys.stdout.write("\n")
        sys.stdout.flush()

if __name__ == "__main__":
    if (len(sys.argv) == 2):
        main(sys.argv[1])



