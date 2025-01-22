import xml.etree.ElementTree as ET

# Ruta al archivo XML
XML_FILE_PATH = "data/zoo.xml"


def handle_xml_exceptions(error_message):
    """
    Decorador para manejar excepciones específicas en las funciones con XML.
    :param error_message: Mensaje de error específico para la función.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except FileNotFoundError:
                raise FileNotFoundError(f"{error_message}: El archivo XML '{XML_FILE_PATH}' no se encontró.")
            except ET.ParseError as e:
                raise ValueError(f"{error_message}: Error al analizar el archivo XML: {str(e)}")
            except Exception as e:
                raise Exception(f"{error_message}: {str(e)}")

        return wrapper

    return decorator


@handle_xml_exceptions("Error al obtener información del zoológico")
def get_zoo_info(zoo_id):
    """
    Busca información de un zoológico por su ID en el archivo XML.
    """
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    zoo = root.find(f".//zoo[@id='{zoo_id}']")
    if zoo is not None:
        return {
            "name": zoo.find('name').text,
            "city": zoo.find('city').text,
            "foundation": zoo.find('foundation').text,
            "location": zoo.get('location'),
        }
    return None


@handle_xml_exceptions("Error al agregar un zoológico")
def add_zoo(zoo_id, name, city, foundation, location):
    """
    Agrega un nuevo zoológico al archivo XML.
    """
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    new_zoo = ET.Element("zoo", attrib={"id": zoo_id, "location": location})
    ET.SubElement(new_zoo, "name").text = name
    ET.SubElement(new_zoo, "city").text = city
    ET.SubElement(new_zoo, "foundation").text = foundation
    root.append(new_zoo)
    tree.write(XML_FILE_PATH, encoding="utf-8", xml_declaration=True)
    return True


@handle_xml_exceptions("Error al eliminar el zoológico")
def delete_zoo(zoo_id):
    """
    Elimina un zoológico por su ID del archivo XML.
    """
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    zoo = root.find(f".//zoo[@id='{zoo_id}']")
    if zoo is not None:
        # Eliminar animales asociados al zoológico
        animals = root.findall(f".//animal[@zooid='{zoo_id}']")
        for animal in animals:
            root.remove(animal)

        # Eliminar el zoológico
        root.remove(zoo)
        tree.write(XML_FILE_PATH, encoding="utf-8", xml_declaration=True)
        return True
    return False


@handle_xml_exceptions("Error al actualizar la información del zoológico")
def update_zoo_info(zoo_id, name=None, city=None, foundation=None, location=None):
    """
    Actualiza información de un zoológico por su ID.
    """
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    zoo = root.find(f".//zoo[@id='{zoo_id}']")
    if zoo is not None:
        if name: zoo.find('name').text = name
        if city: zoo.find('city').text = city
        if foundation: zoo.find('foundation').text = foundation
        if location: zoo.set('location', location)
        tree.write(XML_FILE_PATH, encoding="utf-8", xml_declaration=True)
        return True
    else:
        return False


@handle_xml_exceptions("Error al listar los zoológicos")
def list_zoos():
    """
    Lista todos los zoológicos en el archivo XML.
    """
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    zoos = []
    for zoo in root.findall('.//zoo'):
        zoos.append({
            "id": zoo.get('id'),
            "name": zoo.find('name').text,
            "city": zoo.find('city').text,
            "foundation": zoo.find('foundation').text,
            "location": zoo.get('location')
        })
    return zoos


@handle_xml_exceptions("Error al contar animales en un zoológico")
def count_animals_in_zoo(zoo_id):
    """
    Cuenta cuántos animales están asociados a un zoológico específico.
    """
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    animals = root.findall(f".//animal[@zooid='{zoo_id}']")
    return len(animals)


@handle_xml_exceptions("Error al listar zoológicos con animales")
def list_zoos_with_animals():
    """
    Lista todos los zoológicos junto con los animales asociados.
    """
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    zoos = []
    for zoo in root.findall(".//zoo"):
        zoo_id = zoo.get('id')
        animals = root.findall(f".//animal[@zooid='{zoo_id}']")
        animal_list = [
            {"id": animal.get('id'), "name": animal.find('name').text}
            for animal in animals
        ]
        zoos.append({
            "id": zoo_id,
            "name": zoo.find('name').text,
            "animals": animal_list
        })
    return zoos

@handle_xml_exceptions("Error al obtener el zoológico con más animales")
def get_zoo_with_most_animals():
    """
    Encuentra el zoológico con el mayor número de animales.
    :return: Diccionario con el ID, nombre y cantidad de animales del zoológico.
    """
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    max_count = 0
    best_zoo = None

    for zoo in root.findall(".//zoo"):
        zoo_id = zoo.get('id')
        animals = root.findall(f".//animal[@zooid='{zoo_id}']")
        animal_count = len(animals)

        if animal_count > max_count:
            max_count = animal_count
            best_zoo = {
                "zoo_id": zoo_id,
                "name": zoo.find('name').text,
                "animal_count": animal_count
            }

    return best_zoo if best_zoo else {"message": "No hay zoológicos con animales"}

@handle_xml_exceptions("Error al listar zoológicos con animales")
def list_zoos_with_animals():
    """
    Lista todos los zoológicos junto con sus animales.
    :return: Lista de zoológicos con animales asociados.
    """
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    zoos = []
    for zoo in root.findall(".//zoo"):
        zoo_id = zoo.get('id')
        animals = root.findall(f".//animal[@zooid='{zoo_id}']")
        animal_list = [
            {"id": animal.get('id'), "name": animal.find('name').text}
            for animal in animals
        ]
        zoos.append({
            "id": zoo_id,
            "name": zoo.find('name').text,
            "animals": animal_list
        })
    return zoos

@handle_xml_exceptions("Error al obtener información del animal")
def get_animal_info(animal_id):
    """
    Obtiene información de un animal por su ID.
    """
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    animal = root.find(f".//animal[@id='{animal_id}']")
    if animal is not None:
        return {
            "name": animal.find('name').text,
            "species": animal.get('species'),
            "scientific_name": animal.find('scientific_name').text,
            "habitat": animal.find('habitat').text,
            "diet": animal.find('diet').text,
        }
    return None


@handle_xml_exceptions("Error al agregar un animal")
def add_animal(animal_id, zoo_id, name, species, scientific_name, habitat, diet):
    """
    Agrega un nuevo animal al archivo XML.
    """
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    zoo = root.find(f".//zoo[@id='{zoo_id}']")
    if zoo is None:
        raise ValueError(f"No existe un zoológico con el ID: {zoo_id}")

    new_animal = ET.Element("animal", attrib={"id": animal_id, "species": species, "zooid": zoo_id})
    ET.SubElement(new_animal, "name").text = name
    ET.SubElement(new_animal, "scientific_name").text = scientific_name
    ET.SubElement(new_animal, "habitat").text = habitat
    ET.SubElement(new_animal, "diet").text = diet
    root.append(new_animal)
    tree.write(XML_FILE_PATH, encoding="utf-8", xml_declaration=True)
    return True


@handle_xml_exceptions("Error al eliminar un animal")
def delete_animal(animal_id):
    """
    Elimina un animal por su ID del archivo XML.
    """
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    animal = root.find(f".//animal[@id='{animal_id}']")
    if animal is not None:
        root.remove(animal)
        tree.write(XML_FILE_PATH, encoding="utf-8", xml_declaration=True)
        return True
    return False


@handle_xml_exceptions("Error al actualizar la información del animal")
def update_animal_info(animal_id, name=None, species=None, scientific_name=None, habitat=None, diet=None):
    """
    Actualiza información de un animal por su ID.
    """
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    animal = root.find(f".//animal[@id='{animal_id}']")
    if animal is not None:
        if name: animal.find('name').text = name
        if species: animal.set('species', species)
        if scientific_name: animal.find('scientific_name').text = scientific_name
        if habitat: animal.find('habitat').text = habitat
        if diet: animal.find('diet').text = diet
        tree.write(XML_FILE_PATH, encoding="utf-8", xml_declaration=True)
        return True
    else:
        return False


@handle_xml_exceptions("Error al listar los animales")
def list_animals():
    """
    Lista todos los animales en el archivo XML.
    """
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    animals = []
    for animal in root.findall('.//animal'):
        animals.append({
            "id": animal.get('id'),
            "name": animal.find('name').text,
            "species": animal.get('species'),
            "scientific_name": animal.find('scientific_name').text,
            "habitat": animal.find('habitat').text,
            "diet": animal.find('diet')
        })
    return animals


@handle_xml_exceptions("Error al obtener animales por zoológico")
def get_animals_by_zoo(zoo_id):
    """
    Lista los animales que pertenecen a un zoológico específico.
    """
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    animals = []
    for animal in root.findall(f".//animal[@zooid='{zoo_id}']"):
        animals.append({
            "id": animal.get('id'),
            "name": animal.find('name').text,
            "species": animal.get('species'),
            "scientific_name": animal.find('scientific_name').text,
            "habitat": animal.find('habitat').text,
            "diet": animal.find('diet')
        })
    return animals

@handle_xml_exceptions("Error al buscar animales por especie")
def get_animals_by_species(species):
    """
    Busca animales por su especie en el archivo XML.
    :param species: Especie a buscar.
    :return: Lista de animales pertenecientes a la especie.
    """
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    animals = []
    for animal in root.findall(f".//animal[@species='{species}']"):
        animals.append({
            "id": animal.get('id'),
            "name": animal.find('name').text,
            "scientific_name": animal.find('scientific_name').text,
            "habitat": animal.find('habitat').text,
            "diet": animal.find('diet'),
        })
    return animals