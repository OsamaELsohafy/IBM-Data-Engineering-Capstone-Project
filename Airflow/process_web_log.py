from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

# Define default arguments
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

# Define the DAG
dag = DAG(
    'process_web_log',
    default_args=default_args,
    description='A simple DAG to process web logs',
    schedule_interval='@daily',
)

# Define tasks
extract_task = BashOperator(
    task_id='extract_data',
    bash_command='cat /home/project/airflow/dags/accesslog.text | awk \'{print $1}\' > /home/project/airflow/dags/extracted_data.txt',
    dag=dag,
)

transform_task = BashOperator(
    task_id='transform_data',
    bash_command='cat /home/project/airflow/dags/extracted_data.txt | sort | uniq > /home/project/airflow/dags/transformed_data.txt',
    dag=dag,
)

load_task = BashOperator(
    task_id='load_data',
    bash_command='tar -cvf /home/project/airflow/dags/weblog.tar /home/project/airflow/dags/transformed_data.txt',
    dag=dag,
)

# Set task dependencies
extract_task >> transform_task >> load_task
