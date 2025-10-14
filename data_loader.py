import pandas as pd

file_id = "1i_H46ci0vi-B17v8UKIGfpQeGRpaa2uI"
file_url = f"https://drive.google.com/uc?id={file_id}"

df = pd.read_csv(file_url)

print('Типы данных до изменения:', df.dtypes)

df[['created_at', 'updated_at']] = df[['created_at', 'updated_at']].apply(
    pd.to_datetime, errors='coerce', utc=True)
df[['state', 'origin', 'carcinogenicity', 'export']] = df[['state', 'origin', 'carcinogenicity', 'export']].astype('category')
df = df.drop(columns=['Unnamed: 0'])

num_cols = ['weight', 'moldb_average_mass', 'moldb_mono_mass', 'logp']
df[num_cols] = df[num_cols].apply(pd.to_numeric, errors='coerce')

text = ['title', 'common_name', 'description', 'appearance',
'solubility', 'route_of_exposure', 'mechanism_of_toxicity', 'metabolism',
'toxicity', 'lethaldose', 'use_source', 'health_effects', 'symptoms', 'treatment']
df[text] = df[text].astype(str)

print('Типы данных после изменения:', df.dtypes)

print(df.shape)
duplicate_rows_df = df[df.duplicated()]
print("number of duplicate rows: ", duplicate_rows_df.shape)
df = df.drop_duplicates()
print(df.shape)
print(df.isnull().sum())

