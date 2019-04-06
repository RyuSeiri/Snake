from SnakeGame import *
import sys
import importlib
import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-eval', dest = 'evaluation', action = 'store_true', default = False)
    parser.add_argument('-ai', dest='ai', default = None)
    args = parser.parse_args()
    if args.ai:
        ai = importlib.import_module(args.ai)
    else:
        ai = None
    if args.evaluation:
        app = Evaluator(height = 24, width = 32, ai = ai, config = None)
        app.Evaluate()
    else:
        app = Frame(height = 480, width = 640, ai = ai, speed = 40)
        app.Show()
    sys.exit(0)
