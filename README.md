# rdf-validator-ws
Validate your RDF using a web-service API


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