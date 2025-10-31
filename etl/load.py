import os
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def validate_output_data(df: pd.DataFrame) -> bool:
    if df.empty:
        print("Ошибка: выходной DataFrame пустой")
        return False

    print("Валидация выходных данных пройдена")
    return True


def get_engine():
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_url = os.getenv("DB_URL")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME", "homeworks")

    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_url}:{db_port}/{db_name}",
        pool_recycle=3600
    )
    print(f"Подключение к БД '{db_name}' успешно создано")
    return engine


def load_to_db(input_path: str, table_name="vibe", schema="public", limit: int = 100) -> bool:
    df = pd.read_parquet(input_path) if input_path.endswith(".parquet") else pd.read_csv(input_path)
    df = df.head(limit)

    if not validate_output_data(df):
        print("Выгрузка в базу прервана из-за ошибки валидации")
        return False

    try:
        engine = get_engine()
        df.to_sql(
            name=table_name,
            con=engine,
            schema=schema,
            if_exists="replace",
            index=False,
        )
        print(f"DataFrame ({len(df)} строк) успешно выгружен в таблицу '{schema}.{table_name}'")
        return True
    except Exception as e:
        print(f"Ошибка при выгрузке в базу: {e}")
        return False


def load_to_parquet(input_path: str, output_dir="data/final", name="output"):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet(input_path) if input_path.endswith(".parquet") else pd.read_csv(input_path)

    output_path = Path(output_dir) / f"{name}.parquet"
    df.to_parquet(output_path, index=False)

    print(f"Финальный файл сохранён как: {output_path.resolve()}")
    return str(output_path)
