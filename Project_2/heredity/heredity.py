import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():
    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    print("People = ", people)
    print("Probabilities = ", probabilities)


    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue
    
            # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # Initializing at 1 will not have any affect on
    # the calculation as it consists solely of multiplications
    joint_prob = 1
    for person in people:
        if person in two_genes:
            num_genes = 2
        elif person in one_gene:
            num_genes = 1
        else:
            num_genes = 0

        father = people[person]["father"]
        mother = people[person]["mother"]

        # 1st account for probability of either exhibiting / not exhibiting trait
        if person in have_trait:
            joint_prob *= PROBS["trait"][num_genes][True]
        else:
            joint_prob *= PROBS["trait"][num_genes][False]

        # Then account for probability of number of genes
        # Case 1: person has no parents, use unconditional Probability
        if not father and not mother:
            joint_prob *= PROBS["gene"][num_genes]

        # Case 2: person has parents, prob conditional on Number of genes of Parents
        else:
            prob_to_pass = {father: 0.0, mother: 0.0}
            for the_parent in prob_to_pass:
                if the_parent in two_genes:
                    prob_to_pass[the_parent] = 1.0 - PROBS["mutation"]
                    # no need to account for mutation as it cancels out
                elif the_parent in one_gene:
                    prob_to_pass[the_parent] = 0.5
                else:
                    prob_to_pass[the_parent] = PROBS["mutation"]

            # Inherits gene from both Parents
            if num_genes == 2:
                joint_prob *= prob_to_pass[father] * prob_to_pass[mother]
            # Inherits gene from one parent, but not the other
            elif num_genes == 1:
                joint_prob *= (
                    prob_to_pass[father] * (1 - prob_to_pass[mother])
                    + prob_to_pass[mother] * (1 - prob_to_pass[father])
                    )
            # Does not Inherit the gene
            else:
                joint_prob *= (1 - prob_to_pass[father]) * (1 - prob_to_pass[mother])
    print(joint_prob)
    return joint_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p

        if person in two_genes:
            probabilities[person]["gene"][2] += p
        elif person in one_gene:
            probabilities[person]["gene"][1] += p
        else:
            probabilities[person]["gene"][0] += p




def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        trait_sum = sum(probabilities[person]["trait"].values())
        gene_sum = sum(probabilities[person]["gene"].values())
        for gene_num in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene_num] /= gene_sum

        for has_trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][has_trait] /= trait_sum

if __name__ == "__main__":
    main()
