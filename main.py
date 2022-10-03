# Data model = [N] where N is the number of queens. Each array value represents the row queen i is in for column i
# In possibilities, pos = [N] where the list of possible rows is represented by a string


char_code_1 = 49   # chr(49) is '1'


N = 8

alphabet = ''.join([chr(i) for i in range(char_code_1, char_code_1 + N)])




def create_possibilities(N):
    pos = [alphabet for i in range(0, N)]
    return pos


def print_potential_chess_board(pos):
    N = len(pos)

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
            pos[j] = pos[j].replace(c, '')
            to_propagate = True

        # South-east diagonal
        o = _o - (j0 - j)
        cd = chr(char_code_1 + o)

        if o >= 0 and o < N and cd in pos[j]:
            pos[j] = pos[j].replace(cd, '')
            to_propagate = True

        # North-east diagonal
        o = _o + (j0 - j)
        cd = chr(char_code_1 + o)

        if o >= 0 and o < N and cd in pos[j]:
            pos[j] = pos[j].replace(cd, '')
            to_propagate = True

        if len(pos[j]) == 1 and to_propagate:
            if propagate(pos, j) is None:
                return None

    return pos



pos = create_possibilities(N)

print_potential_chess_board(pos)

pos[2] = '5'
pos[5] = '12'

print_potential_chess_board(pos)
print(pos)

pos = propagate(pos, 2)

print_potential_chess_board(pos)
print(pos)

