import unittest
import requests

API_URL = "http://localhost:5000/soap"

def send_request(payload):
    headers = {"Content-Type": "text/xml"}
    response = requests.post(API_URL, data=payload, headers=headers)
    return response.text

class TestZooOperations(unittest.TestCase):

    def setUp(self):
        """Limpia el estado antes de cada prueba."""
        self.delete_zoo_if_exists("zoo100")
        self.delete_zoo_if_exists("zoo101")

    def delete_zoo_if_exists(self, zoo_id):
        """Elimina un zoológico si ya existe."""
        payload = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:zoo="http://example.com/zoo">
           <soapenv:Header/>
           <soapenv:Body>
              <zoo:DeleteZooRequest>
                 <id>{zoo_id}</id>
              </zoo:DeleteZooRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        send_request(payload)

    def test_add_zoo(self):
        print("Executing: AddZoo")
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:zoo="http://example.com/zoo">
           <soapenv:Header/>
           <soapenv:Body>
              <zoo:AddZooRequest>
                 <id>zoo100</id>
                 <location>Europe</location>
                 <name>Test Zoo</name>
                 <city>Test City</city>
                 <foundation>2025</foundation>
              </zoo:AddZooRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<response>Zoo with ID zoo100 added successfully</response>"
        self.assertIn(expected_response, response)

    def test_add_duplicate_zoo(self):
        print("Executing: AddDuplicateZoo")
        self.test_add_zoo()
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:zoo="http://example.com/zoo">
           <soapenv:Header/>
           <soapenv:Body>
              <zoo:AddZooRequest>
                 <id>zoo100</id>
                 <location>Europe</location>
                 <name>Duplicate Zoo</name>
                 <city>Duplicate City</city>
                 <foundation>2025</foundation>
              </zoo:AddZooRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<response>Zoo with ID zoo100 already exists</response>"
        self.assertIn(expected_response, response)

    def test_get_zoo_by_id(self):
        print("Executing: GetZooById")
        self.test_add_zoo()
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:zoo="http://example.com/zoo">
           <soapenv:Header/>
           <soapenv:Body>
              <zoo:GetZooByIdRequest>
                 <id>zoo100</id>
              </zoo:GetZooByIdRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<zoo id=\"zoo100\" location=\"Europe\">"
        self.assertIn(expected_response, response)

    def test_get_zoo_not_found(self):
        print("Executing: GetZooNotFound")
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:zoo="http://example.com/zoo">
           <soapenv:Header/>
           <soapenv:Body>
              <zoo:GetZooByIdRequest>
                 <id>zoo999</id>
              </zoo:GetZooByIdRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<response>Zoo with ID zoo999 not found</response>"
        self.assertIn(expected_response, response)

    def test_delete_zoo(self):
        print("Executing: DeleteZoo")
        self.test_add_zoo()
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:zoo="http://example.com/zoo">
           <soapenv:Header/>
           <soapenv:Body>
              <zoo:DeleteZooRequest>
                 <id>zoo100</id>
              </zoo:DeleteZooRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<response>Zoo with ID zoo100 removed successfully</response>"
        self.assertIn(expected_response, response)

    def test_delete_zoo_not_found(self):
        print("Executing: DeleteZooNotFound")
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:zoo="http://example.com/zoo">
           <soapenv:Header/>
           <soapenv:Body>
              <zoo:DeleteZooRequest>
                 <id>zoo999</id>
              </zoo:DeleteZooRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<response>Zoo with ID zoo999 not found</response>"
        self.assertIn(expected_response, response)

    def test_update_zoo(self):
        print("Executing: UpdateZoo")
        self.test_add_zoo()
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:zoo="http://example.com/zoo">
           <soapenv:Header/>
           <soapenv:Body>
              <zoo:UpdateZooRequest>
                 <id>zoo100</id>
                 <location>Updated Europe</location>
                 <name>Updated Test Zoo</name>
                 <city>Updated City</city>
                 <foundation>2030</foundation>
              </zoo:UpdateZooRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<response>Zoo with ID zoo100 updated successfully</response>"
        self.assertIn(expected_response, response)

    def test_update_zoo_not_found(self):
        print("Executing: UpdateZooNotFound")
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:zoo="http://example.com/zoo">
           <soapenv:Header/>
           <soapenv:Body>
              <zoo:UpdateZooRequest>
                 <id>zoo999</id>
                 <location>Nonexistent Location</location>
                 <name>Nonexistent Zoo</name>
                 <city>Nonexistent City</city>
                 <foundation>2000</foundation>
              </zoo:UpdateZooRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<response>Zoo with ID zoo999 not found</response>"
        self.assertIn(expected_response, response)

    def test_list_all_zoos(self):
        print("Executing: ListAllZoos")
        # Add multiple zoos
        self.test_add_zoo()
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:zoo="http://example.com/zoo">
           <soapenv:Header/>
           <soapenv:Body>
              <zoo:AddZooRequest>
                 <id>zoo101</id>
                 <location>America</location>
                 <name>Second Zoo</name>
                 <city>Second City</city>
                 <foundation>2023</foundation>
              </zoo:AddZooRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")

        # List all zoos
        payload_list = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:zoo="http://example.com/zoo">
           <soapenv:Header/>
           <soapenv:Body>
              <zoo:ListAllZoosRequest/>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request for ListAllZoos:\n{payload_list}")
        response_list = send_request(payload_list)
        print(f"Response:\n{response_list}")
        self.assertIn("<zoo id=\"zoo100\"", response_list)
        self.assertIn("<zoo id=\"zoo101\"", response_list)
        self.assertIn("<zoos>", response_list)
        self.assertIn("</zoos>", response_list)

if __name__ == "__main__":
    unittest.main()
