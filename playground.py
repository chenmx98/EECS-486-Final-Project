import twitterbot
# import geocoder
import process
import pandas as pd

# cs_1 = "Chicago, IL"
# g = geocoder.google('Mountain View, CA')
# print(g.json)

state = "New York"
fips_df = pd.read_csv("fips2county.tsv", sep='\t')
state_abbr = fips_df.loc[fips_df["StateName"] == state]["StateAbbr"].iloc[0]
sc = "AL | BIBB"
fips = fips_df.loc[fips_df["STATE_COUNTY"] == sc]["CountyFIPS"].iloc[0]


state_abbr = fips_df.loc[fips_df["StateName"] == "District of Columbia"]["StateAbbr"].iloc[0]
print(state_abbr)
