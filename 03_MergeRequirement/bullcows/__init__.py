import textdistance

def bullcows(guess: str, solution: str) -> (int, int):
    bulls = textdistance.hamming.similarity(guess, solution)
    cows = textdistance.sorensen_dice(guess, solution) * len(solution) - bulls
    return (bulls, int(cows))
