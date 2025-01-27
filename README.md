# XML_project
Final Project for 2024/25 XML (EN) subject on Timișoara  , Owner : Martín López Villaverde , Contributors : Pablo Torrado García , Marta Vidal López


Utility commands :

python transformations.py ( this is for xslt transformations , this creates a file in resources called output.html with the result of filtered information , this is for STEP 2 ) 

python validate_xml.py ( this is for xsd implementation , the file validate the xml against the xsd file ) 

python REST/app.py (to access the interface that displays the API operations )

To access Orbeon's Xforms, you must copy the xforms-zoos folder into the Orbeon directory and access the url http://localhost:8080/orbeon/xforms-zoos/ after starting the Tomcat server

For Xquery you must run your existdb application and depending on the url you have configured your XML you must change the code. In my case : EXISTDB_URL = "http://localhost:8080/exist/rest/db/zoo"  . Firstly you must load the xml file in the esxitdb interface

To use the API with orbeon you must launch the api doing python api.py and launch orbeon ( previously you must copy the folder to your orbeon launchspace ) 


Steps to run maven apache camel : 

You have to install maven then follow the steps :

mvn clean install
mvn exec:java -Dexec.mainClass=com.zoo.integration.ZooCamelApp

You can check in :

http://localhost:8081/zoo/animals        or       curl -X GET http://localhost:8081/zoo/animals


. Obtener todos los animales

curl -X GET "http://localhost:8081/zoo/animals"

b. Filtrar animales por tipo

curl -X GET "http://localhost:8081/zoo/animals/filter?type=Mammal"

c. Filtrar por hábitat

curl -X GET "http://localhost:8081/zoo/animals/filter?habitat=Savanna"

d. Filtrar por zoo

curl -X GET "http://localhost:8081/zoo/animals/filter?zooName=Berlin%20Zoo"

e. Combinar filtros

curl -X GET "http://localhost:8081/zoo/animals/filter?type=Mammal&habitat=Savanna&zooName=Berlin%20Zoo"


curl "http://localhost:8081/zoo/animals/filter?type=Bird&zooName=Singapore%20Zoo"





You can also test in web :

http://localhost:8081/zoo/animals

http://localhost:8081/zoo/animals/filter?type=Mammal&habitat=Savanna

http://localhost:8081/zoo/animals/filter?type=Bird&zooName=Singapore%20Zoo
