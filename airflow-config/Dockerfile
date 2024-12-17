FROM openjdk:11-jre-slim AS openjdk

FROM apache/airflow:2.9.3

COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r /requirements.txt

COPY --from=openjdk /usr/local/openjdk-11 /usr/local/openjdk-11

USER root

RUN apt-get update && apt-get install -y wget tar

ENV SPARK_VERSION=3.4.1
RUN wget https://archive.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop3.tgz \
    && tar -xzf spark-$SPARK_VERSION-bin-hadoop3.tgz -C /opt \
    && ln -s /opt/spark-$SPARK_VERSION-bin-hadoop3 /opt/spark \
    && rm spark-$SPARK_VERSION-bin-hadoop3.tgz

RUN apt-get update \
&& apt-get install -y software-properties-common

RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/* && apt-get install -y bash

ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH
ENV JAVA_HOME=/usr/local/openjdk-11
ENV PATH=$JAVA_HOME/bin:$PATH
ENV PATH=$PATH:/opt/spark/bin
ENV PATH="/usr/bin:${PATH}"


USER airflow
