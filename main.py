 
import pygame
import sys
from questions import questions

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # For sound effects

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Load sounds (place files in assets/)
correct_sound = pygame.mixer.Sound("assets/correct_sound.wav")
wrong_sound = pygame.mixer.Sound("assets/wrong_sound.wav")

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quiz Game")
font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 40, bold=True)
clock = pygame.time.Clock()

# Game variables
current_question = 0
score = 0
timer = 30  # 30 seconds per question

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def show_question():
    screen.fill(WHITE)
    question_data = questions[current_question]
    
    # Display question
    draw_text(question_data["question"], title_font, BLACK, 50, 50)
    
    # Display options
    for i, option in enumerate(question_data["options"]):
        draw_text(f"{i+1}. {option}", font, BLUE, 50, 150 + i * 50)
    
    # Display timer
    draw_text(f"Time Left: {timer}", font, RED, 600, 50)

def check_answer(selected_option):
    global score, current_question, timer
    correct_answer = questions[current_question]["answer"]
    selected_answer = questions[current_question]["options"][selected_option]
    
    if selected_answer == correct_answer:
        score += 1
        correct_sound.play()
        draw_text("Correct!", title_font, GREEN, 50, 400)
    else:
        wrong_sound.play()
        draw_text(f"Wrong! Correct: {correct_answer}", title_font, RED, 50, 400)
    
    pygame.display.update()
    pygame.time.delay(2000)  # Pause for feedback
    current_question += 1
    timer = 30  # Reset timer

def game_loop():
    global current_question, score, timer
    running = True
    start_ticks = pygame.time.get_ticks()  # Timer start
    
    while running:
        # Timer logic
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        timer = max(0, 30 - seconds_passed)
        
        if timer == 0:
            check_answer(-1)  # Force wrong answer
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_4:
                    check_answer(event.key - pygame.K_1)
        
        # Render
        if current_question < len(questions):
            show_question()
        else:
            screen.fill(WHITE)
            draw_text(f"Game Over! Score: {score}/{len(questions)}", title_font, BLACK, 50, 50)
            pygame.display.update()
            pygame.time.delay(3000)
            running = False
        
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    game_loop()
    pygame.quit()
    sys.exit()