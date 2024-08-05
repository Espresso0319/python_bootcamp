import random

def guess_number_game():
    # Generate a random integer between 0 and 100
    number_to_guess = random.randint(0, 100)
    attempts = 10

    print("Welcome to the Guess the Number game! You have 10 chances to guess a number between 0 and 100.")

    for attempt in range(1, attempts + 1):
        try:
            # Get user input
            guess = int(input(f"Attempt {attempt}: Please enter your guess: "))

            # Check if the guess is correct
            if guess < number_to_guess:
                print("Your guess is too low.")
            elif guess > number_to_guess:
                print("Your guess is too high.")
            else:
                print(f"Congratulations! You guessed it right. The number was {number_to_guess}.")
                return
        except ValueError:
            print("Please enter a valid integer.")

    print(f"Game over. You didn't guess the number. The correct number was {number_to_guess}.")

# Run the game
guess_number_game()
