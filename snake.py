import curses
import random
import time

# Game configuration
HEIGHT = 20
WIDTH = 40
DELAY = 0.1  # seconds

# Directions
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    snake = [(HEIGHT // 2, WIDTH // 2 + i) for i in range(3)][::-1]
    direction = RIGHT
    food = place_food(snake)
    score = 0

    while True:
        # Input
        key = stdscr.getch()
        if key in [curses.KEY_UP, ord('w')] and direction != DOWN:
            direction = UP
        elif key in [curses.KEY_DOWN, ord('s')] and direction != UP:
            direction = DOWN
        elif key in [curses.KEY_LEFT, ord('a')] and direction != RIGHT:
            direction = LEFT
        elif key in [curses.KEY_RIGHT, ord('d')] and direction != LEFT:
            direction = RIGHT
        elif key in [ord('q'), 27]:  # q or ESC to quit
            break

        # Move snake
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, head)

        # Check collisions
        if (head[0] in [0, HEIGHT-1] or head[1] in [0, WIDTH-1] or head in snake[1:]):
            break

        # Check food
        if head == food:
            score += 1
            food = place_food(snake)
        else:
            snake.pop()

        # Draw
        stdscr.clear()
        stdscr.border()
        stdscr.addstr(0, 2, f'Score: {score}')
        stdscr.addch(food[0], food[1], '*')
        for y, x in snake:
            stdscr.addch(y, x, '#')
        stdscr.refresh()
        time.sleep(DELAY)

    stdscr.nodelay(False)
    stdscr.addstr(HEIGHT // 2, WIDTH // 2 - 5, 'Game Over!')
    stdscr.addstr(HEIGHT // 2 + 1, WIDTH // 2 - 7, f'Final Score: {score}')
    stdscr.addstr(HEIGHT // 2 + 3, WIDTH // 2 - 9, 'Press any key to exit')
    stdscr.getch()

def place_food(snake):
    while True:
        y = random.randint(1, HEIGHT-2)
        x = random.randint(1, WIDTH-2)
        if (y, x) not in snake:
            return (y, x)

if __name__ == '__main__':
    curses.wrapper(main)
