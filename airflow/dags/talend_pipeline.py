from airflow import DAG
from airflow.providers.ssh.operators.ssh import SSHOperator
from datetime import datetime, timedelta

# -----------------------------
# 1️⃣ Sous-classe SSHOperator
# -----------------------------
class SSHOperatorNoTemplate(SSHOperator):
    # désactive complètement le templating pour le champ `command`
    template_fields = []

# -----------------------------
# 2️⃣ Arguments par défaut du DAG
# -----------------------------
default_args = {
    "owner": "data-team",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

# -----------------------------
# 3️⃣ Définition du DAG
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
    # 4️⃣ Tâches SSHOperatorNoTemplate
    # -----------------------------
    web_to_bronze = SSHOperatorNoTemplate(
        task_id="web_to_bronze",
        ssh_conn_id="ssh_vm_bronze",
        command="/home/epifood/BronzeJob_0.1/BronzeJob/BronzeJob_run.sh",
        do_xcom_push=False
    )

    bronze_to_silver = SSHOperatorNoTemplate(
        task_id="bronze_to_silver",
        ssh_conn_id="ssh_vm_silver",
        command="/home/epifood/Silverjob/SilverJob/SilverJob_run.sh",
        do_xcom_push=False
    )

    silver_to_gold = SSHOperatorNoTemplate(
        task_id="silver_to_gold",
        ssh_conn_id="ssh_vm_gold",
        command="/home/epifood/Gold/Gold_run.sh",
        do_xcom_push=False
    )

    # -----------------------------
    # 5️⃣ Ordre d'exécution
    # -----------------------------
    web_to_bronze >> bronze_to_silver >> silver_to_gold

