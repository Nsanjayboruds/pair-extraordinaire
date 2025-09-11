import random

def guess_the_number():
    """Plays a 'Guess the Number' game."""
    secret_number = random.randint(1, 20)
    attempts = 0
    print("I'm thinking of a number between 1 and 20. Can you guess it?")

    while True:
        try:
            guess_input = input("Take a guess: ").strip()
            
            if not guess_input.isdigit():
                print("Invalid input. Please enter a whole number.")
                continue

            guess = int(guess_input)
            attempts += 1

            if guess < 1 or guess > 20:
                print("Out of bounds! Guess a number between 1 and 20.")
                continue

            if guess < secret_number:
                print("Too low. Try again!")
            elif guess > secret_number:
                print("Too high. Try again!")
            else:
                print(f"🎉 Congratulations! You guessed my number in {attempts} attempt(s)!")
                break

        except KeyboardInterrupt:
            print("\nGame interrupted. Goodbye!")
            break

if __name__ == "__main__":
    guess_the_number()
