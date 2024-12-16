FROM apache/airflow:2.9.3

COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r /requirements.txt

USER root

# Обновляем индекс и устанавливаем необходимые пакеты
USER root

# Обновляем индекс и устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y wget tar

# Download and install Apache Spark
ENV SPARK_VERSION=3.4.1
RUN wget https://archive.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop3.tgz \
    && tar -xzf spark-$SPARK_VERSION-bin-hadoop3.tgz -C /opt \
    && ln -s /opt/spark-$SPARK_VERSION-bin-hadoop3 /opt/spark \
    && rm spark-$SPARK_VERSION-bin-hadoop3.tgz

# Set Spark environment variables
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

USER airflow