import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2)
}
dag = DAG(
    dag_id='fluxo_simples',
    default_args=args,
    schedule_interval=timedelta(days=1),
    dagrun_timeout=timedelta(minutes=60)
)
# Depois da preparação da DAG
# 1. Imprime a data na saída padrão
task1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)
# 2. Faz uma sleep de 5 segundos.
# Dando errado tente em no máximo 3 vezes
task2 = BashOperator(
    task_id='sleep',
    bash_command='sleep 5',
    retries=3,
    dag=dag)
# 3. Salve a data em um arquivo texto
task3 = BashOperator(
    task_id='save_date',
    bash_command='date > /tmp/date_output.txt',
    retries=3,
    dag=dag)

# Interligando task1 ao task2
task1.set_downstream(task2)
# Interligando task2 ao task3
task2.set_downstream(task3)
