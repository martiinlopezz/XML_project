# XML_project
Final Project for 2024/25 XML (EN) subject on Timișoara  , Owner : Martín López Villaverde , Contributors : Pablo Torrado García , Marta Vidal López


Utility commands :

python transformations.py ( this is for xslt transformations , this creates a file in resources called output.html with the result of filtered information , this is for STEP 2 ) 

python validate_xml.py ( this is for xsd implementation , the file validate the xml against the xsd file ) 

python REST/app.py (to access the interface that displays the API operations )

To access Orbeon's Xforms, you must copy the xforms-zoos folder into the Orbeon directory and access the url http://localhost:8080/orbeon/xforms-zoos/ after starting the Tomcat server

For Xquery you must run your existdb application and depending on the url you have configured your XML you must change the code. In my case : EXISTDB_URL = "http://localhost:8080/exist/rest/db/zoo"  . Firstly you must load the xml file in the esxitdb interface