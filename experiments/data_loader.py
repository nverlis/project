import pandas as pd
import re
from pathlib import Path

file_id = "1i_H46ci0vi-B17v8UKIGfpQeGRpaa2uI"
file_url = f"https://drive.google.com/uc?id={file_id}"
df = pd.read_csv(file_url)
df.head(10)

print(df.dtypes) # Типы данных до изменения

def extract_number(value: str) -> float | None:
    if pd.isna(value):
        return None

    s = str(value)
    numbers = re.findall(r"-?\d+(?:\.\d+)?", s)
    if not numbers:
        return None

    if len(numbers) >= 2:
        nums = [float(n) for n in numbers[:2]]
        return sum(nums) / len(nums)

    return float(numbers[0])


def clean_route(value):
    if pd.isna(value):
        return None
    cleaned = re.sub(r"\(.*?\)", "", value)        # убираем всё в скобках
    cleaned = re.sub(r"[\.;]", ",", cleaned)       # заменяем ; и . на запятые
    cleaned = re.sub(r"\s+", " ", cleaned).strip() # убираем лишние пробелы
    return cleaned.lower()


def normalize_carcinogenicity(value):
    if pd.isna(value):
        return None

    s = str(value).lower().strip()

    if re.search(r"\b(1[, ]|group 1|carcinogenic to humans)\b", s):
        return "carcinogenic"

    if re.search(r"\b(2a|2b|possible|probable|suspected)\b", s):
        return "uncertain"

    if re.search(r"\b(3|not classifiable|no indication|non|not carcinogenic)\b", s):
        return "non-carcinogenic"

    return "uncertain"


def csv_from_drive_to_parquet(file_id: str, parquet_filename: str | None = None):

    file_url = f"https://drive.google.com/uc?id={file_id}"
    df = pd.read_csv(file_url)
    print(f"Загружено {len(df)} строк и {len(df.columns)} колонок из Google Drive")

    for col in ["melting_point", "boiling_point"]:
        if col in df.columns:
            before = df[col].notna().sum()
            df[col] = df[col].apply(extract_number)
            after = df[col].notna().sum()
            print(f" {col}: успешно преобразовано {after} из {before} значений")

    if "route_of_exposure" in df.columns:
        df["route_of_exposure"] = df["route_of_exposure"].apply(clean_route)
        print("Колонка 'route_of_exposure' успешно очищена (перезаписана)")

    if "carcinogenicity" in df.columns:
        df["carcinogenicity"] = df["carcinogenicity"].apply(normalize_carcinogenicity)
        print("Колонка 'carcinogenicity' нормализована до трёх категорий")


    numeric_cols = [
        "id", "pubchem_id", "weight", "lethaldose", "min_risk_level",
        "actor_id", "export", "moldb_average_mass", "moldb_mono_mass", "logp"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    datetime_cols = ["created_at", "updated_at"]
    for col in datetime_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")


    string_cols = [
        c for c in df.columns
        if c not in numeric_cols + datetime_cols + ["melting_point", "boiling_point"]
    ]
    df[string_cols] = df[string_cols].astype("string")

    print("Типы данных успешно преобразованы и очищены")

    if parquet_filename is None:
        parquet_filename = Path("converted_data_fixed.parquet")
    else:
        parquet_filename = Path(parquet_filename)

    df.to_parquet(parquet_filename, index=False)
    print(f"Файл сохранён как: {parquet_filename.resolve()}")

    return df

if __name__ == "__main__":
    df = csv_from_drive_to_parquet("1i_H46ci0vi-B17v8UKIGfpQeGRpaa2uI")

print(df.dtypes) # Типы данных после изменения