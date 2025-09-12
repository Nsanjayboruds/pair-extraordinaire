import pygame
import random
import math
import sys


pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Guess the Number")


BACKGROUND = (25, 25, 40)
PRIMARY = (70, 130, 180)
SECONDARY = (220, 120, 100)
ACCENT = (90, 200, 150)
TEXT_COLOR = (240, 240, 240)
HIGHLIGHT = (100, 200, 255)


title_font = pygame.font.SysFont("arial", 48, bold=True)
main_font = pygame.font.SysFont("arial", 28)
small_font = pygame.font.SysFont("arial", 20)


secret_number = random.randint(1, 20)
attempts = 0
max_attempts = 6
feedback = "I'm thinking of a number between 1-20"
input_text = ""
game_state = "playing"  
animation_angle = 0
hint_cooldown = 0
hint_available = True
particles = []

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(3, 8)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-5, -1)
        self.gravity = 0.1
        self.life = 100
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.speed_y += self.gravity
        self.life -= 2
        self.size *= 0.97
        
    def draw(self, surface):
        alpha = min(255, self.life * 2.55)
        color_with_alpha = (*self.color, alpha)
        pygame.draw.circle(surface, color_with_alpha, (int(self.x), int(self.y)), int(self.size))

def draw_input_box():
   
    box_width = 200
    box_height = 50
    box_x = WIDTH // 2 - box_width // 2
    box_y = HEIGHT // 2 + 20
    
    
    border_width = 3 + math.sin(animation_angle * 3) * 1.5
    pygame.draw.rect(screen, HIGHLIGHT, (box_x - border_width, box_y - border_width, 
                                        box_width + border_width*2, box_height + border_width*2), 
                    int(border_width), 10)
    
   
    pygame.draw.rect(screen, (50, 50, 70), (box_x, box_y, box_width, box_height), 0, 8)
    
  
    text_surface = main_font.render(input_text, True, TEXT_COLOR)
    screen.blit(text_surface, (box_x + 10, box_y + 10))
    
   
    if int(animation_angle * 5) % 2 == 0:
        cursor_x = box_x + 15 + text_surface.get_width()
        pygame.draw.line(screen, TEXT_COLOR, (cursor_x, box_y + 10), 
                        (cursor_x, box_y + box_height - 10), 2)

def draw_button(text, rect, color, hover_color, action=None):
    mouse_pos = pygame.mouse.get_pos()
    clicked = False
    
    
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect, 0, 10)
        if pygame.mouse.get_pressed()[0]:
            clicked = True
    else:
        pygame.draw.rect(screen, color, rect, 0, 10)
    
    
    text_surf = small_font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
    
    return clicked

def create_particles(x, y, color, count=10):
    for _ in range(count):
        particles.append(Particle(x, y, color))

def draw_hud():
  
    attempts_text = small_font.render(f"Attempts: {attempts}/{max_attempts}", True, TEXT_COLOR)
    screen.blit(attempts_text, (20, 20))
    
    
    hint_rect = pygame.Rect(WIDTH - 150, 20, 130, 40)
    hint_clicked = draw_button("Get Hint", hint_rect, SECONDARY, (240, 140, 120), hint_available)
    
    return hint_clicked, hint_rect

def draw_feedback():
  
    words = feedback.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        test_width = main_font.size(test_line)[0]
        
        if test_width < WIDTH - 100:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    for i, line in enumerate(lines):
        text_surface = main_font.render(line, True, TEXT_COLOR)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - 60 - (len(lines)-i-1)*35))

def draw_title():
   
    title_shadow = title_font.render("Guess the Number", True, (180, 70, 100))
    title_text = title_font.render("Guess the Number", True, PRIMARY)
    
  
    offset = math.sin(animation_angle) * 3
    screen.blit(title_shadow, (WIDTH//2 - title_text.get_width()//2 + 4, 80 + 4 + offset))
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 80 + offset))

def draw_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    if game_state == "won":
        result_text = title_font.render("You Won!", True, ACCENT)
        message = main_font.render(f"You guessed the number in {attempts} attempts!", True, TEXT_COLOR)
    else:
        result_text = title_font.render("Game Over", True, SECONDARY)
        message = main_font.render(f"The number was {secret_number}. Better luck next time!", True, TEXT_COLOR)
    
    screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, HEIGHT//2 - 80))
    screen.blit(message, (WIDTH//2 - message.get_width()//2, HEIGHT//2 - 10))
    
   
    play_again_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50)
    play_again_clicked = draw_button("Play Again", play_again_rect, ACCENT, (110, 230, 170))
    
    return play_again_clicked

def draw_hint():
   
    if not input_text.isdigit():
        return
    
    guess = int(input_text)
    difference = abs(secret_number - guess)
    
    
    pygame.draw.rect(screen, (60, 60, 80), (WIDTH//2 - 150, HEIGHT - 100, 300, 20), 0, 10)
    
    
    max_diff = 19  
    fill_width = 300 * (1 - difference / max_diff)
    pygame.draw.rect(screen, SECONDARY, (WIDTH//2 - 150, HEIGHT - 100, fill_width, 20), 0, 10)
    
    
    for i in range(0, 11):
        x_pos = WIDTH//2 - 150 + i * 30
        pygame.draw.line(screen, TEXT_COLOR, (x_pos, HEIGHT - 105), (x_pos, HEIGHT - 95), 2)
    
    
    cold_text = small_font.render("Cold", True, TEXT_COLOR)
    hot_text = small_font.render("Hot", True, TEXT_COLOR)
    screen.blit(cold_text, (WIDTH//2 - 150 - cold_text.get_width()//2, HEIGHT - 80))
    screen.blit(hot_text, (WIDTH//2 + 150 - hot_text.get_width()//2, HEIGHT - 80))


clock = pygame.time.Clock()
running = True

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if game_state == "playing":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text:
                    if input_text.isdigit():
                        guess = int(input_text)
                        attempts += 1
                        
                        if guess < 1 or guess > 20:
                            feedback = "Please enter a number between 1 and 20!"
                        elif guess < secret_number:
                            feedback = "Too low! Try a higher number."
                            create_particles(WIDTH//2, HEIGHT//2 + 100, (100, 100, 200), 15)
                        elif guess > secret_number:
                            feedback = "Too high! Try a lower number."
                            create_particles(WIDTH//2, HEIGHT//2 + 100, (200, 100, 100), 15)
                        else:
                            feedback = f"🎉 Correct! You guessed it in {attempts} attempts!"
                            game_state = "won"
                            create_particles(WIDTH//2, HEIGHT//2, (100, 200, 100), 50)
                        
                        input_text = ""
                        
                        if attempts >= max_attempts and game_state != "won":
                            game_state = "lost"
                            create_particles(WIDTH//2, HEIGHT//2, (200, 100, 100), 30)
                    
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit() and len(input_text) < 3:
                    input_text += event.unicode
    
    
    animation_angle += 0.02
    
    
    for particle in particles[:]:
        particle.update()
        if particle.life <= 0:
            particles.remove(particle)
    
    
    screen.fill(BACKGROUND)
    
    
    for i in range(20):
        x = (i * 40 + animation_angle * 10) % (WIDTH + 80) - 40
        y = HEIGHT // 3 + math.sin(animation_angle + i * 0.5) * 20
        size = 5 + math.sin(animation_angle + i) * 3
        pygame.draw.circle(screen, (60, 70, 100), (x, y), size)
    
    
    draw_title()
    draw_feedback()
    draw_input_box()
    
    hint_clicked, hint_rect = draw_hud()
    
    
    if hint_clicked and hint_available:
        if secret_number % 2 == 0:
            feedback = f"Hint: The number is even"
        else:
            feedback = f"Hint: The number is odd"
        hint_available = False
        create_particles(hint_rect.centerx, hint_rect.centery, SECONDARY, 20)
    
    
    if input_text.isdigit():
        draw_hint()
    
    
    for particle in particles:
        particle.draw(screen)
    
    
    if game_state in ["won", "lost"]:
        play_again_clicked = draw_game_over()
        if play_again_clicked:
            
            secret_number = random.randint(1, 20)
            attempts = 0
            feedback = "I'm thinking of a number between 1-20"
            input_text = ""
            game_state = "playing"
            hint_available = True
            particles = []
    
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()