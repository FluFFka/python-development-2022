import textdistance
from random import choice

def bullscows(guess: str, solution: str) -> (int, int):
    bulls = textdistance.hamming.similarity(guess, solution)
    cows = textdistance.sorensen_dice(guess, solution) * len(solution) - bulls
    return (bulls, int(cows))

def ask(hint: str, words: list[str] = None) -> str:
    guess = input(hint)
    if words and len(words) > 0:
        while guess not in words:
            print("Word is not from dictionary.")
            guess = input(hint)
    return guess

def inform(fmt: str, bulls: int, cows: int) -> None:
    print(fmt.format(bulls, cows))

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    attempts = 0
    solution = choice(words)
    words.remove(solution)
    while True:
        guess = ask("Input word: ", words)
        attempts += 1
        result = bullscows(guess, solution)
        inform("Bulls: {}, Cows: {}", *result)
        if result[0] == len(solution):
            return attempts
