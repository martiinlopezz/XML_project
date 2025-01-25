import unittest
import requests

API_URL = "http://localhost:5000/soap"

def send_request(payload):
    headers = {"Content-Type": "text/xml"}
    response = requests.post(API_URL, data=payload, headers=headers)
    return response.text

class TestAnimalOperations(unittest.TestCase):

    def setUp(self):
        """Limpia el estado antes de cada prueba."""
        self.delete_animal_if_exists("animal200")
        self.delete_animal_if_exists("animal201")

    def delete_animal_if_exists(self, animal_id):
        """Elimina un animal si ya existe."""
        payload = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ani="http://example.com/animal">
           <soapenv:Header/>
           <soapenv:Body>
              <ani:DeleteAnimalRequest>
                 <id>{animal_id}</id>
              </ani:DeleteAnimalRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        send_request(payload)

    def test_add_animal(self):
        print("Executing: AddAnimal")
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ani="http://example.com/animal">
           <soapenv:Header/>
           <soapenv:Body>
              <ani:AddAnimalRequest>
                 <id>animal200</id>
                 <species>Mammal</species>
                 <zooid>zoo01</zooid>
                 <name>Test Animal</name>
                 <scientific_name>Testus animalus</scientific_name>
                 <habitat>Test Habitat</habitat>
                 <diet>Herbivore</diet>
              </ani:AddAnimalRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<response>Animal with ID animal200 added successfully</response>"
        self.assertIn(expected_response, response)

    def test_add_duplicate_animal(self):
        print("Executing: AddDuplicateAnimal")
        self.test_add_animal()
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ani="http://example.com/animal">
           <soapenv:Header/>
           <soapenv:Body>
              <ani:AddAnimalRequest>
                 <id>animal200</id>
                 <species>Bird</species>
                 <zooid>zoo02</zooid>
                 <name>Duplicate Animal</name>
                 <scientific_name>Duplicatus animalus</scientific_name>
                 <habitat>Duplicate Habitat</habitat>
                 <diet>Carnivore</diet>
              </ani:AddAnimalRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<response>Animal with ID animal200 already exists</response>"
        self.assertIn(expected_response, response)

    def test_update_animal(self):
        print("Executing: UpdateAnimal")
        self.test_add_animal()
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ani="http://example.com/animal">
           <soapenv:Header/>
           <soapenv:Body>
              <ani:UpdateAnimalRequest>
                 <id>animal200</id>
                 <species>Updated Mammal</species>
                 <zooid>zoo01</zooid>
                 <name>Updated Test Animal</name>
                 <scientific_name>Updatedus animalus</scientific_name>
                 <habitat>Updated Habitat</habitat>
                 <diet>Omnivore</diet>
              </ani:UpdateAnimalRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<response>Animal with ID animal200 updated successfully</response>"
        self.assertIn(expected_response, response)

    def test_update_animal_not_found(self):
        print("Executing: UpdateAnimalNotFound")
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ani="http://example.com/animal">
           <soapenv:Header/>
           <soapenv:Body>
              <ani:UpdateAnimalRequest>
                 <id>animal999</id>
                 <species>Nonexistent Species</species>
                 <zooid>zoo99</zooid>
                 <name>Nonexistent Animal</name>
                 <scientific_name>Nonexistus animalus</scientific_name>
                 <habitat>Nonexistent Habitat</habitat>
                 <diet>Carnivore</diet>
              </ani:UpdateAnimalRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<response>Animal with ID animal999 not found</response>"
        self.assertIn(expected_response, response)

    def test_get_animal_by_id(self):
        print("Executing: GetAnimalById")
        self.test_add_animal()
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ani="http://example.com/animal">
           <soapenv:Header/>
           <soapenv:Body>
              <ani:GetAnimalByIdRequest>
                 <id>animal200</id>
              </ani:GetAnimalByIdRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<animal id=\"animal200\""
        self.assertIn(expected_response, response)

    def test_get_animal_not_found(self):
        print("Executing: GetAnimalNotFound")
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ani="http://example.com/animal">
           <soapenv:Header/>
           <soapenv:Body>
              <ani:GetAnimalByIdRequest>
                 <id>animal999</id>
              </ani:GetAnimalByIdRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<response>Animal with ID animal999 not found</response>"
        self.assertIn(expected_response, response)

    def test_delete_animal(self):
        print("Executing: DeleteAnimal")
        self.test_add_animal()
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ani="http://example.com/animal">
           <soapenv:Header/>
           <soapenv:Body>
              <ani:DeleteAnimalRequest>
                 <id>animal200</id>
              </ani:DeleteAnimalRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<response>Animal with ID animal200 removed successfully</response>"
        self.assertIn(expected_response, response)

    def test_delete_animal_not_found(self):
        print("Executing: DeleteAnimalNotFound")
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ani="http://example.com/animal">
           <soapenv:Header/>
           <soapenv:Body>
              <ani:DeleteAnimalRequest>
                 <id>animal999</id>
              </ani:DeleteAnimalRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<response>Animal with ID animal999 not found</response>"
        self.assertIn(expected_response, response)

    def test_list_all_animals(self):
        print("Executing: ListAllAnimals")
        self.test_add_animal()
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ani="http://example.com/animal">
           <soapenv:Header/>
           <soapenv:Body>
              <ani:ListAllAnimalsRequest/>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        self.assertIn("<animal id=\"animal200\"", response)
        self.assertIn("<animals>", response)
        self.assertIn("</animals>", response)

if __name__ == "__main__":
    unittest.main()
