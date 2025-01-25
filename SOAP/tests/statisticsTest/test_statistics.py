import unittest
import requests

API_URL = "http://localhost:5000/soap"

def send_request(payload):
    headers = {"Content-Type": "text/xml"}
    response = requests.post(API_URL, data=payload, headers=headers)
    return response.text

class TestConservationStatistics(unittest.TestCase):

    def setUp(self):
        """Limpia el estado antes de cada prueba."""
        self.delete_conservation_statistic_if_exists("animal200", "2025")
        self.delete_conservation_statistic_if_exists("animal201", "2025")

    def delete_conservation_statistic_if_exists(self, animal_id, year):
        """Elimina una estadística de conservación si ya existe."""
        payload = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cons="http://example.com/conservation">
           <soapenv:Header/>
           <soapenv:Body>
              <cons:DeleteConservationStatisticRequest>
                 <animalid>{animal_id}</animalid>
                 <year>{year}</year>
              </cons:DeleteConservationStatisticRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        send_request(payload)

    def test_add_conservation_statistic(self):
        print("Executing: AddConservationStatistic")
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cons="http://example.com/conservation">
           <soapenv:Header/>
           <soapenv:Body>
              <cons:AddConservationStatisticRequest>
                 <animalid>animal200</animalid>
                 <year>2025</year>
                 <population_in_wild>5000</population_in_wild>
                 <population_in_captivity>300</population_in_captivity>
                 <status>Endangered</status>
              </cons:AddConservationStatisticRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<response>Conservation statistic for animal ID animal200 in year 2025 added successfully</response>"
        self.assertIn(expected_response, response)

    def test_add_duplicate_conservation_statistic(self):
        print("Executing: AddDuplicateConservationStatistic")
        self.test_add_conservation_statistic()
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cons="http://example.com/conservation">
           <soapenv:Header/>
           <soapenv:Body>
              <cons:AddConservationStatisticRequest>
                 <animalid>animal200</animalid>
                 <year>2025</year>
                 <population_in_wild>5000</population_in_wild>
                 <population_in_captivity>300</population_in_captivity>
                 <status>Endangered</status>
              </cons:AddConservationStatisticRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<response>Conservation statistic for animal ID animal200 in year 2025 already exists</response>"
        self.assertIn(expected_response, response)

    def test_update_conservation_statistic(self):
        print("Executing: UpdateConservationStatistic")
        self.test_add_conservation_statistic()
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cons="http://example.com/conservation">
           <soapenv:Header/>
           <soapenv:Body>
              <cons:UpdateConservationStatisticRequest>
                 <animalid>animal200</animalid>
                 <year>2025</year>
                 <population_in_wild>6000</population_in_wild>
                 <population_in_captivity>400</population_in_captivity>
                 <status>Critically Endangered</status>
              </cons:UpdateConservationStatisticRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<response>Conservation statistic for animal ID animal200 in year 2025 updated successfully</response>"
        self.assertIn(expected_response, response)

    def test_update_conservation_statistic_not_found(self):
        print("Executing: UpdateConservationStatisticNotFound")
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cons="http://example.com/conservation">
           <soapenv:Header/>
           <soapenv:Body>
              <cons:UpdateConservationStatisticRequest>
                 <animalid>animal999</animalid>
                 <year>2025</year>
                 <population_in_wild>500</population_in_wild>
                 <population_in_captivity>50</population_in_captivity>
                 <status>Least Concern</status>
              </cons:UpdateConservationStatisticRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<response>Conservation statistic for animal ID animal999 in year 2025 not found</response>"
        self.assertIn(expected_response, response)

    def test_get_conservation_statistic_by_id(self):
        print("Executing: GetConservationStatisticById")
        self.test_add_conservation_statistic()
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cons="http://example.com/conservation">
           <soapenv:Header/>
           <soapenv:Body>
              <cons:GetConservationStatisticByIdRequest>
                 <animalid>animal200</animalid>
                 <year>2025</year>
              </cons:GetConservationStatisticByIdRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<conservation_statistic animalid=\"animal200\" year=\"2025\">"
        self.assertIn(expected_response, response)

    def test_get_conservation_statistic_not_found(self):
        print("Executing: GetConservationStatisticNotFound")
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cons="http://example.com/conservation">
           <soapenv:Header/>
           <soapenv:Body>
              <cons:GetConservationStatisticByIdRequest>
                 <animalid>animal999</animalid>
                 <year>2025</year>
              </cons:GetConservationStatisticByIdRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<response>Conservation statistic for animal ID animal999 in year 2025 not found</response>"
        self.assertIn(expected_response, response)

    def test_delete_conservation_statistic(self):
        print("Executing: DeleteConservationStatistic")
        self.test_add_conservation_statistic()
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cons="http://example.com/conservation">
           <soapenv:Header/>
           <soapenv:Body>
              <cons:DeleteConservationStatisticRequest>
                 <animalid>animal200</animalid>
                 <year>2025</year>
              </cons:DeleteConservationStatisticRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<response>Conservation statistic for animal ID animal200 in year 2025 removed successfully</response>"
        self.assertIn(expected_response, response)

    def test_delete_conservation_statistic_not_found(self):
        print("Executing: DeleteConservationStatisticNotFound")
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cons="http://example.com/conservation">
           <soapenv:Header/>
           <soapenv:Body>
              <cons:DeleteConservationStatisticRequest>
                 <animalid>animal999</animalid>
                 <year>2025</year>
              </cons:DeleteConservationStatisticRequest>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        expected_response = "<response>Conservation statistic for animal ID animal999 in year 2025 not found</response>"
        self.assertIn(expected_response, response)

    def test_list_all_conservation_statistics(self):
        print("Executing: ListAllConservationStatistics")
        self.test_add_conservation_statistic()
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cons="http://example.com/conservation">
           <soapenv:Header/>
           <soapenv:Body>
              <cons:ListAllConservationStatisticsRequest/>
           </soapenv:Body>
        </soapenv:Envelope>"""
        print(f"Request:\n{payload}")
        response = send_request(payload)
        print(f"Response:\n{response}")
        self.assertIn("<conservation_statistic animalid=\"animal200\"", response)
        self.assertIn("<conservation_statistics>", response)
        self.assertIn("</conservation_statistics>", response)

if __name__ == "__main__":
    unittest.main()
