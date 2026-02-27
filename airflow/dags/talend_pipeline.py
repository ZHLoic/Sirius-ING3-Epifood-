from airflow import DAG
from airflow.providers.ssh.operators.ssh import SSHOperator
from datetime import datetime, timedelta

# -----------------------------
# 1 Sous-classe SSHOperator
# -----------------------------
class SSHOperatorNoTemplate(SSHOperator):
    template_fields = []

# -----------------------------
# 2 Arguments par défaut du DAG
# -----------------------------
default_args = {
    "owner": "data-team",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

# -----------------------------
# 3 Définition du DAG
# -----------------------------
with DAG(
    dag_id="talend_multi_vm_pipeline",
    start_date=datetime(2026, 1, 15),
    schedule="0 1 * * *",
    catchup=False,
    default_args=default_args,
    tags=["talend", "multi-vm"],
) as dag:

    # -----------------------------
    # 4 Tâches SSHOperatorNoTemplate
    # -----------------------------

    # VM Bronze : 172.31.253.66
    web_to_bronze = SSHOperatorNoTemplate(
        task_id="web_to_bronze",
        ssh_conn_id="ssh_vm_bronze",  # Host : 172.31.253.66
        command="/home/ZHLoic/job/BronzeJob/BronzeJob_run.sh",
        do_xcom_push=False,
    )

    # VM Silver/Gold : 172.31.252.182
    bronze_to_silver = SSHOperatorNoTemplate(
        task_id="bronze_to_silver",
        ssh_conn_id="ssh_vm_silver_gold",  # Host : 172.31.252.182
        command="/home/ZHLoic/silverjob/SilverJob/SilverJob_run.sh",
        do_xcom_push=False,
    )

    silver_to_gold = SSHOperatorNoTemplate(
        task_id="silver_to_gold",
        ssh_conn_id="ssh_vm_silver_gold",  # Host : 172.31.252.182
        command="/home/ZHLoic/goldjob/Gold_Cuisine/Gold_Cuisine_run.sh",
        do_xcom_push=False,
    )

    # -----------------------------
    # 5 Ordre d'exécution
    # -----------------------------
    web_to_bronze >> bronze_to_silver >> silver_to_gold