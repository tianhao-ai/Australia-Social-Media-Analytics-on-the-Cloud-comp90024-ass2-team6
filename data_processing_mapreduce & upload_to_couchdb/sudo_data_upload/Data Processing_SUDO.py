import pandas as pd
import matplotlib.pyplot as plt
import json
df = pd.read_csv('../graph_data/EducationLevel_SUDO_after cleaning.csv')
jdf = df.to_json(orient='records')
#records = json.loads(jdf)
with open('../graph_data/EducationLevel_SUDO_after cleaning.json', 'w') as f:
    f.write(jdf)
df['X'] = df.index.values

with open('../graph_data/EducationLevel_SUDO_after cleaning.json', 'r') as f:
    for line in f:
        records = json.loads(jdf)
        
ax = df.plot(x = 'X', y=["Bachelar (%)", ' Postgraduate (%)', "Others (%)"], kind="bar", rot=90, stacked=True)
_ = ax.legend(bbox_to_anchor=(1, 1.02), loc='upper left')
ax.set_xticklabels(df[' gccsa_name_2016'].values.tolist())