import pandas as pd
from pathlib import Path

def extract_from_drive(file_id: str, output_dir: str = "data/raw", filename: str = "dataset.csv") -> str:
    file_url = f"https://drive.google.com/uc?id={file_id}"
    df = pd.read_csv(file_url)
    print(f"Загружен датасет: {len(df)} строк, {len(df.columns)} колонок")

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    output_path = Path(output_dir) / filename

    df.to_csv(output_path, index=False)
    print(f"Сырые данные сохранены в: {output_path}")

    return str(output_path)

