# Build RDFUnit
FROM maven:3-jdk-8 as build

RUN curl https://codeload.github.com/AKSW/RDFUnit/zip/master --output rdfunit-sources.zip
RUN unzip rdfunit-sources.zip
WORKDIR /RDFUnit-master
RUN mvn -pl rdfunit-validate -am clean package -P cli-standalone -DskipTests=true

# Build for python API
FROM python:3.8.5-buster as target

RUN apt-get update -y \
&& apt-get upgrade -y \
&& apt-get install -y openjdk-11-jre

WORKDIR /usr/src/rdfunit
COPY --from=build /RDFUnit-master/rdfunit-validate/target/rdfunit-validate-*-standalone.jar /usr/src/rdfunit/rdfunit-validate.jar

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /usr/src/app
COPY . /usr/src/app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD gunicorn --timeout ${RDF_VALIDATOR_GUNICORN_TIMEOUT} --workers 10  --bind 0.0.0.0:${VALIDATOR_API_PORT} --reload validator.entrypoints.api.run:app