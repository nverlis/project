# import pandas as pd
# import re
# from pathlib import Path
# import pyarrow
#
#
# def extract_number(value: str) -> float | None:
#     """
#     Извлекает число (или среднее значение из диапазона) из строки с единицами измерения.
#     Примеры:
#         '108.5 - 109°C' → 108.75
#         '> 615°C'       → 615
#         '1040 K(767 °C)'→ 1040
#         '-153.7°C'      → -153.7
#     """
#     if pd.isna(value):
#         return None
#
#     s = str(value)
#
#     # Найдём все числа (включая отрицательные и дробные)
#     numbers = re.findall(r"-?\d+(?:\.\d+)?", s)
#     if not numbers:
#         return None
#
#     # Если диапазон — берём среднее
#     if len(numbers) >= 2:
#         nums = [float(n) for n in numbers[:2]]
#         return sum(nums) / len(nums)
#
#     return float(numbers[0])
#
#
# def csv_from_drive_to_parquet(file_id: str, parquet_filename: str | None = None):
#     """
#     Загружает CSV с Google Drive, преобразует типы данных и сохраняет в Parquet.
#     """
#     # --- 1️⃣ Формируем URL и читаем CSV ---
#     file_url = f"https://drive.google.com/uc?id={file_id}"
#     df = pd.read_csv(file_url)
#     print(f"✅ Загружено {len(df)} строк и {len(df.columns)} колонок из Google Drive")
#
#     # --- 2️⃣ Очистим и преобразуем температуры ---
#     for col in ["melting_point", "boiling_point"]:
#         if col in df.columns:
#             before = df[col].notna().sum()
#             df[col] = df[col].apply(extract_number)
#             after = df[col].notna().sum()
#             print(f"🌡 {col}: успешно преобразовано {after} из {before} значений")
#
#     # --- 3️⃣ Преобразуем остальные числовые колонки ---
#     numeric_cols = [
#         "id", "pubchem_id", "weight", "lethaldose", "min_risk_level",
#         "actor_id", "export", "moldb_average_mass", "moldb_mono_mass", "logp"
#     ]
#     for col in numeric_cols:
#         if col in df.columns:
#             df[col] = pd.to_numeric(df[col], errors="coerce")
#
#     # --- 4️⃣ Преобразуем даты ---
#     datetime_cols = ["created_at", "updated_at"]
#     for col in datetime_cols:
#         if col in df.columns:
#             df[col] = pd.to_datetime(df[col], errors="coerce")
#
#     # --- 5️⃣ Остальные строки ---
#     string_cols = [c for c in df.columns if c not in numeric_cols + datetime_cols + ["melting_point", "boiling_point"]]
#     df[string_cols] = df[string_cols].astype("string")
#
#     print("📊 Типы данных успешно преобразованы")
#
#     # --- 6️⃣ Сохраняем результат ---
#     if parquet_filename is None:
#         parquet_filename = Path("converted_data_fixed.parquet")
#     else:
#         parquet_filename = Path(parquet_filename)
#
#     df.to_parquet(parquet_filename, index=False)
#     print(f"💾 Файл сохранён как: {parquet_filename.resolve()}")
#
#     return df
#
#
# # --- Пример использования ---
# if __name__ == "__main__":
#     df = csv_from_drive_to_parquet("1i_H46ci0vi-B17v8UKIGfpQeGRpaa2uI")

import pandas as pd
import re
from pathlib import Path
import pyarrow


def extract_number(value: str) -> float | None:
    """
    Извлекает число (или среднее значение из диапазона) из строки с единицами измерения.
    Примеры:
        '108.5 - 109°C' → 108.75
        '> 615°C'       → 615
        '1040 K(767 °C)'→ 1040
        '-153.7°C'      → -153.7
    """
    if pd.isna(value):
        return None

    s = str(value)
    numbers = re.findall(r"-?\d+(?:\.\d+)?", s)
    if not numbers:
        return None

    # Если диапазон — берём среднее
    if len(numbers) >= 2:
        nums = [float(n) for n in numbers[:2]]
        return sum(nums) / len(nums)

    return float(numbers[0])


def clean_route(value):
    """
    Очищает колонку route_of_exposure от кодов (в скобках) и лишних символов.
    Пример:
        'Oral (L4); inhalation (L4); dermal (L4)' → 'oral, inhalation, dermal'
    """
    if pd.isna(value):
        return None
    cleaned = re.sub(r"\(.*?\)", "", value)        # убираем всё в скобках
    cleaned = re.sub(r"[\.;]", ",", cleaned)       # заменяем ; и . на запятые
    cleaned = re.sub(r"\s+", " ", cleaned).strip() # убираем лишние пробелы
    return cleaned.lower()


def normalize_carcinogenicity(value):
    """
    Приводит значения carcinogenicity к унифицированным категориям:
    - 'carcinogenic' (включает IARC 1, Group 1 и т.п.)
    - 'possible/uncertain' (включает 2A, 2B, possible, probable)
    - 'non-carcinogenic' (включает not classifiable, no evidence)
    """
    if pd.isna(value):
        return None

    s = str(value).lower().strip()

    # --- приоритет 1: явно канцерогенные ---
    if re.search(r"\b(1[, ]|group 1|carcinogenic to humans)\b", s):
        return "carcinogenic"

    # --- приоритет 2: возможно/вероятно канцерогенные ---
    if re.search(r"\b(2a|2b|possible|probable|suspected)\b", s):
        return "uncertain"

    # --- приоритет 3: не классифицируется / нет данных ---
    if re.search(r"\b(3|not classifiable|no indication|non|not carcinogenic)\b", s):
        return "non-carcinogenic"

    # --- по умолчанию ---
    return "uncertain"


def csv_from_drive_to_parquet(file_id: str, parquet_filename: str | None = None):
    """
    Загружает CSV с Google Drive, очищает и преобразует данные, сохраняет в Parquet.
    """
    # --- 1️⃣ Загружаем CSV ---
    file_url = f"https://drive.google.com/uc?id={file_id}"
    df = pd.read_csv(file_url)
    print(f"✅ Загружено {len(df)} строк и {len(df.columns)} колонок из Google Drive")

    # --- 2️⃣ Очистка и преобразование температур ---
    for col in ["melting_point", "boiling_point"]:
        if col in df.columns:
            before = df[col].notna().sum()
            df[col] = df[col].apply(extract_number)
            after = df[col].notna().sum()
            print(f"🌡 {col}: успешно преобразовано {after} из {before} значений")

    # --- 3️⃣ Очистка пути воздействия токсинов ---
    if "route_of_exposure" in df.columns:
        df["route_of_exposure"] = df["route_of_exposure"].apply(clean_route)
        print("🧪 Колонка 'route_of_exposure' успешно очищена (перезаписана)")

    # --- 4️⃣ Очистка онкогенности ---
    if "carcinogenicity" in df.columns:
        df["carcinogenicity"] = df["carcinogenicity"].apply(normalize_carcinogenicity)
        print("☣️ Колонка 'carcinogenicity' нормализована до трёх категорий")

    # --- 5️⃣ Преобразуем числовые колонки ---
    numeric_cols = [
        "id", "pubchem_id", "weight", "lethaldose", "min_risk_level",
        "actor_id", "export", "moldb_average_mass", "moldb_mono_mass", "logp"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # --- 6️⃣ Преобразуем даты ---
    datetime_cols = ["created_at", "updated_at"]
    for col in datetime_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # --- 7️⃣ Остальные — строки ---
    string_cols = [
        c for c in df.columns
        if c not in numeric_cols + datetime_cols + ["melting_point", "boiling_point"]
    ]
    df[string_cols] = df[string_cols].astype("string")

    print("📊 Типы данных успешно преобразованы и очищены")

    # --- 8️⃣ Сохраняем результат ---
    if parquet_filename is None:
        parquet_filename = Path("converted_data_fixed.parquet")
    else:
        parquet_filename = Path(parquet_filename)

    df.to_parquet(parquet_filename, index=False)
    print(f"💾 Файл сохранён как: {parquet_filename.resolve()}")

    return df


# --- Пример использования ---
if __name__ == "__main__":
    df = csv_from_drive_to_parquet("1i_H46ci0vi-B17v8UKIGfpQeGRpaa2uI")

# Посмотреть первые 10 значений после очистки
df["route_of_exposure"].head(10)
