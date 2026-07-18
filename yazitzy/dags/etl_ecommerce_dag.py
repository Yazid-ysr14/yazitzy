"""
Airflow DAG: ETL E-Commerce Orders
Sesuai struktur GitHub yang direncanakan di halaman 9
"yazitzy.pdf".

Diletakkan di folder dags/ Apache Airflow -- otomatis terdeteksi dan
terjadwal. Task logic (extract/transform/validate/load) diimpor dari
etl_pipeline.py supaya DAG ini tetap tipis dan konsisten dengan versi
script/notebook yang lain.
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

from etl_pipeline import extract, transform, validate, load

default_args = {
    "owner": "yazitzy",
    "depends_on_past": False,
    "email": ["alert@company.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}


def _extract(**kwargs):
    orders, products = extract()
    kwargs["ti"].xcom_push(key="row_count", value=len(orders))
    orders.to_csv("_tmp_extracted.csv", index=False)
    return "_tmp_extracted.csv"


def _transform(**kwargs):
    import pandas as pd
    orders = pd.read_csv("_tmp_extracted.csv")
    orders = transform(orders)
    orders.to_csv("_tmp_transformed.csv", index=False)
    return "_tmp_transformed.csv"


def _validate(**kwargs):
    import pandas as pd
    orders = pd.read_csv("_tmp_transformed.csv", parse_dates=["tanggal_order"])
    validate(orders)  # raises -> task fails -> Airflow retries/alerts
    return "_tmp_transformed.csv"


def _load(**kwargs):
    import pandas as pd
    orders = pd.read_csv("_tmp_transformed.csv", parse_dates=["tanggal_order"])
    load(orders)


with DAG(
    dag_id="etl_ecommerce_daily",
    default_args=default_args,
    description="Daily ETL pipeline untuk data transaksi e-commerce",
    schedule="0 6 * * *",  # setiap hari jam 06:00
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["etl", "ecommerce", "daily"],
) as dag:

    start = EmptyOperator(task_id="start")
    extract_task = PythonOperator(task_id="extract_orders", python_callable=_extract)
    transform_task = PythonOperator(task_id="transform_and_clean", python_callable=_transform)
    validate_task = PythonOperator(task_id="validate_quality", python_callable=_validate)
    load_task = PythonOperator(task_id="load_to_warehouse", python_callable=_load)
    end = EmptyOperator(task_id="end")

    start >> extract_task >> transform_task >> validate_task >> load_task >> end
