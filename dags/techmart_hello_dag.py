from datetime import datetime

from airflow.sdk import dag, task


@dag(
    dag_id="techmart_hello_dag",
    start_date=datetime(2026, 10, 1),
    schedule=None,
    catchup=False,
    tags=["techmart", "setup"],
)
def techmart_hello_dag():

    @task
    def check_project():
        print("TechMart Data Platform is connected to Airflow!")
        return "Setup successful"

    check_project()


techmart_hello_dag()

