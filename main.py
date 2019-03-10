from random import shuffle, randrange
import os

maze_size = {'x': 12, 'y': 8}

def make_maze(w=maze_size['x'], h=maze_size['y']):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+--"] * w + ['+'] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                hor[max(y, yy)][x] = "+  "
            if yy == y:
                ver[y][max(x, xx)] = "   "
            walk(xx, yy)

    walk(randrange(w), randrange(h))

    array = []
    for (a, b) in zip(hor, ver):
        array.append(a)
        array.append(b)
    return array


def show_me(current_position, maze, end_location, outtxt):
    clear_screen()  # Clears the terminal of previous input
    display_maze = []
    for item in maze:
        display_maze.append(item)

    end_square = display_maze[end_location['y'] * 2 - 1][end_location['x'] - 1]
    s = list(end_square)
    s[1] = '•'
    display_maze[end_location['y'] * 2 - 1][end_location['x'] - 1] = "".join(s)

    current_square = display_maze[current_position['y'] * 2 - 1][current_position['x'] - 1]
    s = list(current_square)
    s[1] = '#'
    display_maze[current_position['y'] * 2 - 1][current_position['x'] - 1] = "".join(s)

    for row in maze:
        print("".join(row))
    print(outtxt)


def generate_x_mark(maze_size):
    return {'x': maze_size['x'], 'y': maze_size['y']}


def find_finished(current_position, end_location, turns):
    if (current_position['x'] == end_location['x']) and (current_position['y'] == end_location['y']):
        print("You Win! Took you: {} turns".format(turns))
        return False
    else:
        return True


def valid_moves(current_position, maze):
    """Function to check your current location and give a list of valid moves"""
    valid_moves_list = []
    open_spaces = {
        'n': ['+  ', '|  ', '   ']
        , 's': ['+  ', '|  ', '   ']
        , 'e': ['   ', ' • ']
        , 'w': ['   ', '|  ', ' • ', '|• ']}

    if current_position['y'] != 1 \
            and maze[current_position['y'] * 2 - 2][current_position['x'] - 1] in open_spaces['n'] \
            and '#' not in maze[current_position['y'] * 2 - 3][current_position['x'] - 1]:
        valid_moves_list.append('n')
    if current_position['y'] != maze_size['y'] \
            and maze[current_position['y'] * 2][current_position['x'] - 1] in open_spaces['s'] \
            and '#' not in maze[current_position['y'] * 2 + 1][current_position['x'] - 1]:
        valid_moves_list.append('s')
    if current_position['x'] != maze_size['x'] \
            and maze[current_position['y'] * 2 - 1][current_position['x']] in open_spaces['e']:
        valid_moves_list.append('e')
    if current_position['x'] != 1 \
            and maze[current_position['y'] * 2 - 1][current_position['x'] - 2] in open_spaces['w'] \
            and '|' not in maze[current_position['y'] * 2 - 1][current_position['x'] - 1]:
        valid_moves_list.append('w')

    return valid_moves_list


def process_move(move, current_position, options):
    rsp = ""
    if move == 'n' and move in options:
        current_position['y'] -= 1
    elif move == 's' and move in options:
        current_position['y'] += 1
    elif move == 'e' and move in options:
        current_position['x'] += 1
    elif move == 'w' and move in options:
        current_position['x'] -= 1
    else:
        rsp = "That was an illegal move, try again"

    return rsp


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("")


def main():
    current_position = {'x': 1, 'y': 1}
    end_location = generate_x_mark(maze_size)

    maze = make_maze()
    txt_for_player = ""
    turns = 0
    while find_finished(current_position, end_location, turns):

        show_me(current_position, maze, end_location, txt_for_player)  # Show the maze
        options = valid_moves(current_position, maze)
        if len(options) == 0:
            print("Game over. Better luck next time.")
            break
        elif len(options) == 1 and turns != 0:
            move = options[0]
        else:
            move = input("Pick a direction ('n', 's', 'e', 'w'): ")
            turns += 1
        if move == 'q':
            print("Thanks for playing!")
            break
        else:
            txt_for_player = process_move(move, current_position, options)


if __name__ == '__main__':
    main()
