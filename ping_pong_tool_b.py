"""
Ping-Pong game using Python's turtle module.
Left paddle: W/S keys. Right paddle: Up/Down arrow keys.
"""

import turtle
import time

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_SPEED = 25
BALL_SPEED = 8
BALL_SIZE = 20
WALL_MARGIN = 50

# Colors
BG_COLOR = "black"
PADDLE_COLOR = "white"
BALL_COLOR = "white"
TEXT_COLOR = "white"


def create_paddle(x_pos):
    """Create and return a paddle at the given x position."""
    paddle = turtle.Turtle()
    paddle.speed(0)
    paddle.shape("square")
    paddle.color(PADDLE_COLOR)
    paddle.shapesize(stretch_wid=PADDLE_HEIGHT / 20, stretch_len=PADDLE_WIDTH / 20)
    paddle.penup()
    paddle.goto(x_pos, 0)
    return paddle


def create_ball():
    """Create and return the ball."""
    ball = turtle.Turtle()
    ball.speed(0)
    ball.shape("circle")
    ball.color(BALL_COLOR)
    ball.penup()
    ball.goto(0, 0)
    return ball


def create_score_display():
    """Create and return the score display turtle."""
    pen = turtle.Turtle()
    pen.speed(0)
    pen.color(TEXT_COLOR)
    pen.penup()
    pen.hideturtle()
    pen.goto(0, SCREEN_HEIGHT // 2 - 60)
    return pen


def update_score_display(pen, left_score, right_score):
    """Update the score text on screen."""
    pen.clear()
    pen.write(
        f"Left: {left_score}  |  Right: {right_score}",
        align="center",
        font=("Courier", 24, "bold"),
    )


def main():
    screen = turtle.Screen()
    screen.title("Ping-Pong")
    screen.bgcolor(BG_COLOR)
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.tracer(0)

    # Create paddles
    left_paddle = create_paddle(-SCREEN_WIDTH // 2 + PADDLE_WIDTH)
    right_paddle = create_paddle(SCREEN_WIDTH // 2 - PADDLE_WIDTH)

    # Create ball
    ball = create_ball()

    # Score
    left_score = 0
    right_score = 0
    score_pen = create_score_display()
    update_score_display(score_pen, left_score, right_score)

    # Ball velocity
    ball_dx = BALL_SPEED
    ball_dy = BALL_SPEED

    # Paddle movement
    def left_paddle_up():
        y = left_paddle.ycor()
        if y < SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2 - WALL_MARGIN:
            left_paddle.sety(y + PADDLE_SPEED)

    def left_paddle_down():
        y = left_paddle.ycor()
        if y > -SCREEN_HEIGHT // 2 + PADDLE_HEIGHT // 2 + WALL_MARGIN:
            left_paddle.sety(y - PADDLE_SPEED)

    def right_paddle_up():
        y = right_paddle.ycor()
        if y < SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2 - WALL_MARGIN:
            right_paddle.sety(y + PADDLE_SPEED)

    def right_paddle_down():
        y = right_paddle.ycor()
        if y > -SCREEN_HEIGHT // 2 + PADDLE_HEIGHT // 2 + WALL_MARGIN:
            right_paddle.sety(y - PADDLE_SPEED)

    # Keyboard bindings
    screen.listen()
    screen.onkeypress(left_paddle_up, "w")
    screen.onkeypress(left_paddle_down, "s")
    screen.onkeypress(right_paddle_up, "Up")
    screen.onkeypress(right_paddle_down, "Down")

    # Paddle hit boxes (half-width, half-height for collision)
    paddle_half_w = PADDLE_WIDTH / 2
    paddle_half_h = PADDLE_HEIGHT / 2

    def game_loop():
        nonlocal ball_dx, ball_dy, left_score, right_score

        # Move ball
        ball.setx(ball.xcor() + ball_dx)
        ball.sety(ball.ycor() + ball_dy)

        # Top and bottom wall bounce
        if ball.ycor() > SCREEN_HEIGHT // 2 - BALL_SIZE - WALL_MARGIN:
            ball.sety(SCREEN_HEIGHT // 2 - BALL_SIZE - WALL_MARGIN)
            ball_dy *= -1
        if ball.ycor() < -SCREEN_HEIGHT // 2 + BALL_SIZE + WALL_MARGIN:
            ball.sety(-SCREEN_HEIGHT // 2 + BALL_SIZE + WALL_MARGIN)
            ball_dy *= -1

        # Left paddle collision
        if (
            ball.xcor() < -SCREEN_WIDTH // 2 + PADDLE_WIDTH + BALL_SIZE
            and ball_dx < 0
            and left_paddle.ycor() - paddle_half_h - BALL_SIZE / 2
            < ball.ycor()
            < left_paddle.ycor() + paddle_half_h + BALL_SIZE / 2
        ):
            ball.setx(-SCREEN_WIDTH // 2 + PADDLE_WIDTH + BALL_SIZE)
            ball_dx *= -1

        # Right paddle collision
        if (
            ball.xcor() > SCREEN_WIDTH // 2 - PADDLE_WIDTH - BALL_SIZE
            and ball_dx > 0
            and right_paddle.ycor() - paddle_half_h - BALL_SIZE / 2
            < ball.ycor()
            < right_paddle.ycor() + paddle_half_h + BALL_SIZE / 2
        ):
            ball.setx(SCREEN_WIDTH // 2 - PADDLE_WIDTH - BALL_SIZE)
            ball_dx *= -1

        # Left wall (right scores)
        if ball.xcor() < -SCREEN_WIDTH // 2:
            right_score += 1
            update_score_display(score_pen, left_score, right_score)
            ball.goto(0, 0)
            ball_dx = BALL_SPEED
            ball_dy = BALL_SPEED
            time.sleep(0.5)

        # Right wall (left scores)
        if ball.xcor() > SCREEN_WIDTH // 2:
            left_score += 1
            update_score_display(score_pen, left_score, right_score)
            ball.goto(0, 0)
            ball_dx = -BALL_SPEED
            ball_dy = BALL_SPEED
            time.sleep(0.5)

        screen.update()
        screen.ontimer(game_loop, 20)

    game_loop()
    turtle.done()


if __name__ == "__main__":
    main()
