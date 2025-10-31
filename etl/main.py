from etl.extract import extract_from_drive
from etl.transform import transform_data
from etl.load import load_to_db


def main():
    file_id = "1i_H46ci0vi-B17v8UKIGfpQeGRpaa2uI"
    raw_path = extract_from_drive(file_id, filename="t3db_raw.csv")
    processed_path = transform_data(raw_path, filename="t3db_clean.parquet")
    load_to_db(processed_path, table_name="t3db_data")

if __name__ == "__main__":
    main()
