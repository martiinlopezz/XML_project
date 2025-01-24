from flask import Flask, request, Response
from lxml import etree

app = Flask(__name__)

# Ruta del archivo XML
XML_FILE = "resources/zoo.xml"

def load_xml():
    """Carga y parsea el archivo XML."""
    try:
        with open(XML_FILE, "r", encoding="utf-8") as file:
            return etree.parse(file)
    except Exception as e:
        print(f"Error al cargar el archivo XML: {e}")
        return None


@app.route('/api/zoo', methods=['GET'])
def get_animals():
    # Obtener parámetros de la solicitud
    zoo_name = request.args.get('zooName', '').strip()
    animal_type = request.args.get('animalType', '').strip()
    habitat = request.args.get('habitat', '').strip()

    # Cargar el archivo XML
    xml_tree = load_xml()
    if xml_tree is None:
        return Response("<response><error>Error loading XML file</error></response>", content_type="application/xml", status=500)

    # Si no se pasan parámetros, devolver todos los animales
    if not zoo_name and not animal_type and not habitat:
        animals = xml_tree.xpath("//animal")
    else:
        # Construir la consulta XPath dinámicamente
        xpath_conditions = []
        if zoo_name:
            xpath_conditions.append(f"@zooid=//zoo[name='{zoo_name}']/@id")
        if animal_type:
            xpath_conditions.append(f"@species='{animal_type}'")
        if habitat:
            xpath_conditions.append(f"habitat='{habitat}'")

        # Crear la consulta XPath final
        xpath_query = f"//animal[{ ' and '.join(xpath_conditions) }]"
        animals = xml_tree.xpath(xpath_query)

    # Si no se encuentran resultados
    if not animals:
        return Response("<response><animals/></response>", content_type="application/xml", status=200)

    # Generar respuesta XML
    response = "<response><animals>"
    for animal in animals:
        name = animal.findtext("name")
        species = animal.get("species")
        animal_habitat = animal.findtext("habitat")
        response += f"<animal><name>{name}</name><species>{species}</species><habitat>{animal_habitat}</habitat></animal>"
    response += "</animals></response>"

    # Devolver respuesta XML
    return Response(response, content_type="application/xml")


if __name__ == '__main__':
    app.run(debug=True, port=5000)
