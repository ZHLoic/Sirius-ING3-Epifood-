from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="food_pipeline",
    start_date=datetime(2026, 8, 16),
    schedule=None,
    catchup=False,
    tags=["food", "mongodb", "pipeline"],
) as dag:

    bronze_to_silver = BashOperator(
        task_id="bronze_to_silver",
        bash_command=(
            "/home/epifood/airflow_venv/bin/python "
            "/home/epifood/data_pipeline/scripts/bronze_to_silver.py"
        ),
    )

    silver_to_gold = BashOperator(
        task_id="silver_to_gold",
        bash_command=(
            "/home/epifood/airflow_venv/bin/python "
            "/home/epifood/data_pipeline/scripts/silver_to_gold.py"
        ),
    )

    bronze_to_silver >> silver_to_gold