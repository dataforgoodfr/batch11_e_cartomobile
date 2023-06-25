### This file is for IEA data preparation on world and European EV registrations and forecast.
### The final data are to be used for visualization

import pandas as pd

### Raw data are uploaded in Git repo
hist_path = "e_cartomobile/data_extract/data_for_viz/IEA-EV-dataEV salesCarsHistorical.csv"
steps_path = "e_cartomobile/data_extract/data_for_viz/IEA-EV-dataEV salesCarsProjection-STEPS.csv"

df_hist = pd.read_csv(hist_path)
df_steps = pd.read_csv(steps_path)

hist_w = df_hist.loc[df_hist.region == 'World']
steps_w = df_steps.loc[df_steps.region == 'World']

hist_eu = df_hist.loc[df_hist.region == 'Europe']
steps_eu = df_steps.loc[df_steps.region == 'Europe']

df_w = pd.concat([hist_w, steps_w])
df_eu = pd.concat([hist_eu, steps_eu])