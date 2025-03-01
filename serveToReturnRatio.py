#%%
import pandas as pd

#%%
# raw = pd.read_csv('https://raw.githubusercontent.com/granthohol/Modeling-Tennis-with-Markov-Chains/main/Data/raw_kaggle.csv')
raw = pd.read_csv('Data/raw_kaggle.csv')
ret = pd.read_csv('Data/return_kaggle.csv')
serve = pd.read_csv('Data/serve_kaggle.csv')

# %%
raw = raw[['Name', 'Surface', 'TP']]
raw.head()

# %%
ret = ret[['TPW', 'RPW']]
ret.head()

#%%
serve = serve[['Dr']]
serve.head()

# %%
ratio_data = raw.join(ret)
ratio_data = ratio_data.join(serve)
ratio_data.head()

#%%
ratio_data = ratio_data[ratio_data['RPW'] != '-']
ratio_data = ratio_data[ratio_data['TPW'] != '-']
ratio_data = ratio_data[ratio_data['Dr'] != '-']

ratio_data.shape

# %%
ratio_data.dtypes

# %%
ratio_data['RPW'] = ratio_data['RPW'].str.rstrip('%').astype(float) / 100
ratio_data['TPW'] = ratio_data['TPW'].str.rstrip('%').astype(float) / 100
ratio_data['Dr'] = ratio_data['Dr'].astype(float)

ratio_data['TPW_Int'] = ratio_data['TP'] * ratio_data['TPW']

ratio_data['TPL_Int'] = ratio_data['TP'] * (1 - ratio_data['TPW'])
ratio_data['TPL'] = ratio_data['TPL_Int'] / ratio_data['TP']

ratio_data['SPW'] = ratio_data['Dr'] * ratio_data['TPL']

ratio_data = ratio_data[['Name', 'Surface', 'TP', 'TPW', 'TPW_Int', 'TPL', 'TPL_Int', 'SPW', 'RPW', 'Dr']]

ratio_data.head()


# %%
ratio_data = ratio_data[['Name', 'Surface', 'SPW', 'RPW']]
ratio_data = ratio_data.groupby(["Name", "Surface"], as_index=False).mean()
ratio_data = ratio_data[ratio_data['Surface'] != 'Carpet']
ratio_data.head()

#%%
ratio_data = ratio_data.dropna()

# %%
ratio_data['Golden Ratio'] = ratio_data['SPW'] / ratio_data['RPW']
ratio_data.head()

# %%
ratio_data.to_csv('Data/golden_ratio_data.csv')

# %%
