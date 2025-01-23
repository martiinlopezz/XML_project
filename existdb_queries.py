import requests

# eXistDB Configuration
EXISTDB_URL = "http://localhost:8080/exist/rest/db/zoo"  # Change '/db/zoo' to your collection path
USERNAME = "admin"
PASSWORD = ""


# Function to execute XQuery queries
def execute_xquery(query):
    try:
        # Send the query as a parameter in the URL
        params = {"_query": query}  # Send the query in the parameters
        response = requests.get(
            EXISTDB_URL,
            params=params,
            auth=(USERNAME, PASSWORD)
        )

        # Handle response errors
        if response.status_code == 200:
            return response.text  # Return the result
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Error connecting to eXistDB: {e}")
        return None


# Available XQuery queries
queries = {
    "1": {
        "description": "List of herbivorous animals",
        "query": """
for $animal in //animal[diet = 'Herbivore']
let $zoo := //zoo[@id = $animal/@zooid]
return
    <animal>
        <name>{string($animal/name)}</name>
        <habitat>{string($animal/habitat)}</habitat>
        <zoo>{string($zoo/name)}</zoo>
    </animal>
"""
    },
    "2": {
        "description": "List of zoos",
        "query": """
for $zoo in //zoo
return
    <zoo>
        <name>{string($zoo/name)}</name>
        <city>{string($zoo/city)}</city>
        <location>{string($zoo/@location)}</location>
    </zoo>
"""
    },
    "3": {
        "description": "Animals at risk of extinction",
        "query": """
for $stat in //conservation_statistic[status = 'Endangered' or status = 'Vulnerable']
let $animal := //animal[@id = $stat/@animalid]
return
    <animal>
        <name>{string($animal/name)}</name>
        <status>{string($stat/status)}</status>
        <population_in_wild>{string($stat/population_in_wild)}</population_in_wild>
    </animal>
"""
    },
    "4": {
        "description": "Count of animals per zoo",
        "query": """
for $zoo in //zoo
let $animalCount := count(//animal[@zooid = $zoo/@id])
return
    <zoo>
        <name>{string($zoo/name)}</name>
        <animal_count>{$animalCount}</animal_count>
    </zoo>
"""
    },
    "5": {
        "description": "Animals living in specific habitats (e.g., Savanna)",
        "query": """
for $animal in //animal[habitat = 'Savanna']
let $zoo := //zoo[@id = $animal/@zooid]
return
    <animal>
        <name>{string($animal/name)}</name>
        <habitat>{string($animal/habitat)}</habitat>
        <zoo>{string($zoo/name)}</zoo>
    </animal>
"""
    }
}


# Menu to select a query
def main():
    print("Select a query to execute:")
    for key, value in queries.items():
        print(f"{key}. {value['description']}")

    choice = input("Enter the query number: ")
    if choice in queries:
        print(f"Executing: {queries[choice]['description']}")
        result = execute_xquery(queries[choice]["query"])
        if result:
            print("Query result:")
            print(result)
    else:
        print("Invalid option.")


# Execute the script
if __name__ == "__main__":
    main()
