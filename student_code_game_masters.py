from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        peg1, peg2, peg3 = []  # will later be changed to tuples
        list_of_pegs = self.kb.kb_ask(Fact("(inst ?peg peg)"))  # build list of all known pegs (typically 3)
        for peg_binding in list_of_pegs:  # for each peg, find out if its empty or what disks are on it
            if not Fact(instantiate(Statement("(empty ?peg)"), peg_binding)) in self.kb.facts:
                # if not empty, get list of all disks on it
                list_of_disks = self.kb.kb_ask(Fact(instantiate(Statement("(on ?disk ?peg)"), peg_binding)))
                list_of_disk_int = []
                for disk_binding in list_of_disks:
                    disk_int = int(disk_binding.constant.element[4])
                    list_of_disk_int.append(disk_int)
                peg_int = int(peg_binding.constant.element[3])  # get this peg's identity
                if peg_int == 1:
                    while list_of_disk_int:  # depopulate this list and build the correct tuple
                        smallest = min(list_of_disk_int)
                        peg1.append(smallest)
                        list_of_disk_int.remove(smallest)
                elif peg_int == 2:
                    while list_of_disk_int:  # depopulate this list and build the correct tuple
                        smallest = min(list_of_disk_int)
                        peg2.append(smallest)
                        list_of_disk_int.remove(smallest)
                else:
                    while list_of_disk_int:  # depopulate this list and build the correct tuple
                        smallest = min(list_of_disk_int)
                        peg3.append(smallest)
                        list_of_disk_int.remove(smallest)
        state = (tuple(peg1), tuple(peg2), tuple(peg3))
        return state

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        terms = movable_statement.terms
        disk = terms[0]
        origin = terms[1]
        target = terms[2]
        self.kb.kb_retract(Fact(Statement(("on", disk, origin))))
        self.kb.kb_retract(Fact(Statement(("top", disk, origin))))
        self.kb.kb_assert(Fact(Statement(("on", disk, target))))
        self.kb.kb_assert(Fact(Statement(("top", disk, target))))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        rows = {"pos1": ("pos1", "pos2", "pos3"),  # rows are y coordinates, columns are x
                "pos2": ("pos1", "pos2", "pos3"),
                "pos3": ("pos1", "pos2", "pos3")}
        state = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
        for y_pos in rows:
            y = int(y_pos[3])
            for x_pos in rows[y_pos]:
                x = int(x_pos[3])
                ask = Fact(Statement(["coord", "?tile", x_pos, y_pos]))
                binding = self.kb.kb_ask(ask)
                tile = binding.constant.element[4]
                tile_int = 0
                if tile == 'y':  # tile name is 'empty'
                    tile_int = -1
                else:
                    tile_int = int(tile)
                state[y][x] = tile_int
        return [tuple(state[0]), tuple(state[1]), tuple(state[2])]

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        terms = movable_statement.terms
        tile = terms[0]
        initial_x = terms[1]
        initial_y = terms[2]
        target_x = terms[3]
        target_y = terms[4]
        #  'empty tile' and movable tile basically swap coordinates
        self.kb.kb_retract(Fact(Statement(("coord", tile, initial_x, initial_y))))
        self.kb.kb_retract(Fact(Statement(("coord", "empty", target_x, target_y))))
        self.kb.kb_assert(Fact(Statement(("coord", tile, target_x, target_y))))
        self.kb.kb_assert(Fact(Statement(("coord", "empty", initial_x, initial_y))))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
