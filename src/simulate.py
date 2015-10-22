import os
import pandas

toplevel_dir = os.path.join(os.path.dirname(__file__), os.path.pardir)
CSV_FILENAME = os.path.join(toplevel_dir, "data", "projections.csv")

def load_csv(fn):
    return pandas.read_csv(fn)

def main():
    df = load_csv(CSV_FILENAME)

if __name__ == '__main__':
    main()
