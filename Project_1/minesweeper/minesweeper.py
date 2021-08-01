import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """ 
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells
        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # Second Accounts for case when set is empty
        if self.count == 0:
            return self.cells
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1
        self.moves_made.add(cell)

        # 2
        self.mark_safe(cell)

        # 3
        new_neighbours, new_count = self.get_neighbours(cell, count)
        if new_neighbours:
            self.knowledge.append(Sentence(new_neighbours, new_count))

        # 4 & 5, will continously loop until neither mark_cells or -
        # add_new_sentences make changes to the knowledge base
        while self.mark_cells() or self.add_new_sentences():
            print("No. Sentences = ", len(self.knowledge))


    def clean_up(self):
        """
        Removes Empty Sentences
        """
        for sentence in self.knowledge:
            if not sentence.cells:
                self.knowledge.remove(sentence)

    def mark_cells(self):
        """
        Marks any additional cells as safe or mines if it may be concluded from the AIs database
        """
        new_safes = set()
        new_mines = set()

        for sentence in self.knowledge:
            safe_store = sentence.known_safes()
            mine_store = sentence.known_mines()
            if safe_store is not None:
                new_safes = new_safes | safe_store
            if mine_store is not None:
                new_mines = new_mines | mine_store

        for the_safe in new_safes:
            self.mark_safe(the_safe)
        for the_mine in new_mines:
            self.mark_mine(the_mine)

        self.clean_up()
        return new_safes or new_mines

    def add_new_sentences(self):
        """
        Infers New Sentences from the knowledge base and adds them
        """
        new_knowledge = []
        for set1, set2 in itertools.permutations(self.knowledge, 2):
            if set1.cells < set2.cells:
                # Makes sure knowledge isn't already in self.knowledge,
                # avoids infinite re-adding of same sentence edge-case
                if Sentence(set2.cells - set1.cells, set2.count - set1.count) not in self.knowledge:
                    print("_____________________")
                    print("ADDING NEW KNOWLEDGE")
                    print("_____________________")
                    new_knowledge.append(Sentence(set2.cells - set1.cells, set2.count - set1.count))
        self.knowledge.extend(new_knowledge)
        return bool(new_knowledge)

    def get_neighbours(self, cell, count):
        """
        returns a set of the valid (i.e. state ambiguous) neighbours of cell
        as well as the associated count, adjusted for removed mines
        """
        # i is row number and 0th element in cell
        minimum_i = max(cell[0]-1, 0)
        maximum_i = min(cell[0]+1, self.height-1)

        # j is column number and 1st element in cell
        minimum_j = max(cell[1]-1, 0)
        maximum_j = min(cell[1]+1, self.width-1)

        neighbours = set()
        for i in range(minimum_i, maximum_i+1):
            for j in range(minimum_j, maximum_j+1):
                neighbours.add((i, j))

        # Remove all neighbours whose state is already known
        # And adjust count for each already known mine
        neighbours -= self.safes
        for neighbour in neighbours:
            if neighbour in self.mines:
                count -= 1
        neighbours -= self.mines

        return neighbours, count

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves = self.safes - self.moves_made

        return safe_moves.pop() if safe_moves else None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        print("Making Random Move")
        universe = set(itertools.product(range(self.height), range(self.width)))
        valid_moves = universe - self.moves_made - self.mines

        return random.choice(list(valid_moves)) if valid_moves else None
