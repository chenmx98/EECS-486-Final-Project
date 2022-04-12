import csv

def process_validation(model_data):
    file = open('countypres_2000-2020.csv')
    csvreader = csv.reader(file)
    rows = []
    for row in csvreader:
        rows.append(row)
    # print(rows)
    county_winner = {}

    for i in range(1, len(rows) - 4, 4):
        if rows[i][9] > rows[i + 1][9]:
            # 3 is name, 4 is flip
            county_winner[rows[i][3]] = "DEMOCRAT"
        else:
            county_winner[rows[i][3]] = "REPUBLICAN"
    accuracy = 0
    num_county = 0
    for i in model_data:
        if i in county_winner:
            if model_data[i] == county_winner:
                accuracy += 1
            num_county += 1
    return accuracy / num_county






if __name__ == '__main__':

    accuracy = process_validation()
    print(accuracy)