import pandas as pd

def extract_from_drive(file_id: str) -> pd.DataFrame:
    file_url = f"https://drive.google.com/uc?id={file_id}"
    df = pd.read_csv(file_url)
    print(f"Загружен датасет из {len(df)} строк и {len(df.columns)} колонок")
    return df