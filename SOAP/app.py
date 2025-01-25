from flask import Flask, request, Response
import xml.etree.ElementTree as ET
from xml.dom import minidom

app = Flask(__name__)

# Load the XML database
DATABASE_FILE = 'data/zoo.xml'


def load_database():
    tree = ET.parse(DATABASE_FILE)
    return tree


def indent(elem, level=0):
    """Helper function to format XML with indentation."""
    i = "\n" + "  " * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for child in elem:
            indent(child, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
    return elem


def save_database(tree):
    """Guardar la base de datos con una indentación correcta y sin saltos de línea extra."""
    root = tree.getroot()
    raw_xml = ET.tostring(root, encoding='unicode')  # Convierte el XML a string
    parsed_xml = minidom.parseString(raw_xml)  # Parsea el XML para formatearlo
    pretty_xml = parsed_xml.toprettyxml(indent="    ")  # Aplica indentación de 4 espacios

    # Elimina líneas vacías causadas por toprettyxml
    fixed_xml = "\n".join([line for line in pretty_xml.splitlines() if line.strip()])

    # Escribe el XML formateado en el archivo
    with open(DATABASE_FILE, 'w', encoding='utf-8') as file:
        file.write(fixed_xml)

@app.route('/wsdl', methods=['GET'])
def get_wsdl():
    with open('wsdl/service.wsdl', 'r') as wsdl_file:
        wsdl_content = wsdl_file.read()
    return Response(wsdl_content, mimetype='text/xml')


@app.route('/soap', methods=['POST'])
def soap_api():
    try:
        # Parse the incoming SOAP request
        xml_tree = ET.fromstring(request.data)
        body = xml_tree.find("{http://schemas.xmlsoap.org/soap/envelope/}Body")
        operation = body[0].tag.split("}")[1]  # Get the operation name (e.g., "AddZooRequest")
    except Exception as e:
        return Response(f"Error parsing SOAP request: {str(e)}", status=400)

    # Load the XML database
    tree = load_database()
    root = tree.getroot()
    response = ""

    # Route the operation for animals
    if operation == "AddAnimalRequest":
        response = add_animal(root, body[0])
    elif operation == "DeleteAnimalRequest":
        response = delete_animal(root, body[0])
    elif operation == "UpdateAnimalRequest":
        response = update_animal(root, body[0])
    elif operation == "GetAnimalByIdRequest":
        response = get_animal_by_id(root, body[0])
    elif operation == "ListAllAnimalsRequest":
        response = list_all_animals(root)

    # Route the operation for zoos (existing functionality)
    elif operation == "AddZooRequest":
        response = add_zoo(root, body[0])
    elif operation == "DeleteZooRequest":
        response = delete_zoo(root, body[0])
    elif operation == "UpdateZooRequest":
        response = update_zoo(root, body[0])
    elif operation == "GetZooByIdRequest":
        response = get_zoo_by_id(root, body[0])
    elif operation == "ListAllZoosRequest":
        response = list_all_zoos(root)
    else:
        return Response("<response>Unsupported operation</response>", status=400)

    # Save the database if changes were made
    save_database(tree)

    # Return the SOAP response
    return Response(response, mimetype="text/xml")


# Helper functions for operations
def add_zoo(root, data):
    # Check for duplicates
    zoo_id = data.find("id").text
    if root.find(f".//zoo[@id='{zoo_id}']") is not None:
        return f"<response>Zoo with ID {zoo_id} already exists</response>"

    # Extract zoo data from the XML request
    new_zoo = ET.Element('zoo', id=zoo_id, location=data.find("location").text)
    ET.SubElement(new_zoo, 'name').text = data.find("name").text
    ET.SubElement(new_zoo, 'city').text = data.find("city").text
    ET.SubElement(new_zoo, 'foundation').text = data.find("foundation").text

    # Find where to insert the new zoo (before the first <animal>)
    first_animal = root.find(".//animal")
    if first_animal is not None:
        root.insert(list(root).index(first_animal), new_zoo)
    else:
        root.append(new_zoo)  # If no animals, append at the end

    return f"<response>Zoo with ID {zoo_id} added successfully</response>"



def delete_zoo(root, data):
    zoo_id = data.find("id").text
    zoo_to_remove = root.find(f".//zoo[@id='{zoo_id}']")

    if zoo_to_remove is not None:
        root.remove(zoo_to_remove)
        return f"<response>Zoo with ID {zoo_id} removed successfully</response>"
    else:
        return f"<response>Zoo with ID {zoo_id} not found</response>"


def update_zoo(root, data):
    zoo_id = data.find("id").text
    zoo_to_update = root.find(f".//zoo[@id='{zoo_id}']")

    if zoo_to_update is not None:
        zoo_to_update.set('location', data.find("location").text)
        zoo_to_update.find('name').text = data.find("name").text
        zoo_to_update.find('city').text = data.find("city").text
        zoo_to_update.find('foundation').text = data.find("foundation").text

        return f"<response>Zoo with ID {zoo_id} updated successfully</response>"
    else:
        return f"<response>Zoo with ID {zoo_id} not found</response>"


def get_zoo_by_id(root, data):
    zoo_id = data.find("id").text
    zoo = root.find(f".//zoo[@id='{zoo_id}']")

    if zoo is not None:
        return ET.tostring(zoo, encoding='unicode')
    else:
        return f"<response>Zoo with ID {zoo_id} not found</response>"


def list_all_zoos(root):
    zoos = root.findall(".//zoo")
    response = "<zoos>" + "".join([ET.tostring(zoo, encoding='unicode') for zoo in zoos]) + "</zoos>"
    return response

def add_animal(root, data):
    # Check for duplicates
    animal_id = data.find("id").text
    if root.find(f".//animal[@id='{animal_id}']") is not None:
        return f"<response>Animal with ID {animal_id} already exists</response>"

    # Extract animal data from the XML request
    new_animal = ET.Element('animal', id=animal_id, species=data.find("species").text, zooid=data.find("zooid").text)
    ET.SubElement(new_animal, 'name').text = data.find("name").text
    ET.SubElement(new_animal, 'scientific_name').text = data.find("scientific_name").text
    ET.SubElement(new_animal, 'habitat').text = data.find("habitat").text
    ET.SubElement(new_animal, 'diet').text = data.find("diet").text

    # Find the position to insert the new animal (after the last <animal>)
    last_animal = root.findall(".//animal")[-1] if root.findall(".//animal") else None
    if last_animal is not None:
        parent = last_animal.getparent() if hasattr(last_animal, 'getparent') else root
        parent.insert(list(root).index(last_animal) + 1, new_animal)
    else:
        root.append(new_animal)  # If no animals exist, append at the end

    return f"<response>Animal with ID {animal_id} added successfully</response>"

def delete_animal(root, data):
    animal_id = data.find("id").text
    animal_to_remove = root.find(f".//animal[@id='{animal_id}']")

    if animal_to_remove is not None:
        root.remove(animal_to_remove)
        return f"<response>Animal with ID {animal_id} removed successfully</response>"
    else:
        return f"<response>Animal with ID {animal_id} not found</response>"

def update_animal(root, data):
    animal_id = data.find("id").text
    animal_to_update = root.find(f".//animal[@id='{animal_id}']")

    if animal_to_update is not None:
        animal_to_update.set('species', data.find("species").text)
        animal_to_update.set('zooid', data.find("zooid").text)
        animal_to_update.find('name').text = data.find("name").text
        animal_to_update.find('scientific_name').text = data.find("scientific_name").text
        animal_to_update.find('habitat').text = data.find("habitat").text
        animal_to_update.find('diet').text = data.find("diet").text

        return f"<response>Animal with ID {animal_id} updated successfully</response>"
    else:
        return f"<response>Animal with ID {animal_id} not found</response>"

def get_animal_by_id(root, data):
    animal_id = data.find("id").text
    animal = root.find(f".//animal[@id='{animal_id}']")

    if animal is not None:
        return ET.tostring(animal, encoding='unicode')
    else:
        return f"<response>Animal with ID {animal_id} not found</response>"

def list_all_animals(root):
    animals = root.findall(".//animal")
    response = "<animals>" + "".join([ET.tostring(animal, encoding='unicode') for animal in animals]) + "</animals>"
    return response



if __name__ == '__main__':
    app.run(debug=True)
