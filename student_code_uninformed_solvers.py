
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
        if self.currentState.state == self.victoryCondition:   # first check if already resolved
            return True
        possible_moves = self.gm.getMovables()  # returns a list of movable Statements
        child_depth = self.currentState.depth + 1
        move = False
        while not move:  # while next move not found
            ind = self.currentState.nextChildToVisit
            if len(possible_moves) <= ind:  # no moves possible from this node (this is a leaf)
                if self.currentState.parent:  # try finding ancestor with unvisited children if there are parents
                    self.gm.reverseMove(self.currentState.requiredMovable)  # reverse in gm
                    possible_moves = self.gm.getMovables()  # change list of moves to ancestor's
                    self.currentState = self.currentState.parent  # become ancestor, retry finding move
                    child_depth = self.currentState.depth + 1
                    continue
                else:  # no more parents and no more unvisited children, it's gg
                    return False
            trying_move = possible_moves[ind]
            self.gm.makeMove(trying_move)
            new_state = GameState(self.gm.getGameState(), child_depth, trying_move)
            if new_state not in self.visited:  # this is an unvisited state, explore
                new_state.parent = self.currentState  # save the current game state as the parent
                self.currentState.children.append(new_state)
                self.currentState.nextChildToVisit += 1  # so that next time, continue down possible moves
                self.currentState = new_state  # move to new state
                move = trying_move  # this breaks out of finding a loop
            else:  # this state has been visited, go to next possible move at this node
                self.gm.reverseMove(trying_move)  # return to current node in order to try different move
                self.currentState.nextChildToVisit += 1
        if self.currentState.state == self.victoryCondition:  # move found, check if won
            return True
        else:
            self.visited[self.currentState] = True  # have not won, add this state to visited
            return False

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
