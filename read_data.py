import pandas as pd

def view_csv(file_path):
    df = pd.read_csv(file_path)
    print("Columns:", df.columns.tolist())
    print(df.head(3))

if __name__ == "__main__":
    view_csv("biorXiv_license.csv")
