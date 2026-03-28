"""
4-Gram Language Model for Next Word Prediction
Usage:
  Build and save:  python fourgram_model.py <text_file> --save model.pkl
  Load and run:    python fourgram_model.py --load model.pkl
"""

import sys
import re
import pickle
from collections import defaultdict, Counter


def load_text(filepath: str) -> str:
    """Load text from a .txt file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def tokenize(text: str) -> list[str]:
    """Lowercase and split text into word tokens, stripping punctuation."""
    text = text.lower()
    tokens = re.findall(r"\b[a-z']+\b", text)
    return tokens


def build_fourgram_model(tokens: list[str]) -> tuple[dict, set]:
    """
    Build a 4-gram model and collect the vocabulary.
    Returns:
      model: dict mapping trigram context -> Counter of next words
      vocab: set of all unique tokens
    """
    model = defaultdict(Counter)
    for i in range(len(tokens) - 3):
        context = (tokens[i], tokens[i + 1], tokens[i + 2])
        next_word = tokens[i + 3]
        model[context][next_word] += 1
    vocab = set(tokens)
    return model, vocab


def predict_next(
    model: dict,
    vocab: set,
    w1: str,
    w2: str,
    w3: str,
    top_n: int = 5,
    alpha: float = 1.0,
) -> list[tuple]:
    """
    Given a 3-word context, return the top_n predicted next words with
    Laplace-smoothed probabilities.

    P(w | context) = (count(context, w) + alpha) / (count(context) + alpha * |V|)

    Args:
      model:  the 4-gram model
      vocab:  set of all known words (used for smoothing denominator)
      w1, w2, w3: the 3-word context
      top_n:  number of predictions to return
      alpha:  smoothing parameter (1.0 = Laplace, 0 = no smoothing)
    Returns:
      list of (word, smoothed_probability) tuples, sorted by probability desc
    """
    context = (w1.lower(), w2.lower(), w3.lower())
    counter = model.get(context, Counter())
    total = sum(counter.values())
    V = len(vocab)

    # With smoothing, every vocab word gets a non-zero probability,
    # so we score all vocab words and return the top_n.
    scored = {
        word: (counter.get(word, 0) + alpha) / (total + alpha * V)
        for word in vocab
    }
    top = sorted(scored.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return top


def save_model(model: dict, vocab: set, filepath: str):
    """Save the 4-gram model and vocabulary to a file using pickle."""
    with open(filepath, "wb") as f:
        pickle.dump({"model": model, "vocab": vocab}, f)
    print(f"Model saved to: {filepath}")


def load_model(filepath: str) -> tuple[dict, set]:
    """Load a saved 4-gram model and vocabulary from a pickle file."""
    with open(filepath, "rb") as f:
        data = pickle.load(f)
    model, vocab = data["model"], data["vocab"]
    print(f"Model loaded from: {filepath} ({len(model):,} trigram contexts, vocab size {len(vocab):,})")
    return model, vocab


def interactive_mode(model: dict, vocab: set, alpha: float = 1.0):
    """Run an interactive prompt for next-word prediction."""
    print("\n4-Gram Next Word Predictor (Laplace smoothing, alpha={})".format(alpha))
    print("Enter 3 words to get predictions. Type 'quit' to exit.\n")
    while True:
        user_input = input("Enter 3 words: ").strip()
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        words = user_input.lower().split()
        if len(words) != 3:
            print("  Please enter exactly 3 words.\n")
            continue
        predictions = predict_next(model, vocab, *words, alpha=alpha)
        print(f"  Top predictions after '{' '.join(words)}':")
        for word, prob in predictions:
            print(f"    {word:<20} {prob:.4%}")
        print()


def main():
    args = sys.argv[1:]

    # Parse optional --alpha flag
    alpha = 1.0
    if "--alpha" in args:
        idx = args.index("--alpha")
        if idx + 1 >= len(args):
            print("Error: --alpha requires a numeric value.")
            sys.exit(1)
        try:
            alpha = float(args[idx + 1])
        except ValueError:
            print("Error: --alpha value must be a number.")
            sys.exit(1)
        args = args[:idx] + args[idx + 2:]  # remove --alpha and its value

    # -- Load mode: python fourgram_model.py --load model.pkl [--alpha 0.5]
    if "--load" in args:
        idx = args.index("--load")
        if idx + 1 >= len(args):
            print("Error: --load requires a file path.")
            sys.exit(1)
        model, vocab = load_model(args[idx + 1])
        interactive_mode(model, vocab, alpha=alpha)
        return

    # -- Build mode: python fourgram_model.py <text_file> [--save model.pkl] [--alpha 0.5]
    if not args:
        print("Usage:")
        print("  Build and save:  python fourgram_model.py <text_file> --save model.pkl [--alpha 0.5]")
        print("  Load and run:    python fourgram_model.py --load model.pkl [--alpha 0.5]")
        sys.exit(1)

    filepath = args[0]
    print(f"Loading text from: {filepath}")
    text = load_text(filepath)

    tokens = tokenize(text)
    print(f"Tokenized {len(tokens):,} words.")

    if len(tokens) < 4:
        print("Error: Text is too short to build a 4-gram model (need at least 4 words).")
        sys.exit(1)

    model, vocab = build_fourgram_model(tokens)
    print(f"Built 4-gram model with {len(model):,} unique trigram contexts, vocab size {len(vocab):,}.")

    # Optionally save
    if "--save" in args:
        idx = args.index("--save")
        if idx + 1 >= len(args):
            print("Error: --save requires a file path.")
            sys.exit(1)
        save_model(model, vocab, args[idx + 1])

    interactive_mode(model, vocab, alpha=alpha)


if __name__ == "__main__":
    main()