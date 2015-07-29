#!/usr/bin/env python

# References
# http://en.wikipedia.org/wiki/KenKen
# https://docs.python.org/2/library/itertools.html

import argparse
import itertools
import random


def check_board(board, cardinality):
    rows = [set() for i in xrange(cardinality)]
    cols = [set() for i in xrange(cardinality)]
    for position, item in enumerate(board):
        row = position / cardinality
        col = position % cardinality
        rows[row].add(item)
        cols[col].add(item)
    for row in rows:
        if len(row) != cardinality:
            return False
    for col in cols:
        if len(col) != cardinality:
            return False
    return True


def _get_items(cardinality):
    items = []
    for item in xrange(1, cardinality+1):
        for i in xrange(cardinality):
            items.append(item)
    return items


def _get_boards_permutations(cardinality):
    items = _get_items(cardinality)
    items = ''.join(map(str, items))
    return itertools.permutations(items, len(items))


def _get_boards_random(cardinality):
    items = _get_items(cardinality)
    while True:
        random.shuffle(items)
        yield tuple(items)


def get_boards(cardinality):
    # return _get_boards_permutations(cardinality)
    return _get_boards_random(cardinality)


def get_num_combinations(cardinality, verbose=False):
    results = {
        True: 0,
        False: 0,
    }
    seen = set()
    for i, board in enumerate(get_boards(cardinality), 1):
        if i % 1000000 == 0:
            print "%s / %s checking board %s ..." % (
                results[True],
                results[False],
                i,
            )
        if board in seen:
            continue
        result = check_board(board, cardinality)
        results[result] += 1
        if verbose:
            print board, result
        seen.add(board)
    return results[True], results[False]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cardinality',
                        type=int,
                        help="Number of rows/columns (ie 6)")
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    good, bad = get_num_combinations(args.cardinality, args.verbose)
    print "Number of unique combinations for cardinality %s: %s" % (args.cardinality,
                                                                    good + bad)
    print "Good: %s" % good
    print "Bad: %s" % bad


if __name__ == '__main__':
    main()
