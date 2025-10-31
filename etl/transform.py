import pandas as pd
import re

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
    cleaned = re.sub(r"\(.*?\)", "", value)
    cleaned = re.sub(r"[\.;]", ",", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
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

def transform(df: pd.DataFrame) -> pd.DataFrame:
    for col in ["melting_point", "boiling_point"]:
        if col in df.columns:
            df[col] = df[col].apply(extract_number)

    if "route_of_exposure" in df.columns:
        df["route_of_exposure"] = df["route_of_exposure"].apply(clean_route)

    if "carcinogenicity" in df.columns:
        df["carcinogenicity"] = df["carcinogenicity"].apply(normalize_carcinogenicity)

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

    print("Данные успешно преобразованы")
    return df
