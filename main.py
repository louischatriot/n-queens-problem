# Data model = [N] where N is the number of queens. Each array value represents the row queen i is in for column i
# In possibilities, pos = [N] where the list of possible rows is represented by a string

import time
from random import randrange
# from math import factorial

TIMEOUT = 0.15
char_code_1 = 49   # chr(49) is '1' - arbitrary but easier for low N debugging

def create_alphabet(N):
    alphabet = ''.join([chr(i) for i in range(char_code_1, char_code_1 + N)])
    return alphabet


def create_possibilities(N):
    alphabet = create_alphabet(N)
    pos = [alphabet for i in range(0, N)]
    return pos


def print_chess_board(pos):
    N = len(pos)
    alphabet = create_alphabet(N)

    print("==" * N)

    for i in range(0, N):
        l = ''

        for j in range(0, N):
            if alphabet[i] not in pos[j]:
                l += " x"
            elif len(pos[j]) == 1:
                l += " Q"
            else:
                l += " ."

        print(l)

    print("==" * N)


def clone_pos(pos):
    return [c for c in pos]


# Characters in s are ordered so we can use dichotomy
# Actually slower than stro.replace
# Using regex is faster than this but slower than replace even when searching the whole string
# Using translate is much slower
def remove_character(s, c):
    N = len(s)
    if N < 5:
        return s.replace(c, '')

    o = ord(c)
    l = 0
    u = N - 1
    i = N // 2
    while s[i] != c:
        if ord(s[i]) < o:
            l = i
        else:
            u = i

        i = (l + u) // 2

    return s[0:i] + s[(i+1):]


# c = column number
def propagate(pos, j0):
    N = len(pos)

    if len(pos[j0]) == 0:
        return None

    if len(pos[j0]) > 1:
        return pos

    c = pos[j0]
    _o = ord(c) - char_code_1

    for j in range(0, N):
        if j == j0:
            continue

        to_propagate = False

        # Row
        if c in pos[j]:
            pos[j] = pos[j].replace(c, '', 1)
            to_propagate = True

        # South-east diagonal
        o = _o - (j0 - j)
        if o >= 0 and o < N:
            cd = chr(char_code_1 + o)
            if cd in pos[j]:
                pos[j] = pos[j].replace(cd, '', 1)
                to_propagate = True

        # North-east diagonal
        o = _o + (j0 - j)
        if o >= 0 and o < N:
            cd = chr(char_code_1 + o)
            if cd in pos[j]:
                pos[j] = pos[j].replace(cd, '', 1)
                to_propagate = True

        if len(pos[j]) == 1 and to_propagate:
            if propagate(pos, j) is None:
                return None

    return pos




def search(pos, start = None):
    N = len(pos)

    sizes = list(map(len, pos))

    if min(sizes) == 0:
        return None

    if max(sizes) == 1:
        return pos

    if start and time.time() - start > TIMEOUT:
        return None

    # Starting with column with the least number of possibilities but not 1
    sizes = list(map(lambda l: N if l == 1 else l, sizes))
    j0 = sizes.index(min(sizes))

    for c in pos[j0]:
        _pos = clone_pos(pos)
        _pos[j0] = c

        if propagate(_pos, j0):
            res = search(_pos, start)
            if res is not None:
                return res

    return None


def string_rep(res):
    N = len(res)
    s = ''
    for i in range(0, N):
        l = ''

        for j in range(0, N):
            if i == ord(res[j]) - char_code_1:
                l += 'Q'
            else:
                l += '.'

        l += '\n'
        s += l

    return s



def solve_n_queens_backtrack(N, fixed_queen):
    pos = create_possibilities(N)

    # Declaring fixed queen
    alphabet = create_alphabet(N)
    i, j = fixed_queen
    pos[j] = alphabet[i]

    # Place random queens to speed algo up if board is large
    # There are so many solutions it provides a very nice speed up at a low risk
    # We should actually check execution time downstream and stop if it takes too long
    # That, or find a better heuristic for placing our queens
    if N > 500:
        empty_slots = 80
    elif N > 100:
        empty_slots = 40
    else:
        empty_slots = 0

    if empty_slots == 0:
        # No random optimization
        res = search(pos)

        if res is None:
            return None
        else:
            return string_rep(res)

    # For N > 100 there are always solutions so if our initial random placement didn't work we try again
    res = None
    empty_step = N // empty_slots
    while res is None:
        _pos = clone_pos(pos)
        if empty_step > 0:
            for p in range(0, N):
                if p % empty_step != 0 and p != j:
                    try:
                        chosen = randrange(0, len(_pos[p]))
                    except ValueError:
                        # Could not place this random queen, dismiss and move on to the next
                        continue

                    _pos[p] = _pos[p][chosen]
                    propagate(_pos, p)

        res = search(_pos, time.time())

    return string_rep(res)





# Permutation method where each array cell is the column corresponding to the array line
def generate_permutation_with_fixed(N, fi, fj):
    res = [i for i in range(0, N)]

    for i in range(N - 1, 0, -1):
        j = randrange(0, i + 1)
        swp = res[i]
        res[i] = res[j]
        res[j] = swp

    # Ensure fixed queen is in place ; for large N the array stays "random enough"
    if res[fi] != fj:
        i0 = res.index(fj)
        swp = res[fi]
        res[fi] = res[i0]
        res[i0] = swp

    return res


# Format asked by kata is not very legible
def string_rep_permutation(pos, legible = False):
    N = len(pos)
    s = ''
    quanta = '.' + (' ' if legible else '')
    for i in range(0, N):
        l = [quanta] * N + ['\n']
        l[pos[i]] = 'Q' + (' ' if legible else '')
        s += ''.join(l)

    return s


def reset_diags(pos):
    N = len(pos)

    se_diag = [0 for i in range(0, 2 * N - 1)]
    ne_diag = [0 for i in range(0, 2 * N - 1)]

    for i in range(0, N):
        j = pos[i]
        ne_diag[i + j] += 1
        se_diag[N - 1 + j - i] += 1   # True domain is [-N+1, N-1] hence the offset

    return (ne_diag, se_diag)


def solve_n_queens_permutations(N, fi, fj):
    pos = generate_permutation_with_fixed(N, fi, fj)
    ne_diag, se_diag = reset_diags(pos)

    def get_attacks(i1, i2):
        score = sum([0 if i == 0 else i - 1 for i in se_diag]) + sum([0 if i == 0 else i - 1 for i in ne_diag])
        return score

    # Assumes i1 != i2 (and hence j1 != j2)
    # Can have two queens on the same diagonal, but not on the two diagonals at once
    def swap(i1, i2):
        attacks_before = get_attacks(i1, i2)

        swp = pos[i1]
        pos[i1] = pos[i2]
        pos[i2] = swp

        n, s = reset_diags(pos)
        for i in range(0, 2 * N - 1):
            ne_diag[i] = n[i]
            se_diag[i] = s[i]

        attacks_after = get_attacks(i1, i2)

        if attacks_after < attacks_before:
            # Better after swap, keep it
            return 1
        else:
            # Rollback
            swp = pos[i1]
            pos[i1] = pos[i2]
            pos[i2] = swp

            n, s = reset_diags(pos)
            for i in range(0, 2 * N - 1):
                ne_diag[i] = n[i]
                se_diag[i] = s[i]

            return 0

    swaps = 1
    t = 0
    while swaps != 0:
        t += 1
        swaps = 0

        for i1 in range(0, N):
            for i2 in range(i1 + 1, N):
                j1 = pos[i1]
                j2 = pos[i2]

                # One of the queens, at least, is attacked
                if max(ne_diag[i1 + j1], se_diag[N - 1 + j1 - i1], ne_diag[i2 + j2], se_diag[N - 1 + j2 - i2]) >= 2:
                    swaps += swap(i1, i2)

    print("DONE")
    print(max(se_diag))
    print(max(ne_diag))

    return pos



def solve_n_queens(N, fixed_queen):
    fi, fj = fixed_queen

    while True:
        pos = solve_n_queens_permutations(N, fi, fj)
        ne_diag, se_diag = reset_diags(pos)
        if max(ne_diag) == 1 and max(se_diag) == 1:
            break

    s = string_rep_permutation(pos)
    return s






start = time.time()

s = solve_n_queens(200, (4, 1))

# Nice print
# for l in s.split():
    # print(' '.join([c for c in l]))


# res = solve_n_queens(219, (24, 104))

# print(res)

duration2 = time.time() - start
print(f"======> Duration: {duration2}")







