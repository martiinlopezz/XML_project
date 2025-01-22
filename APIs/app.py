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
    return jsonify(get_all_zoos(XML_FILE))

@app.route('/zoos/<zoo_id>', methods=['GET'])
def get_zoo(zoo_id):
    zoo = get_zoo_by_id(XML_FILE, zoo_id)
    if zoo:
        return jsonify(zoo)
    return jsonify({"error": "Zoo not found"}), 404

@app.route('/zoos', methods=['POST'])
def create_zoo():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    result = add_zoo(XML_FILE, data)

    if result["success"]:
        return jsonify({"message": result["message"], "id": result["id"]}), 201
    else:
        return jsonify({"error": result["message"]}), 400


@app.route('/zoos/<zoo_id>', methods=['PUT'])
def modify_zoo(zoo_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400
    if update_zoo(XML_FILE, zoo_id, data):
        return jsonify({"message": "Zoo updated"})
    return jsonify({"error": "Zoo not found"}), 404

@app.route('/zoos/<zoo_id>', methods=['DELETE'])
def delete_zoo_endpoint(zoo_id):
    try:
        deleted = delete_zoo(XML_FILE, zoo_id)  # Aquí pasamos correctamente los argumentos
        if deleted:
            return jsonify({"message": f"Zoo {zoo_id} and its associated animals deleted successfully."})
        return jsonify({"error": f"Zoo {zoo_id} not found."}), 404
    except Exception as e:
        print(f"Error in delete_zoo endpoint: {e}")
        return jsonify({"error": "Failed to delete zoo."}), 500




# Rutas para Animales
@app.route('/animals', methods=['GET'])
def list_animals():
    return jsonify(get_all_animals(XML_FILE))

@app.route('/animals/<animal_id>', methods=['GET'])
def get_animal(animal_id):
    animal = get_animal_by_id(XML_FILE, animal_id)
    if animal:
        return jsonify(animal)
    return jsonify({"error": "Animal not found"}), 404

@app.route('/animals', methods=['POST'])
def create_animal():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    result = add_animal(XML_FILE, data)

    if result["success"]:
        return jsonify({"message": result["message"], "id": result["id"]}), 201
    else:
        return jsonify({"error": result["message"]}), 400


@app.route('/animals/<animal_id>', methods=['PUT'])
def modify_animal(animal_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400
    if update_animal(XML_FILE, animal_id, data):
        return jsonify({"message": "Animal updated"})
    return jsonify({"error": "Animal not found"}), 404

@app.route('/animals/<animal_id>', methods=['DELETE'])
def delete_animal_route(animal_id):
    deleted = delete_animal(XML_FILE, animal_id)
    if deleted:
        return jsonify({"message": "Animal deleted successfully"}), 200
    return jsonify({"error": "Animal not found"}), 404


# Rutas para estadísticas de conservación
@app.route('/conservation_stats', methods=['GET'])
def list_stats():
    return jsonify(get_all_conservation_stats(XML_FILE))

@app.route('/conservation_stats', methods=['POST'])
def create_stat():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400
    new_id = add_conservation_stat(XML_FILE, data)
    return jsonify({"message": "Stat added", "id": new_id}), 201

@app.route('/conservation_stats/<animal_id>', methods=['DELETE'])
def remove_stat(animal_id):
    if delete_conservation_stat(XML_FILE, animal_id):
        return jsonify({"message": "Stat deleted"})
    return jsonify({"error": "Stat not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
