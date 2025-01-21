const API_URL = "http://127.0.0.1:5000";

// Fetch Zoos
function getZoos() {
    fetch(`${API_URL}/zoos`)
        .then(response => response.json())
        .then(data => {
            const zoosList = document.getElementById('zoos-list');
            zoosList.innerHTML = data.map(zoo =>
                `<tr>
                    <td>${zoo.id}</td>
                    <td>${zoo.name}</td>
                    <td>${zoo.city}</td>
                    <td>${zoo.foundation}</td>
                    <td>${zoo.location}</td>
                </tr>`
            ).join('');
        });
}

function addZoo(event) {
    event.preventDefault();
    const name = document.getElementById('zoo-name').value;
    const city = document.getElementById('zoo-city').value;
    const foundation = document.getElementById('zoo-foundation').value;
    const location = document.getElementById('zoo-location').value;

    fetch(`${API_URL}/zoos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, city, foundation, location }) // No se envía el ID aquí
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.error); });
            }
            return response.json();
        })
        .then(() => {
            getZoos(); // Recargar la lista
            alert("Zoo added successfully");
            document.getElementById('add-zoo-form').reset();
        })
        .catch(err => alert("Error: " + err.message));
}

// Fetch Animals
function getAnimals() {
    fetch(`${API_URL}/animals`)
        .then(response => response.json())
        .then(data => {
            const animalsList = document.getElementById('animals-list');
            animalsList.innerHTML = data.map(animal =>
                `<tr>
                    <td>${animal.id}</td>
                    <td>${animal.name}</td>
                    <td>${animal.species}</td>
                    <td>${animal.zooid}</td>
                    <td>${animal.habitat}</td>
                    <td>${animal.diet}</td>
                </tr>`
            ).join('');
        });
}

// Add Animal
function addAnimal(event) {
    event.preventDefault();
    const name = document.getElementById('animal-name').value;
    const species = document.getElementById('animal-species').value;
    const zooid = document.getElementById('animal-zooid').value;
    const habitat = document.getElementById('animal-habitat').value;
    const diet = document.getElementById('animal-diet').value;
    const scientific_name = document.getElementById('animal-scientific-name').value;

    fetch(`${API_URL}/animals`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, species, zooid, habitat, diet, scientific_name })
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.error); });
            }
            return response.json();
        })
        .then(() => {
            getAnimals(); // Recargar la lista
            alert("Animal added successfully");
            document.getElementById('add-animal-form').reset();
        })
        .catch(err => alert("Error: " + err.message));
}



// Fetch Conservation Statistics
function getConservationStats() {
    fetch(`${API_URL}/conservation-stats`)
        .then(response => response.json())
        .then(data => {
            const statsList = document.getElementById('stats-list');
            statsList.innerHTML = data.map(stat =>
                `<tr>
                    <td>${stat.animalid}</td>
                    <td>${stat.year}</td>
                    <td>${stat.population_in_wild}</td>
                    <td>${stat.population_in_captivity}</td>
                    <td>${stat.status}</td>
                </tr>`
            ).join('');
        });
}

// Add Conservation Stat
function addConservationStat(event) {
    event.preventDefault();
    const animalid = document.getElementById('stat-animalid').value;
    const year = document.getElementById('stat-year').value;
    const population_in_wild = document.getElementById('stat-population-wild').value;
    const population_in_captivity = document.getElementById('stat-population-captivity').value;
    const status = document.getElementById('stat-status').value;

    fetch(`${API_URL}/conservation-stats`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ animalid, year, population_in_wild, population_in_captivity, status })
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.error); });
            }
            return response.json();
        })
        .then(() => {
            getConservationStats(); // Recargar la lista
            alert("Conservation statistic added successfully");
            document.getElementById('add-stat-form').reset();
        })
        .catch(err => alert("Error: " + err.message));
}


// Initialize Event Listeners
function initialize() {
    document.getElementById('add-zoo-form').addEventListener('submit', addZoo);
    document.getElementById('add-animal-form').addEventListener('submit', addAnimal);
    document.getElementById('add-stat-form').addEventListener('submit', addConservationStat);

    // Load initial data
    getZoos();
    getAnimals();
    getConservationStats();
}

// Run initialize on page load
window.onload = initialize;
