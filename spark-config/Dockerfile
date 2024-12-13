# Use Bitnami Spark image as base
FROM bitnami/spark:latest

# Install curl
USER root
RUN apt-get update && apt-get install -y curl

# Download the necessary dependencies (hadoop-aws and aws-sdk)
RUN curl -sL -o /opt/bitnami/spark/jars/hadoop-aws-3.2.0.jar \
    https://repo.maven.apache.org/maven2/org/apache/hadoop/hadoop-aws/3.2.0/hadoop-aws-3.2.0.jar && \
    curl -sL -o /opt/bitnami/spark/jars/aws-java-sdk-bundle-1.11.603.jar \
    https://repo.maven.apache.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.603/aws-java-sdk-bundle-1.11.603.jar

# Revert to the default spark user
USER 1001
