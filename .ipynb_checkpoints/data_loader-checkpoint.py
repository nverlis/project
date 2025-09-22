import pandas as pd

FILE_ID = "1i_H46ci0vi-B17v8UKIGfpQeGRpaa2uI"  # ID файла на Google Drive
file_url = f"https://drive.google.com/uc?id={file_id}"

raw_data = pd.read_csv(file_url)     # читаем файл

raw_data.head(10)         # выводим на экран первые 10 строк для проверки