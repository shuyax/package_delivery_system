import "./style.css"

const map = L.map('mapid').setView([39.8283, -98.5795], 4);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Leaflet supports multiple layers, allowing you to overlay various datasets on the map (e.g., multiple tile layers, markers, geoJSON data).
// Layer Groups: Organize multiple markers or shapes into a single layer group.
// Layer Control: A built-in control to switch between different layers.
// const baseLayers = { "Map": osmLayer };
// const overlays = { "Cities": citiesLayer };
// L.control.layers(baseLayers, overlays).addTo(map);

function addMarkerOnMap([latitude, longitude],address, city, state, zipcode) {
    L.marker([latitude, longitude]).addTo(map)
        .bindPopup(`${address} <br> ${city}, ${state}, ${zipcode}`)
        .openPopup();
}

function displayPackagesInTable(packages) {
    const table = document.getElementById('tbody')
    let i = 0
    for (let eachPackage of packages){
        if (eachPackage != null) {
            addMarkerOnMap(eachPackage[6],eachPackage[0],eachPackage[2],eachPackage[7],eachPackage[3])
            const tableRow = document.createElement('tr')
            table.appendChild(tableRow)

            const packageId = document.createElement('td')
            packageId.textContent = i
            tableRow.appendChild(packageId)

            const address = document.createElement('td')
            address.textContent = eachPackage[0]
            tableRow.appendChild(address)

            const city = document.createElement('td')
            city.textContent = eachPackage[2]
            tableRow.appendChild(city)

            const state = document.createElement('td')
            state.textContent = eachPackage[7]
            tableRow.appendChild(state)

            const zipcode = document.createElement('td')
            zipcode.textContent = eachPackage[3]
            tableRow.appendChild(zipcode)

            const deadline = document.createElement('td')
            deadline.textContent = eachPackage[1]
            tableRow.appendChild(deadline)

            const weight = document.createElement('td')
            weight.textContent = eachPackage[4]
            tableRow.appendChild(weight)

            const note = document.createElement('td')
            note.textContent = eachPackage[8]
            tableRow.appendChild(note)
        }
        
        i ++
    } 
}

fetch('http://192.168.1.163:5000/package-delivery-system/api/data')
    .then(response => response.json())
    .then(data => displayPackagesInTable(data))
    .catch(error => console.error('Error: ', error))

fetch('http://192.168.1.163:5000/package-delivery-system/api/get-settings')
    .then(response => response.json())
    .then(data => {
      console.log('Current Settings:', data);
      // Display data in the front-end, e.g., in input fields
      document.getElementById('total-packages-per-truck').value = data.total_packages_per_truck;
      document.getElementById('truck-speed').value = data.truck_speed;
      document.getElementById('truck1-start-time').value = data.truck1_start_time;
      document.getElementById('truck2-start-time').value = data.truck2_start_time;
    });


function updateTruckSettings() {
    const updatedData = {
        "total_packages_per_truck": document.getElementById('total-packages-per-truck').value,
        "truck_speed": document.getElementById('truck-speed').value,
        "truck1_start_time": document.getElementById('truck1-start-time').value,
        "truck2_start_time": document.getElementById('truck2-start-time').value
    }

    const urlEncodedData = new URLSearchParams(updatedData).toString();

    fetch('http://192.168.1.163:5000/package-delivery-system/api/update-settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: urlEncodedData
    })
        .then(response => response.json())
        .then(data => {
            console.log('Updated Settings:', data);
            // Optionally, update the UI with the new settings
        })
}
document.getElementById('calculate').addEventListener('click',updateTruckSettings)