import random

def maxime_quote():
    with open("maxime_quote.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()