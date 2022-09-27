# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


# TODO remove
from searchTestClasses import GraphSearch
def depthFirstSearch(problem: GraphSearch):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    # s0
    s = problem.getStartState()
    prev = (-1, -1)
    # States visited and fringe
    V = set()
    L = util.Stack()
    L.push((s, prev, Directions.STOP))
    # Memory of the steps
    steps = [(prev, Directions.STOP, prev)]
    # Main loop
    while (not L.isEmpty()):
        s, prev, dir = L.pop()
        if not problem.isGoalState(s):
            # c = ((x,y),'West',1)
            # Filtering not visited states
            C = [c for c in problem.getSuccessors(s) if c[0] not in V]
            for c in C: # Adding neighbors to fringe
                L.push((c[0], s, c[1]))
            V.add(s)
            # Checking the last state in the steps
            while steps[-1][0] != prev: 
                # Depiles states until the previous state is found to add
                # the new state at the right place
                steps.pop()
            steps.append((s, dir))
        else:
            steps.append((s, dir))
            return [d for _, d in steps[2:]]
    return -1


def breadthFirstSearch(problem: GraphSearch):
    """Search the shallowest nodes in the search tree first."""

    # s0
    s = problem.getStartState()
    prev = (-1, -1)
    # States visited and fringe
    V = set()
    L = util.Queue()
    L.push((s, prev, Directions.STOP))
    # Memory of the steps
    steps = [(prev, Directions.STOP, prev)]

    # Main loop
    while (not L.isEmpty()):
        s, prev, dir = L.pop()
        if not problem.isGoalState(s):
            # c = ((x,y),'West',1)
            # Filtering not visited states
            C = [c for c in problem.getSuccessors(s) if c[0] not in V]
            for c in C:
                L.push((c[0], s, c[1]))
                # To keep the first apparation of each node inside the fringe 
                # even if their not explored yet
                V.add(c[0])
            V.add(s)
            steps.append((s, dir, prev))
        else:
            prev_step = prev
            sol = [(s, dir)]

            while (prev_step != (-1, -1) and len(steps) != 0):
                current, dir, prev = steps.pop()
                if current == prev_step:
                    prev_step = prev
                    sol.insert(0, (current, dir))

            return [d for _, d in sol[1:]]
    return -1


def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    # s0
    s = problem.getStartState()
    prev = (-1, -1)
    cost = 0
    # States visited and fringe
    V = set()
    L = util.PriorityQueue()
    L.push((s, prev, Directions.STOP, cost), cost)
    # Memory of the steps
    steps = [(prev, Directions.STOP, prev)]

    # Main loop
    while (not L.isEmpty()):
        s, prev, dir, cost = L.pop()
        if not problem.isGoalState(s):
            # c = ((x,y),'West',1)
            # Filtering not visited states
            C = [c for c in problem.getSuccessors(s) if c[0] not in V]
            for c in C:
                newCost = c[2] + cost
                L.push((c[0], s, c[1], newCost), newCost)
                # To keep the first apparation of each node inside the fringe 
                # even if their not explored yet
                if not problem.isGoalState(c[0]) :
                    V.add(c[0])
            V.add(s)
            steps.append((s, dir, prev))
        else:
            prev_step = prev
            sol = [(s, dir)]
            while (prev_step != (-1, -1) and len(steps) != 0):
                current, dir, prev = steps.pop()
                if current == prev_step:
                    prev_step = prev
                    sol.insert(0, (current, dir))

            return [d for _, d in sol[1:]]
    return -1


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    # s0
    s = problem.getStartState()
    start = s
    prev = (-1, -1)
    cout = heuristic(s, problem)
    # States visited and fringe
    V = set()
    L = util.PriorityQueue()
    # Memory of the steps
    steps = [(prev, Directions.STOP, prev)]
    L.push((s, prev, Directions.STOP, cout), cout)

    i = 0

    # object use to create the solution
    sortie = []
    actuel = s
    prev_rechercher = (0, 0)

    while (not L.isEmpty()):
        i += 1
        s, prev, dir, cout = L.pop()
        cout = cout - heuristic(s, problem)
        if not problem.isGoalState(s):
            if s not in V:
                V.add(s)
                C = [c for c in problem.getSuccessors(s) if c[0] not in V]
                # c = ((4,5),'West',1)
                for c in C:
                    L.push((c[0], s, c[1], c[2]+cout+heuristic(c[0],
                           problem)), c[2]+cout+heuristic(c[0], problem))
                # V.add(c[0]) #to keep the first apparation of each node inside the fringe even if their not explore yet
                steps.append((s, dir, prev))
        else:
            # print("WIN\n")

            prev_rechercher = prev
            sortie.insert(0, (s, dir))
            while (prev_rechercher != (-1, -1) and len(steps) != 0):
                actuel, dir, prev = steps.pop()
                if actuel == prev_rechercher:
                    prev_rechercher = prev
                    sortie.insert(0, (actuel, dir))

            return [d for _, d in sortie[1:]]  # + [dir]
        # print(f"[{i:2d}] : s = {s}\nV = {V}\nL = {L}\nsteps = {steps}\n")
    return -1


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
