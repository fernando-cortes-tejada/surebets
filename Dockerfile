FROM apache/airflow:latest-python3.12

USER root
ARG AIRFLOW_USER_HOME=/opt/airflow
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}
WORKDIR ${AIRFLOW_HOME}
ENV PYTHONPATH “${AIRFLOW_USER_HOME}/dags”:“$PYTHONPATH”
COPY . ./

USER airflow
RUN pip install pip --upgrade && pip install -r requirements.txt
RUN pip install protobuf==3.20.*

RUN playwright install