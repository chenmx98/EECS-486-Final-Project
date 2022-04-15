import csv
import pandas as pd

def process_validation(model_data):
    file = open('data/train/countypres_2000-2020.csv')
    csvreader = csv.reader(file)
    rows = []
    for row in csvreader:
        rows.append(row)
    # print(rows)
    county_winner = {}

    for i in range(1, len(rows) - 4, 4):
        if rows[i][9] > rows[i + 1][9]:
            # 3 is name, 4 is flip
            
            county_winner[rows[i][4]] = "DEMOCRAT"
        else:
            county_winner[rows[i][4]] = "REPUBLICAN"
    

    accuracy = 0
    num_county = 0
    # print(model_data)
    for (fip,c) in model_data:
        # print(i)
        j = int(fip)
        if (j == -1 or j == 0):
            continue
        if c == county_winner[str(j)]:
            accuracy += 1
        num_county += 1
    print(accuracy)
    print(num_county)
    return accuracy / num_county



if __name__ == '__main__':

    # df = pd.read_csv("Predict_counties.csv").dropna()
    df = pd.read_csv("data/result/prediction_bert.csv").dropna()
    ls = []
    for index, row in df.iterrows():
        if (row["Pred"] == 0):
            ls.append((row["FIPS"], "REPUBLICAN"))
        else:
            ls.append((row["FIPS"], "DEMOCRAT"))
    # print(ls)
    accuracy = process_validation(ls)
    print(accuracy)
    # print(accuracy)