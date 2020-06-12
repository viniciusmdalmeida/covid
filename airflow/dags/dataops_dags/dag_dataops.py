import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta
from airflow.utils.dates import days_ago

src_path = '/home/vinicius/Documents/Projetos/Claro/Piloto/git_Homologação/src'

args = {
    'owner': 'Dell_EMC',
    'start_date': airflow.utils.dates.days_ago(2),
    'start_date': days_ago(2),
    'email': ['example@dell.com'],
    'email_on_failure': False,
    'email_on_retry': False
}
dag = DAG(
    dag_id='dataops',
    default_args=args,
    schedule_interval=None,
    dagrun_timeout=timedelta(minutes=60)
)

prep_data = BashOperator(
    task_id='prep_data',
    bash_command=f'python {src_path}/prep_data/prep_data.py',
    dag=dag)


unit_test = BashOperator(
    task_id='unit_test',
    bash_command=f'python {src_path}/unit_test/unit_test.py',
    retries=3,
    dag=dag)

modeling = BashOperator(
    task_id='modeling',
    bash_command=f'python {src_path}/modeling/run.py',
    retries=3,
    dag=dag)

prep_data >> unit_test >> modeling