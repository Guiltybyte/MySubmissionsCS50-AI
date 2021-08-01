from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
        # Can be either a knight or a knave But can only be one
        Biconditional(AKnight, Not(AKnave)),

        # A is a Knight if and only if A is both a knave and a knight
        Biconditional(AKnight, And(AKnave, AKnight))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
        # Can be either a knight or a knave But can only be one
        Biconditional(AKnight, Not(AKnave)),
        Biconditional(BKnight, Not(BKnave)),

        # A is a knight,if and only if both A and B will be Knaves
        Biconditional(AKnight, And(AKnave, BKnave))
        #B is silent
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
        # Can be either a knight or a knave But can only be one
        Biconditional(AKnight, Not(AKnave)),
        Biconditional(BKnight, Not(BKnave)),

        # A is a Knight if and only if, A and B are both Knights, or A and B are both Knaves
        Biconditional(
            AKnight,
            Or(And(AKnight, BKnight), And(AKnave, BKnave))
            ),
        # B is a Knight if and only if, either A is a Knight and B is a Knave or vice versa
        Biconditional(
            BKnight,
            Or(And(AKnight, BKnave), And(AKnave, BKnight))
            )
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
        # Can be either a knight or a knave But can only be one
        Biconditional(AKnight, Not(AKnave)),
        Biconditional(BKnight, Not(BKnave)),
        Biconditional(CKnight, Not(CKnave)),

        # A says either they are a knight or a they are a knave (dont know which)
        Or(
            Biconditional(AKnight, AKnight),
            Biconditional(AKnave, AKnight)
            ),
        # B is a knight if and only if A told the truth by saying "I am a knave" 
        # And if and only if C is a knave
        And(
            Biconditional(
                BKnight,
                Biconditional(AKnight, AKnave)
                ),
            Biconditional(BKnight, CKnave),
            ),
        # C is a Knight if and only if A is a knight
        Biconditional(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
