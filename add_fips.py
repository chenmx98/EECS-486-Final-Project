import sys
import csv
import pandas as pd
import preprocess


def add_fips(df):
    fips_df = pd.read_csv("fips2county.tsv", sep='\t')
    df["FIPS"] = ""
    df["State_County"] = ""
    df["State"] = df["State"].fillna("NA")
    for i in range(len(df)):
        state = str(df.loc[i, "State"])
        county = df.loc[i, "County"]

        county = county.replace("ʻ", "")
        county = county.replace("(", "")
        county = county.replace(")", "")
        county = county.replace("Saint", "St.")

        if state == "Puerto Rico":
            # TODO: "Puerto Rico" is not in the list of normal FIPS code
            continue

        if "County" in county:
            county = county[:-7]
            # print(county)

        if county == "District of Columbia":
            state = "District of Columbia"


        fips = -1
        if state != "NA":


            state_abbr = fips_df.loc[fips_df["StateName"] == state]["StateAbbr"].iloc[0]
            state_abbr += " | "
            sc = (state_abbr + county).upper()
            df.loc[i, "State_County"] = sc




            try:
                fips = fips_df.loc[fips_df["STATE_COUNTY"] == sc]["CountyFIPS"].iloc[0]
            except:
                print(fips, sc)
                try:
                    sc += " CITY"
                    fips = fips_df.loc[fips_df["STATE_COUNTY"] == sc]["CountyFIPS"].iloc[0]
                    print("\t Solved by adding city to the end")
                except:
                    print(fips, sc)
                    try:
                        fips = fips = fips_df.loc[fips_df["CountyName"] == county]["CountyFIPS"].iloc[0]
                        print("\t Solved by omit the state label")
                    except:
                        print(fips, county)
        else:
            try:
                fips = fips_df.loc[fips_df["CountyName"] == county]["CountyFIPS"].iloc[0]
            except:
                print(fips, county)
                try:
                    county += " city"
                    fips = fips_df.loc[fips_df["CountyName"] == county]["CountyFIPS"].iloc[0]
                    print("\t Solved by adding city to the end")
                except:
                    print(fips, county)

        df.loc[i,"FIPS"] = fips

    return df


def group_by_fips(df):
    df = df.groupby(['FIPS'])['Text'].apply(' '.join)
    return df

def clean_text(df):
    df["Clean Text"] = ""
    for i in range(len(df)):
        text = df.loc[i, "Text"]
        print(text)
        df.loc[i,"Clean Text"] = preprocess(df.loc[i, "Text"])

    return df


if __name__ == "__main__":
    # df = pd.read_csv("US_tweets_county.csv")
    # df = add_fips(df)
    # df.to_csv("County_with_fips.csv")
    df = pd.read_csv("County_with_fips.csv")
    df = group_by_fips(df)
    print(df[0])
    df = clean_text(df)
    df.to_csv("text_group_by_fips.csv")
