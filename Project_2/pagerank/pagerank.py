import os
import random
import re
import sys
import numpy
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # accounts for case in which there are no links to a page
    if not corpus[page]:
        return dict.fromkeys(corpus.keys(), 1 / len(corpus))

    # adds the 1 - damp factor to all keys
    prob_dist_for_page = dict.fromkeys(corpus.keys(), (1 - damping_factor) / len(corpus))

    # damp factor evenly among linked pages
    for link in corpus[page]:
        prob_dist_for_page[link] += damping_factor / len(corpus[page])

    return prob_dist_for_page


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    estimated_page_rank = dict.fromkeys(corpus.keys(), 0)

    sample = random.choice(list(corpus.keys()))
    estimated_page_rank[sample] += 1 / n

    for dummy in range(1, n):
        model = transition_model(corpus, sample, damping_factor)
        # Numpy is returning sample as a 1 element numpy array, hence the inclusion of 0 index
        sample = numpy.random.choice(
            a=list(model.keys()),
            size=1,
            p=list(model.values())
            )[0]
        estimated_page_rank[sample] += 1 / n
    return estimated_page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    iterated_page_rank = dict.fromkeys(corpus.keys(), 1 / len(corpus))
    prev_rank = dict.fromkeys(corpus.keys(), numpy.inf)
    
    while not has_converged(prev_rank, iterated_page_rank):
        prev_rank = copy.deepcopy(iterated_page_rank)
        for page in corpus:
            link_condition = 0
            for pot_candidate in corpus:
                if page in corpus[pot_candidate]:
                    link_condition += (prev_rank[pot_candidate] / len(corpus[pot_candidate]))
                if not corpus[pot_candidate]:
                    link_condition += (prev_rank[pot_candidate] / len(corpus))
            iterated_page_rank[page] = ((1 - damping_factor) / len(corpus)) + (damping_factor * link_condition)
    return iterated_page_rank

def has_converged(prev_rank, current_rank):
    """
    Checks if all page_rank values have converged (to accuracy within 0.001)
    and returns true if this is the case
    """
    ACCURACY = 0.001
    for prev_val, current_val in zip(prev_rank.values(), current_rank.values()):
        if abs(current_val - prev_val) >= ACCURACY:
            return False
    return True


if __name__ == "__main__":
    main()
