from flask import Flask, Response, url_for

app = Flask(__name__)

# Definición de las operaciones
OPERATIONS = [
    {"name": "get_zoo_info", "input": "getZooInfoRequest", "output": "getZooInfoResponse", "description": "Obtener información sobre un zoológico."},
    {"name": "add_zoo", "input": "addZooRequest", "output": "addZooResponse", "description": "Agregar un nuevo zoológico."},
    {"name": "delete_zoo", "input": "deleteZooRequest", "output": "deleteZooResponse", "description": "Eliminar un zoológico."},
    {"name": "update_zoo_info", "input": "updateZooInfoRequest", "output": "updateZooInfoResponse", "description": "Actualizar información de un zoológico."},
    {"name": "list_zoos", "input": "listZoosRequest", "output": "listZoosResponse", "description": "Listar todos los zoológicos."},
    {"name": "list_zoos_with_animals", "input": "listZoosWithAnimalsRequest", "output": "listZoosWithAnimalsResponse", "description": "Listar zoológicos con animales asociados."},
    {"name": "get_zoo_with_most_animals", "input": "getZooWithMostAnimalsRequest", "output": "getZooWithMostAnimalsResponse", "description": "Obtener el zoológico con más animales."},
    {"name": "get_animal", "input": "getAnimalRequest", "output": "getAnimalResponse", "description": "Obtener información sobre un animal."},
    {"name": "add_animal", "input": "addAnimalRequest", "output": "addAnimalResponse", "description": "Agregar un nuevo animal."},
    {"name": "delete_animal", "input": "deleteAnimalRequest", "output": "deleteAnimalResponse", "description": "Eliminar un animal."},
    {"name": "update_animal_info", "input": "updateAnimalInfoRequest", "output": "updateAnimalInfoResponse", "description": "Actualizar información de un animal."},
    {"name": "list_animals", "input": "listAnimalsRequest", "output": "listAnimalsResponse", "description": "Listar todos los animales."},
    {"name": "get_animals_by_zoo", "input": "getAnimalsByZooRequest", "output": "getAnimalsByZooResponse", "description": "Obtener animales por zoológico."},
    {"name": "count_animals_in_zoo", "input": "countAnimalsInZooRequest", "output": "countAnimalsInZooResponse", "description": "Contar animales en un zoológico."},
    {"name": "get_animals_by_species", "input": "getAnimalsBySpeciesRequest", "output": "getAnimalsBySpeciesResponse", "description": "Obtener animales por especie."}
]

@app.route("/wsdl", methods=["GET"])
def generate_wsdl():
    """
    Genera dinámicamente un archivo WSDL basado en las operaciones definidas.
    """
    service_url = url_for("generate_wsdl", _external=True).replace("/wsdl", "")
    target_namespace = f"{service_url}/zoo_soap"

    # Inicio del WSDL
    wsdl = f"""<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="http://schemas.xmlsoap.org/wsdl/"
             xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
             xmlns:xs="http://www.w3.org/2001/XMLSchema"
             xmlns:tns="{target_namespace}"
             targetNamespace="{target_namespace}"
             name="ZooService">

    <!-- Tipos de datos -->
    <types>
        <xs:schema targetNamespace="{target_namespace}">
    """

    # Generar los elementos para cada operación
    for operation in OPERATIONS:
        wsdl += f"""
            <!-- Operación: {operation['name']} -->
            <xs:element name="{operation['input']}">
                <xs:complexType>
                    <xs:sequence>
                        <xs:element name="parameter" type="xs:string" minOccurs="0"/>
                    </xs:sequence>
                </xs:complexType>
            </xs:element>
            <xs:element name="{operation['output']}">
                <xs:complexType>
                    <xs:sequence>
                        <xs:element name="message" type="xs:string"/>
                    </xs:sequence>
                </xs:complexType>
            </xs:element>
        """

    wsdl += """
        </xs:schema>
    </types>

    <!-- Mensajes -->
    """

    # Generar mensajes
    for operation in OPERATIONS:
        wsdl += f"""
        <message name="{operation['input']}">
            <part name="parameters" element="tns:{operation['input']}"/>
        </message>
        <message name="{operation['output']}">
            <part name="parameters" element="tns:{operation['output']}"/>
        </message>
        """

    # Generar el portType
    wsdl += """
    <!-- Puerto y operación -->
    <portType name="ZooServicePortType">
    """
    for operation in OPERATIONS:
        wsdl += f"""
        <operation name="{operation['name']}">
            <documentation>{operation['description']}</documentation>
            <input message="tns:{operation['input']}"/>
            <output message="tns:{operation['output']}"/>
        </operation>
        """

    wsdl += """
    </portType>

    <!-- Protocolo de enlace -->
    <binding name="ZooServiceBinding" type="tns:ZooServicePortType">
        <soap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
    """
    for operation in OPERATIONS:
        wsdl += f"""
        <operation name="{operation['name']}">
            <soap:operation soapAction="{target_namespace}#{operation['name']}" style="document"/>
            <input>
                <soap:body use="literal"/>
            </input>
            <output>
                <soap:body use="literal"/>
            </output>
        </operation>
        """

    # Servicio final
    wsdl += f"""
    </binding>

    <!-- Servicio -->
    <service name="ZooService">
        <port name="ZooServicePort" binding="tns:ZooServiceBinding">
            <soap:address location="{service_url}"/>
        </port>
    </service>

</definitions>
"""
    return Response(wsdl, content_type="text/xml")
