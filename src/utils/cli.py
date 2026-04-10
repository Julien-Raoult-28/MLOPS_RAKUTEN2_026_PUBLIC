#python -m src.utils.cli --mode fast
#python -m src.utils.cli --mode full



import argparse
from src.models.train import train

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["fast", "full"], default="fast")
    return parser.parse_args()

def main():
    args = parse_args()
    train(mode=args.mode)

if __name__ == "__main__":
    main()