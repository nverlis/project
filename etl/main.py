from extract import extract_from_drive
from transform import transform
from load import load_to_parquet

def main():
    file_id = "1i_H46ci0vi-B17v8UKIGfpQeGRpaa2uI"
    df = extract_from_drive(file_id)
    df = transform(df)
    load_to_parquet(df)
