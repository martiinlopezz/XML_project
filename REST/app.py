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
    deleted = delete_animal(XML_FILE, animal_id)
    if deleted:
        response = jsonify({"message": "Animal deleted successfully"})
        print(f"DELETE /animals/{animal_id} Response:", response.json)
        return response, 200
    response = jsonify({"error": "Animal not found"})
    print(f"DELETE /animals/{animal_id} Response:", response.json)
    return response, 404

# Rutas para estadísticas de conservación
@app.route('/conservation_stats', methods=['GET'])
def list_stats():
    response = jsonify(get_all_conservation_stats(XML_FILE))
    print("GET /conservation_stats Response:", response.json)
    return response

@app.route('/conservation_stats/<animal_id>', methods=['GET'])
def get_stat_by_animal(animal_id):
    stats = get_all_conservation_stats(XML_FILE)  # Obtiene todas las estadísticas
    filtered_stats = [stat for stat in stats if stat["animalid"] == animal_id]  # Filtra por animal_id
    
    if filtered_stats:
        response = jsonify(filtered_stats)
        print(f"GET /conservation_stats/{animal_id} Response:", response.json)
        return response
    response = jsonify({"error": "No statistics found for the given animal ID"})
    print(f"GET /conservation_stats/{animal_id} Response:", response.json)
    return response, 404


@app.route('/conservation_stats', methods=['POST'])
def create_stat():
    data = request.get_json()
    print("POST /conservation_stats Request Data:", data)
    if not data:
        response = jsonify({"error": "Invalid or missing JSON"})
        print("POST /conservation_stats Response:", response.json)
        return response, 400
    new_id = add_conservation_stat(XML_FILE, data)
    response = jsonify({"message": "Stat added", "id": new_id})
    print("POST /conservation_stats Response:", response.json)
    return response, 201

@app.route('/conservation_stats/<animal_id>', methods=['DELETE'])
def remove_stat(animal_id):
    if delete_conservation_stat(XML_FILE, animal_id):
        response = jsonify({"message": "Stat deleted"})
        print(f"DELETE /conservation_stats/{animal_id} Response:", response.json)
        return response
    response = jsonify({"error": "Stat not found"})
    print(f"DELETE /conservation_stats/{animal_id} Response:", response.json)
    return response, 404

if __name__ == '__main__':
    app.run(debug=True)
