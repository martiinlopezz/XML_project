import xml.etree.ElementTree as ET
from lxml import etree

# Cargar el archivo XML
def load_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return tree, root

# Guardar el archivo XML
def save_xml(tree, file_path):
    tree.write(file_path, encoding="utf-8", xml_declaration=True)

# Funciones para Zoos
def get_all_zoos(file_path):
    tree, root = load_xml(file_path)
    zoos = []
    for zoo in root.findall("zoo"):
        zoos.append({
            "id": zoo.get("id"),
            "location": zoo.get("location"),
            "name": zoo.find("name").text,
            "city": zoo.find("city").text,
            "foundation": zoo.find("foundation").text,
        })
    return zoos

def get_zoo_by_id(file_path, zoo_id):
    tree, root = load_xml(file_path)
    zoo = root.find(f"zoo[@id='{zoo_id}']")
    if zoo:
        return {
            "id": zoo.get("id"),
            "location": zoo.get("location"),
            "name": zoo.find("name").text,
            "city": zoo.find("city").text,
            "foundation": zoo.find("foundation").text,
        }
    return None

def add_zoo(file_path, data):
    try:
        tree, root = load_xml(file_path)
        zoos = root.findall("zoo")  # Obtener todos los nodos zoo

        # Validación del año de fundación
        try:
            foundation_year = int(data["foundation"])
            if foundation_year < 0 or foundation_year > 2025:
                return {"success": False, "message": "Invalid foundation year. It must be between 0 and 2025."}
        except ValueError:
            return {"success": False, "message": "Foundation year must be a valid number."}

        # Generar un nuevo ID basado en el último nodo
        if zoos:
            last_zoo = zoos[-1]
            new_id = f"zoo{int(last_zoo.get('id').replace('zoo', '')) + 1}"
        else:
            last_zoo = None
            new_id = "zoo1"

        # Crear el nuevo nodo zoo
        new_zoo = ET.Element("zoo", id=new_id, location=data["location"])
        ET.SubElement(new_zoo, "name").text = data["name"]
        ET.SubElement(new_zoo, "city").text = data["city"]
        ET.SubElement(new_zoo, "foundation").text = data["foundation"]

        # Insertar el nuevo nodo en la posición correcta
        if last_zoo is not None:
            root.insert(list(root).index(last_zoo) + 1, new_zoo)
        else:
            root.append(new_zoo)

        # Guardar los cambios en el archivo XML
        save_xml(tree, file_path)
        return {"success": True, "id": new_id, "message": "Zoo added successfully."}

    except Exception as e:
        print(f"Error in add_zoo: {e}")
        return {"success": False, "message": "Failed to add zoo."}


def update_zoo(file_path, zoo_id, data):
    tree, root = load_xml(file_path)
    zoo = root.find(f"zoo[@id='{zoo_id}']")
    if zoo:
        zoo.set("location", data.get("location", zoo.get("location")))
        zoo.find("name").text = data.get("name", zoo.find("name").text)
        zoo.find("city").text = data.get("city", zoo.find("city").text)
        zoo.find("foundation").text = data.get("foundation", zoo.find("foundation").text)
        save_xml(tree, file_path)
        return True
    return False

def delete_zoo(file_path, zoo_id):
    tree, root = load_xml(file_path)

    # Encuentra el zoo
    zoo = root.find(f"zoo[@id='{zoo_id}']")
    if not zoo:
        return False

    # Encuentra y elimina animales asociados al zoo
    animals_to_remove = root.findall(f"animal[@zooid='{zoo_id}']")
    for animal in animals_to_remove:
        # Eliminar estadísticas asociadas al animal
        animal_id = animal.get("id")
        delete_conservation_stat(file_path, animal_id)  # Asegúrate de que esta función se llame correctamente

        # Eliminar el nodo del animal
        root.remove(animal)

    # Eliminar el zoo
    root.remove(zoo)

    # Guardar los cambios en el archivo XML
    save_xml(tree, file_path)
    return True







# Funciones para Animales
def get_all_animals(file_path):
    tree, root = load_xml(file_path)
    animals = []
    for animal in root.findall("animal"):
        animals.append({
            "id": animal.get("id"),
            "species": animal.get("species"),
            "zooid": animal.get("zooid"),
            "name": animal.find("name").text,
            "scientific_name": animal.find("scientific_name").text,
            "habitat": animal.find("habitat").text,
            "diet": animal.find("diet").text,
        })
    return animals

def get_animal_by_id(file_path, animal_id):
    tree, root = load_xml(file_path)
    animal = root.find(f"animal[@id='{animal_id}']")
    if animal:
        return {
            "id": animal.get("id"),
            "species": animal.get("species"),
            "zooid": animal.get("zooid"),
            "name": animal.find("name").text,
            "scientific_name": animal.find("scientific_name").text,
            "habitat": animal.find("habitat").text,
            "diet": animal.find("diet").text,
        }
    return None

def add_animal(file_path, data):
    try:
        tree, root = load_xml(file_path)
        animals = root.findall("animal")  # Obtener todos los nodos animal

        # Validar si el zoo asociado al animal existe
        zoo = root.find(f"zoo[@id='{data['zooid']}']")
        if not zoo:
            return {"success": False, "message": "Zoo ID does not exist. Cannot add animal."}

        # Validar que el nombre del animal sea único dentro del zoo
        existing_animal = root.find(f"animal[@zooid='{data['zooid']}'][name='{data['name']}']")
        if existing_animal:
            return {"success": False, "message": f"Animal with the name '{data['name']}' already exists in zoo '{data['zooid']}'."}

        # Generar un nuevo ID basado en el último nodo
        if animals:
            last_animal = animals[-1]
            new_id = f"animal{int(last_animal.get('id').replace('animal', '')) + 1}"
        else:
            last_animal = None
            new_id = "animal1"

        # Crear el nuevo nodo animal
        new_animal = ET.Element("animal", id=new_id, species=data["species"], zooid=data["zooid"])
        ET.SubElement(new_animal, "name").text = data["name"]
        ET.SubElement(new_animal, "scientific_name").text = data.get("scientific_name", "Unknown")
        ET.SubElement(new_animal, "habitat").text = data["habitat"]
        ET.SubElement(new_animal, "diet").text = data["diet"]

        # Insertar el nuevo nodo en la posición correcta
        if last_animal is not None:
            root.insert(list(root).index(last_animal) + 1, new_animal)
        else:
            root.append(new_animal)

        # Guardar los cambios en el archivo XML
        save_xml(tree, file_path)
        return {"success": True, "id": new_id, "message": "Animal added successfully."}
    except Exception as e:
        print(f"Error in add_animal: {e}")
        return {"success": False, "message": "Failed to add animal."}





def update_animal(file_path, animal_id, data):
    tree, root = load_xml(file_path)
    animal = root.find(f"animal[@id='{animal_id}']")
    if animal:
        animal.set("species", data.get("species", animal.get("species")))
        animal.set("zooid", data.get("zooid", animal.get("zooid")))
        animal.find("name").text = data.get("name", animal.find("name").text)
        animal.find("scientific_name").text = data.get("scientific_name", animal.find("scientific_name").text)
        animal.find("habitat").text = data.get("habitat", animal.find("habitat").text)
        animal.find("diet").text = data.get("diet", animal.find("diet").text)
        save_xml(tree, file_path)
        return True
    return False

def delete_animal(file_path, animal_id):
    tree, root = load_xml(file_path)

    # Encuentra el animal
    animal = root.find(f"animal[@id='{animal_id}']")
    if animal:
        # Eliminar estadísticas asociadas al animal
        delete_conservation_stat(file_path, animal_id)
        # Eliminar el nodo del animal
        root.remove(animal)
        # Guardar los cambios en el archivo XML
        save_xml(tree, file_path)
        return True
    return False



# Funciones para Estadísticas de Conservación
def get_all_conservation_stats(file_path):
    tree, root = load_xml(file_path)
    stats = []
    for stat in root.findall("conservation_statistic"):
        stats.append({
            "animalid": stat.get("animalid"),
            "year": stat.get("year"),
            "population_in_wild": stat.find("population_in_wild").text,
            "population_in_captivity": stat.find("population_in_captivity").text,
            "status": stat.find("status").text,
        })
    return stats

def add_conservation_stat(file_path, data):
    tree, root = load_xml(file_path)
    stats = root.findall("conservation_statistic")  # Obtener todos los nodos conservation_statistic

    # Determinar el último nodo
    if stats:
        last_stat = stats[-1]
    else:
        last_stat = None

    # Crear el nuevo nodo conservation_statistic
    new_stat = ET.Element("conservation_statistic", animalid=data["animalid"], year=data["year"])
    ET.SubElement(new_stat, "population_in_wild").text = data["population_in_wild"]
    ET.SubElement(new_stat, "population_in_captivity").text = data["population_in_captivity"]
    ET.SubElement(new_stat, "status").text = data["status"]

    # Insertar el nuevo nodo en la posición correcta
    if last_stat is not None:
        root.insert(list(root).index(last_stat) + 1, new_stat)
    else:
        root.append(new_stat)

    # Guardar los cambios en el archivo XML
    save_xml(tree, file_path)
    return data["animalid"]


def delete_conservation_stat(file_path, animal_id):
    tree, root = load_xml(file_path)

    # Encuentra todas las estadísticas asociadas al animal_id
    stats_to_remove = root.findall(f"conservation_statistic[@animalid='{animal_id}']")
    if stats_to_remove:
        for stat in stats_to_remove:
            root.remove(stat)

        # Guardar los cambios en el archivo XML
        save_xml(tree, file_path)
        return True

    return False


