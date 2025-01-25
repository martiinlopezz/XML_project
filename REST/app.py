from flask import Flask, request, jsonify, render_template
from utils.xml_utils import (
    get_all_zoos,
    get_zoo_by_id,
    add_zoo,
    update_zoo,
    delete_zoo,
    get_all_animals,
    get_animal_by_id,
    add_animal,
    update_animal,
    delete_animal,
    get_all_conservation_stats,
    add_conservation_stat,
    delete_conservation_stat,
)

app = Flask(__name__)

XML_FILE = "data/zoo.xml"

# Página principal
@app.route('/')
def home():
    return render_template('index.html')

# Rutas para Zoos
@app.route('/zoos', methods=['GET'])
def list_zoos():
    response = jsonify(get_all_zoos(XML_FILE))
    print("GET /zoos Response:", response.json)
    return response

@app.route('/zoos/<zoo_id>', methods=['GET'])
def get_zoo(zoo_id):
    zoo = get_zoo_by_id(XML_FILE, zoo_id)
    if zoo:
        response = jsonify(zoo)
        print(f"GET /zoos/{zoo_id} Response:", response.json)
        return response
    response = jsonify({"error": "Zoo not found"})
    print(f"GET /zoos/{zoo_id} Response:", response.json)
    return response, 404

@app.route('/zoos', methods=['POST'])
def create_zoo():
    data = request.get_json()
    print("POST /zoos Request Data:", data)
    if not data:
        response = jsonify({"error": "Invalid or missing JSON"})
        print("POST /zoos Response:", response.json)
        return response, 400

    result = add_zoo(XML_FILE, data)

    if result["success"]:
        response = jsonify({"message": result["message"], "id": result["id"]})
        print("POST /zoos Response:", response.json)
        return response, 201
    else:
        response = jsonify({"error": result["message"]})
        print("POST /zoos Response:", response.json)
        return response, 400

@app.route('/zoos/<zoo_id>', methods=['PUT'])
def modify_zoo(zoo_id):
    data = request.get_json()
    print(f"PUT /zoos/{zoo_id} Request Data:", data)
    if not data:
        response = jsonify({"error": "Invalid or missing JSON"})
        print(f"PUT /zoos/{zoo_id} Response:", response.json)
        return response, 400
    if update_zoo(XML_FILE, zoo_id, data):
        response = jsonify({"message": "Zoo updated"})
        print(f"PUT /zoos/{zoo_id} Response:", response.json)
        return response
    response = jsonify({"error": "Zoo not found"})
    print(f"PUT /zoos/{zoo_id} Response:", response.json)
    return response, 404

@app.route('/zoos/<zoo_id>', methods=['DELETE'])
def delete_zoo_endpoint(zoo_id):
    try:
        deleted = delete_zoo(XML_FILE, zoo_id)
        if deleted:
            response = jsonify({"message": f"Zoo {zoo_id} and its associated animals deleted successfully."})
            print(f"DELETE /zoos/{zoo_id} Response:", response.json)
            return response
        response = jsonify({"error": f"Zoo {zoo_id} not found."})
        print(f"DELETE /zoos/{zoo_id} Response:", response.json)
        return response, 404
    except Exception as e:
        print(f"Error in delete_zoo endpoint: {e}")
        response = jsonify({"error": "Failed to delete zoo."})
        print(f"DELETE /zoos/{zoo_id} Response:", response.json)
        return response, 500

# Rutas para Animales
@app.route('/animals', methods=['GET'])
def list_animals():
    response = jsonify(get_all_animals(XML_FILE))
    print("GET /animals Response:", response.json)
    return response

@app.route('/animals/<animal_id>', methods=['GET'])
def get_animal(animal_id):
    animal = get_animal_by_id(XML_FILE, animal_id)
    if animal:
        response = jsonify(animal)
        print(f"GET /animals/{animal_id} Response:", response.json)
        return response
    response = jsonify({"error": "Animal not found"})
    print(f"GET /animals/{animal_id} Response:", response.json)
    return response, 404

@app.route('/animals', methods=['POST'])
def create_animal():
    data = request.get_json()
    print("POST /animals Request Data:", data)
    if not data:
        response = jsonify({"error": "Invalid or missing JSON"})
        print("POST /animals Response:", response.json)
        return response, 400

    result = add_animal(XML_FILE, data)

    if result["success"]:
        response = jsonify({"message": result["message"], "id": result["id"]})
        print("POST /animals Response:", response.json)
        return response, 201
    else:
        response = jsonify({"error": result["message"]})
        print("POST /animals Response:", response.json)
        return response, 400

@app.route('/animals/<animal_id>', methods=['PUT'])
def modify_animal(animal_id):
    data = request.get_json()
    print(f"PUT /animals/{animal_id} Request Data:", data)
    if not data:
        response = jsonify({"error": "Invalid or missing JSON"})
        print(f"PUT /animals/{animal_id} Response:", response.json)
        return response, 400
    if update_animal(XML_FILE, animal_id, data):
        response = jsonify({"message": "Animal updated"})
        print(f"PUT /animals/{animal_id} Response:", response.json)
        return response
    response = jsonify({"error": "Animal not found"})
    print(f"PUT /animals/{animal_id} Response:", response.json)
    return response, 404

@app.route('/animals/<animal_id>', methods=['DELETE'])
def delete_animal_route(animal_id):
    try:
        # Primero eliminamos el animal
        animal_deleted = delete_animal(XML_FILE, animal_id)

        if animal_deleted:
            # Intentar eliminar estadísticas asociadas al animal
            stats_deleted = delete_conservation_stat(XML_FILE, animal_id)

            if stats_deleted:
                return jsonify({"message": f"Animal {animal_id} and its associated conservation stats deleted successfully."}), 200
            else:
                return jsonify({"message": f"Animal {animal_id} deleted, but no associated conservation stats found."}), 200

        return jsonify({"error": "Animal not found"}), 404
    except Exception as e:
        print(f"Error deleting animal {animal_id}: {e}")
        return jsonify({"error": "Failed to delete animal"}), 500

# Rutas para estadísticas de conservación
@app.route('/conservation_stats', methods=['GET'])
def list_stats():
    try:
        response = jsonify(get_all_conservation_stats(XML_FILE))
        return response
    except Exception as e:
        print(f"Error fetching conservation stats: {e}")
        return jsonify({"error": "Failed to fetch conservation stats"}), 500

@app.route('/conservation_stats/<animal_id>', methods=['GET'])
def get_stat_by_animal(animal_id):
    try:
        stats = get_all_conservation_stats(XML_FILE)
        filtered_stats = [stat for stat in stats if stat["animalid"] == animal_id]
        if filtered_stats:
            return jsonify(filtered_stats)
        return jsonify({"error": "No statistics found for the given animal ID"}), 404
    except Exception as e:
        print(f"Error fetching stats for animal {animal_id}: {e}")
        return jsonify({"error": "Failed to fetch conservation stats"}), 500

@app.route('/conservation_stats', methods=['POST'])
def create_stat():
    data = request.get_json()
    if not data or not all(k in data for k in ["animalid", "year", "population_in_wild", "population_in_captivity", "status"]):
        return jsonify({"error": "Invalid or missing JSON fields"}), 400

    new_id = add_conservation_stat(XML_FILE, data)
    if new_id:
        return jsonify({"message": "Stat added", "id": new_id}), 201
    return jsonify({"error": "Failed to add conservation stat"}), 500

@app.route('/conservation_stats/<animal_id>', methods=['DELETE'])
def remove_stat(animal_id):
    try:
        if delete_conservation_stat(XML_FILE, animal_id):
            return jsonify({"message": "Stat deleted"}), 200
        return jsonify({"error": "Stat not found"}), 404
    except Exception as e:
        print(f"Error deleting stat for animal {animal_id}: {e}")
        return jsonify({"error": "Failed to delete stat"}), 500

if __name__ == '__main__':
    app.run(debug=True)
