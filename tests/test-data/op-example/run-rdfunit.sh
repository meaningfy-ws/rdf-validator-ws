#!/bin/bash

DATA_FOLDER=`pwd`
CONTAINER_DATA_FOLDER=/mnt/data
#DATA_FILE=$CONTAINER_DATA_FOLDER/treaties-2019-01-28-nal-src-ap.rdf
DATA_FILE=$CONTAINER_DATA_FOLDER/2019-01-28-nal-src-ap/treaties-source-ap.rdf
#DATA_FILE=$CONTAINER_DATA_FOLDER/report-itb-treaties-skos-ap.ttl
SHAPE_FILE=$CONTAINER_DATA_FOLDER/shacl/skos-ap/skosShapes.shapes.ttl
# $CONTAINER_DATA_FOLDER/EuVocOntology/ontologies-lib-release/skos-owl1-dl.rdf,
ENDPOINT=http://localhost:3030/cb

# run file validation
docker run -v $DATA_FOLDER:${CONTAINER_DATA_FOLDER}  --rm -it aksw/rdfunit -d $DATA_FILE -u $DATA_FILE -s $SHAPE_FILE -r shacl -o html,ttl -f $CONTAINER_DATA_FOLDER/


# run endpoint validation (0 query delay)
#docker run -v $DATA_FOLDER:${CONTAINER_DATA_FOLDER} --net="host" --rm -it aksw/rdfunit -d $ENDPOINT -e $ENDPOINT -C -T 0 -D 1 -s $SHAPE_FILE -r shacl -o html,ttl -f $CONTAINER_DATA_FOLDER/

# enter into the container with a bash entripoint
#docker run -v $DATA_FOLDER:$CONTAINER_DATA_FOLDER  --rm -it  --entrypoint bash aksw/rdfunit

