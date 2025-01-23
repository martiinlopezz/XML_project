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
    # Obtener parámetros
    zoo_name = request.args.get('zooName')
    animal_type = request.args.get('animalType')

    # Validación de parámetros
    if not zoo_name or not animal_type:
        return Response("<response><error>Missing parameters: zooName and animalType are required</error></response>", content_type="application/xml", status=400)

    # Cargar el archivo XML
    xml_tree = load_xml()
    if xml_tree is None:
        return Response("<response><error>Error loading XML file</error></response>", content_type="application/xml", status=500)

    # Buscar animales que coincidan con los parámetros
    xpath_query = f"//animal[@species='{animal_type}' and @zooid=//zoo[name='{zoo_name}']/@id]"
    animals = xml_tree.xpath(xpath_query)

    # Si no se encuentran resultados
    if not animals:
        return Response("<response><error>No animals found for the given criteria</error></response>", content_type="application/xml")

    # Generar respuesta XML
    response = "<response><animals>"
    for animal in animals:
        name = animal.findtext("name")
        species = animal.get("species")
        response += f"<animal><name>{name}</name><species>{species}</species></animal>"
    response += "</animals></response>"

    # Devolver respuesta XML
    return Response(response, content_type="application/xml")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
