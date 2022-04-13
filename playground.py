# import twitterbot
# import geocoder
# import process
import pandas as pd
import predict

# cs_1 = "Chicago, IL"
# g = geocoder.google('Mountain View, CA')
# print(g.json)

# state = "New York"
# fips_df = pd.read_csv("fips2county.tsv", sep='\t')
# state_abbr = fips_df.loc[fips_df["StateName"] == state]["StateAbbr"].iloc[0]
# sc = "AL | BIBB"
# fips = fips_df.loc[fips_df["STATE_COUNTY"] == sc]["CountyFIPS"].iloc[0]
#
#
# state_abbr = fips_df.loc[fips_df["StateName"] == "District of Columbia"]["StateAbbr"].iloc[0]
# print(state_abbr)
#
# filepath = "data/train/countypres_2000-2020.csv"
# df = pd.read_csv(filepath, usecols=["county_fips", "party", "candidatevotes", "totalvotes"])
# print(df.iloc[0]["county_fips"])

# l = ['chrisjollyhale', 'tnsseans', 'let', 'walk', 'walk', 'amp', 'ask', 'dnc', 'tndp', 'recruit', 'candidates', 'run', 'u', 's', 'senate', 'rep']
#
#
# clf, v= predict.train_svm()
#
# print(predict.predict(clf,v, l))

# df = pd.read_csv("data/result/Predict_counties.csv").dropna()
df = pd.read_csv("data/result/Predict_counties.csv").dropna()

m = df.groupby("FIPS")["Pred"].mean()
m.to_csv("county_mean.csv")
