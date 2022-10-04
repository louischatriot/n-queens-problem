# Data model = [N] where N is the number of queens. Each array value represents the row queen i is in for column i
# In possibilities, pos = [N] where the list of possible rows is represented by a string

import time
from random import randrange

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




def search(pos):
    N = len(pos)

    sizes = list(map(len, pos))

    if min(sizes) == 0:
        return None

    if max(sizes) == 1:
        return pos

    # Starting with column with the least number of possibilities but not 1
    sizes = list(map(lambda l: N if l == 1 else l, sizes))
    j0 = sizes.index(min(sizes))

    for c in pos[j0]:
        _pos = clone_pos(pos)
        _pos[j0] = c

        if propagate(_pos, j0):
            res = search(_pos)
            if res is not None:
                return res

    return None


def solve_n_queens(N, fixed_queen):
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
        empty_slots = N + 1

    empty_step = N // empty_slots
    if empty_step > 0:
        for p in range(0, N):
            if p % empty_step != 0 and p != j:
                try:
                    chosen = randrange(0, len(pos[p]))
                except ValueError:
                    # Could not place this random queen, dismiss and move on to the next
                    continue

                pos[p] = pos[p][chosen]
                propagate(pos, p)

    res = search(pos)

    if res is None:
        return None

    # Transform into expected string format
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









start = time.time()

res = solve_n_queens(104, (86, 51))

print(res)

duration2 = time.time() - start
print(f"======> Duration backtracking: {duration2}")







