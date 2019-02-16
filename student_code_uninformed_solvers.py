
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        possible_moves = self.gm.getMovables  # returns a list of movable Statements
        child_depth = self.gm.depth + 1
        for move in possible_moves:  # build list of children in this new node
            self.gm.makeMove(move)  # try expanding into this state to see if it is new
            if self.gm.getGameState() not in self.visited:
                new_state = GameState(self.gm.getGameState, child_depth, move)
                new_state.parent = self.currentState  # save the current game state as the parent
                self.currentState.children.append(new_state)
            self.gm.reverseMove(move)
        if self.currentState.children:  # there are new unvisited children, expand into the first one
            self.currentState.nextChildToVisit += 1
            self.currentState = self.currentState.children[0]
            if self.currentState == self.victoryCondition:
                return True
            else:
                self.visited[self.currentState] = True
                return False
        else:  # no unvisited child node found, find ancestor with unvisited child
            while self.currentState.parent:  # while there is a parent to go to (i.e. not root)
                self.currentState = self.currentState.parent
                ind = self.currentState.nextChildToVisit
                if len(self.currentState.children) > ind:  # this parent still has unvisited children
                    self.currentState.nextChildToVisit += 1
                    self.currentState = self.currentState.children[ind]
                    if self.currentState == self.victoryCondition:
                        return True
                    else:
                        self.visited[self.currentState] = True
                        return False
            return False  # no more unexplored game states

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        return True
