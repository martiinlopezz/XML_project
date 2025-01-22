from flask import Flask, request, jsonify, Response
from utils.xml_utils import *
from wsdl.wsdl_generator import generate_wsdl


app = Flask(__name__)
app.add_url_rule("/wsdl", "generate_wsdl", generate_wsdl)


@app.route("/", methods=["GET"])
def index():
    """
    Endpoint raíz de la aplicación.
    Redirige al WSDL o muestra una página de inicio.
    """
    return """
    <h1>Bienvenido al Servicio SOAP de Zoológicos</h1>
    <p>Consulta el archivo WSDL en <a href="/wsdl">/wsdl</a>.</p>
    """

@app.route("/list_routes", methods=["GET"])
def list_routes():
    """
    Lista todas las rutas disponibles en la aplicación Flask.
    """
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(f"{rule.rule} -> {rule.endpoint}")
    return "<br>".join(routes)

@app.route("/wsdl", methods=["GET"])
def generate_wsdl():
    """
    Genera dinámicamente el archivo WSDL basado en las operaciones definidas.
    """
    wsdl_content = """<?xml version="1.0" encoding="UTF-8"?>
    <!-- Aquí estaría tu WSDL generado dinámicamente -->
    """
    return Response(wsdl_content, content_type="text/xml")

@app.route("/get_zoo_info", methods=["POST"])
def get_zoo_info_service():
    """
    Endpoint para obtener información sobre un zoológico a partir de su ID.
    """
    try:
        zoo_id = request.json.get("zoo_id")
        if not zoo_id:
            return jsonify({"error": "El parámetro 'zoo_id' es obligatorio"}), 400

        response = get_zoo_info(zoo_id)
        if response:
            return jsonify({"zoo_info": response})
        else:
            return jsonify({"error": f"No se encontró un zoológico con el ID: {zoo_id}"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al procesar la solicitud: {str(e)}"}), 500


@app.route("/add_zoo", methods=["POST"])
def add_zoo_service():
    """
    Endpoint para agregar un nuevo zoológico al archivo XML.
    """
    try:
        data = request.json
        zoo_id = data.get("zoo_id")
        name = data.get("name")
        city = data.get("city")
        foundation = data.get("foundation")
        location = data.get("location")

        # Validación básica
        if not (zoo_id and name and city and foundation and location):
            return jsonify({"error": "Todos los campos son obligatorios"}), 400

        success = add_zoo(zoo_id, name, city, foundation, location)
        if success:
            return jsonify({"message": "Zoológico agregado exitosamente"}), 201
        else:
            return jsonify({"error": "No se pudo agregar el zoológico"}), 500
    except Exception as e:
        return jsonify({"error": f"Error al procesar la solicitud: {str(e)}"}), 500


@app.route("/delete_zoo", methods=["POST"])
def delete_zoo_service():
    zoo_id = request.json.get("zoo_id")

    if not zoo_id:
        return jsonify({"error": "El parámetro 'zoo_id' es obligatorio"}), 400

    if delete_zoo(zoo_id):
        return jsonify({"message": "Zoológico eliminado exitosamente"}), 200
    else:
        return jsonify({"error": f"No se encontró un zoológico con ID: {zoo_id}"}), 404


@app.route("/update_zoo_info", methods=["POST"])
def update_zoo_info_service():
    data = request.json
    zoo_id = data.get("zoo_id")
    name = data.get("name")
    city = data.get("city")
    foundation = data.get("foundation")
    location = data.get("location")

    if not zoo_id:
        return jsonify({"error": "El parámetro 'zoo_id' es obligatorio"}), 400

    if update_zoo_info(zoo_id, name, city, foundation, location):
        return jsonify({"message": "Información del zoológico actualizada exitosamente"}), 200
    else:
        return jsonify({"error": f"No se encontró un zoológico con ID: {zoo_id}"}), 404


@app.route("/list_zoos", methods=["GET"])
def list_zoos_service():
    return jsonify({"zoos": list_zoos()}), 200


@app.route("/list_zoos_with_animals", methods=["GET"])
def list_all_zoos_with_animals():
    """
    Endpoint para listar zoológicos con sus animales asociados.
    """
    zoos = list_zoos_with_animals()
    return jsonify({"zoos": zoos}), 200

@app.route("/get_zoo_with_most_animals", methods=["GET"])
def get_zoo_with_most_animals_service():
    """
    Endpoint para obtener el zoológico con más animales.
    """
    zoo = get_zoo_with_most_animals()
    if "zoo_id" in zoo:
        return jsonify(zoo), 200
    else:
        return jsonify(zoo), 404


@app.route("/list_zoos_with_animals", methods=["GET"])
def list_zoos_with_animals_service():
    """
    Endpoint para listar zoológicos con sus animales asociados.
    """
    zoos = list_zoos_with_animals()
    return jsonify({"zoos": zoos}), 200

@app.route("/get_animal", methods=["POST"])
def get_animal_service():
    """
    Endpoint para obtener información sobre un animal a partir de su ID.
    """
    try:
        animal_id = request.json.get("animal_id")
        if not animal_id:
            return jsonify({"error": "El parámetro 'animal_id' es obligatorio"}), 400

        response = get_animal_info(animal_id)
        if response:
            return jsonify({"animal_info": response})
        else:
            return jsonify({"error": f"No se encontró un animal con el ID: {animal_id}"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al procesar la solicitud: {str(e)}"}), 500


@app.route("/add_animal", methods=["POST"])
def add_animal_service():
    """
    Endpoint para agregar un nuevo animal al archivo XML.
    """
    try:
        data = request.json
        animal_id = data.get("animal_id")
        zoo_id = data.get("zoo_id")
        name = data.get("name")
        species = data.get("species")
        scientific_name = data.get("scientific_name")
        habitat = data.get("habitat")
        diet = data.get("diet")

        # Validación básica
        if not (animal_id and zoo_id and name and species and scientific_name and habitat and diet):
            return jsonify({"error": "Todos los campos son obligatorios"}), 400

        # Llamada a la función para agregar al XML
        success = add_animal(animal_id, zoo_id, name, species, scientific_name, habitat, diet)
        if success:
            return jsonify({"message": "Animal agregado exitosamente"}), 201
        else:
            return jsonify({"error": "No se pudo agregar el animal"}), 500
    except Exception as e:
        return jsonify({"error": f"Error al procesar la solicitud: {str(e)}"}), 500


@app.route("/delete_animal", methods=["POST"])
def delete_animal_service():
    """
    Endpoint para eliminar un animal del archivo XML.
    """
    try:
        animal_id = request.json.get("animal_id")
        if not animal_id:
            return jsonify({"error": "El parámetro 'animal_id' es obligatorio"}), 400

        success = delete_animal(animal_id)
        if success:
            return jsonify({"message": "Animal eliminado exitosamente"}), 200
        else:
            return jsonify({"error": f"No se encontró un animal con el ID: {animal_id}"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al procesar la solicitud: {str(e)}"}), 500


@app.route("/update_animal_info", methods=["POST"])
def update_animal_info_service():
    data = request.json
    animal_id = data.get("animal_id")
    name = data.get("name")
    species = data.get("species")
    scientific_name = data.get("scientific_name")
    habitat = data.get("habitat")
    diet = data.get("diet")

    if not animal_id:
        return jsonify({"error": "El parámetro 'animal_id' es obligatorio"}), 400

    if update_animal_info(animal_id, name, species, scientific_name, habitat, diet):
        return jsonify({"message": "Información del animal actualizada exitosamente"}), 200
    else:
        return jsonify({"error": f"No se encontró un animal con ID: {animal_id}"}), 404


@app.route("/list_animals", methods=["GET"])
def list_animals_service():
    return jsonify({"animals": list_animals()}), 200


@app.route("/get_animals_by_zoo", methods=["POST"])
def get_animals_by_zoo_service():
    zoo_id = request.json.get("zoo_id")

    if not zoo_id:
        return jsonify({"error": "El parámetro 'zoo_id' es obligatorio"}), 400

    return jsonify({"animals": get_animals_by_zoo(zoo_id)}), 200

@app.route("/count_animals_in_zoo", methods=["POST"])
def count_animals_in_zoo_service():
    zoo_id = request.json.get("zoo_id")

    if not zoo_id:
        return jsonify({"error": "El parámetro 'zoo_id' es obligatorio"}), 400

    count = count_animals_in_zoo(zoo_id)
    return jsonify({"zoo_id": zoo_id, "animal_count": count}), 200

@app.route("/get_animals_by_species", methods=["POST"])
def get_animals_by_species_service():
    """
    Endpoint para obtener animales filtrados por especie.
    """
    species = request.json.get("species")

    if not species:
        return jsonify({"error": "El parámetro 'species' es obligatorio"}), 400

    animals = get_animals_by_species(species)
    if animals:
        return jsonify({"species": species, "animals": animals}), 200
    else:
        return jsonify({"message": f"No se encontraron animales de la especie: {species}"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=8000)
