import plotly.figure_factory as ff

import numpy as np
import pandas as pd

# df_result = pd.read_csv('data/result/Predict_counties.csv').dropna()
# df_result["Party"] = df_result["Pred"].map({"0":"Republic", "1":"Democrat"})
df_result = pd.read_csv('data/result/county_mean.csv').dropna()


colorscale = ["#f1471d", "#FF9912", "#4b8bbe"]
endpts = [0.45, 0.55]
fips = df_result['FIPS'].tolist()
values = df_result["Pred"].tolist()

fig = ff.create_choropleth(
    fips=fips, values=values,
    binning_endpoints=endpts,
    colorscale=colorscale,
    show_state_data=False,
    show_hover=True, centroid_marker={'opacity': 0},
    asp=2.9, title='Tweet Party Alignment Prediction',
    legend_title='Party (Blank if valid data is missing)',
)

fig.layout.template = None
fig.show()
fig.write_image("map_result.png")