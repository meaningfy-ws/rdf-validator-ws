# 2019-11
## Reducing the number of imports

* the old imports are in the ./deprecated folder; the corresponding library sources are moved into the ./deprecated-imports
* the new imports are in the ./ folder

## Remove the restrictions from the class definitions

* Moving the restrictions into the ./deprecated/extensionDescriptions.ttl
** euvoc:XlNotation
** euvoc:XlNote

## Move the deprecated classes into the orgDescription module

* euvoc:XlNumericalValue
* euvoc:XlSemanticRelation (possibly needed in orgDescription, added back)
* euvoc:XlType  (possibly needed in the orgDescription, added back)

## Remove the deprecated/obsolete properties

* euvoc:isTextual (used in file format)
* euvoc:licenceVersion
* euvoc:license
* euvoc:downloadURL
* euvoc:contributor

## Move the potentially unused properties into orgDescriotion module

* euvoc:xlNumericalValue
* euvoc:xlObject
* euvoc:xlTarget
* euvoc:xlCodification
* euvoc:xlTypeValue

## euvoc:domain
* remove the range ( rdfs:range euvoc:DomainEurovoc ;)

# 2016-07
## Modified standard models:

* Removed illegal "--" character sequence from comments of ontologies in XML format (org ontology only)
* removed circular importd between geosparql gml-32 and sf-geometries
* owl-time, eli and foaf replaced import  http://purl.org/dc/elements/1.1/ with http://purl.org/NET/dc_owl2dl/elements 

Issue: Eli ontology is not consistent according to Cellar pellet. 

Individual http://data.europa.eu/eli/ontology#LegalValue-authoritative is forced to belong to class http://www.w3.org/2008/05/skos-xl#Label and its complement
Inconsistent statements :
equivalentClasses(http://www.w3.org/2004/02/skos/core#Concept,
and([
	max(http://publications.europa.eu/ontology/euvoc#startDate,1,
	http://www.w3.org/2000/01/rdf-schema#Literal),
	some(http://publications.europa.eu/ontology/euvoc#xlNotation,
	http://publications.europa.eu/ontology/euvoc#XlNotation),
	max(http://publications.europa.eu/ontology/euvoc#endDate,1,http://www.w3.org/2000/01/rdf-schema#Literal),
	some(http://purl.org/dc/terms/subject,http://publications.europa.eu/ontology/euvoc#EuroVoc),
	max(http://purl.org/dc/terms/dateAccepted,1,http://www.w3.org/2000/01/rdf-schema#Literal),
	max(http://purl.org/dc/terms/dateSubmitted,1,http://www.w3.org/2000/01/rdf-schema#Literal),
	some(http://publications.europa.eu/ontology/euvoc#status,http://publications.europa.eu/ontology/euvoc#ConceptStatus),
	some(http://lemon-model.net/lemon#context,http://lemon-model.net/lemon#LexicalContext),
	some(http://purl.org/dc/terms/hasPart,http://www.w3.org/2004/02/skos/core#Concept),_TOP_]))
equivalentClasses(http://www.w3.org/2008/05/skos-xl#Label,
and([max(http://publications.europa.eu/ontology/euvoc#startDate,1,http://www.w3.org/2000/01/rdf-schema#Literal),
max(http://publications.europa.eu/ontology/euvoc#endDate,1,http://www.w3.org/2000/01/rdf-schema#Literal),_TOP_]))
disjointWith(http://www.w3.org/2008/05/skos-xl#Label,http://www.w3.org/2004/02/skos/core#Concept)
type(http://data.europa.eu/eli/ontology#LegalValue-authoritative,http://www.w3.org/2004/02/skos/core#Concept)

## Modifications: 

* Removed the module extensionDescriptions.ttl


