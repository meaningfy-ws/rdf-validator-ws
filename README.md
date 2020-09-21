# rdf-validator-ws

Validate your RDF using a web-service API

## build and run project

```
docker-compose up --build
```

**Form validation** is available at [http://localhost:9090/shacl/any/upload](http://localhost:9090/shacl/any/upload)

**API validation** is available at [http://localhost:9090/shacl/any/api](http://localhost:9090/shacl/any/api)

## Docs

Read more documentation on configuring the RDF validator [here](https://www.itb.ec.europa.eu/docs/guides/latest/validatingRDF/index.html).


# use cases 
Case 1 parameters: 
- dataset URI 1..1
- graph 0..*
- SPARQL endpoint 1..1
- schemas 1..*


Case 2 parameters: 
- dataset URI 1..1
- data files 1..*
- schemas 1..*


Case 3 parameters: 
- dataset URI 1..1
- source URI 1..*
- schemas 1..*

Output:
- Machine readable: Validation Report RDF
- Human friendly: eds4jinja over the RDF output, resulting in HTML/PDF content