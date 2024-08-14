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


let packages = [
    ['195 West Oakland Ave', '10:30 AM', 'Salt Lake City', '84115', '21', ['at the hub', ''], [40.716805758613766, -111.89531934157908], 'UT', ''],
    ['2530 S 500 E', 'EOD', 'Salt Lake City', '84106', '44', ['at the hub', ''], [40.7155193, -111.8774493], 'UT', ''],
    ['231 North Canyon Rd', 'EOD', 'Salt Lake City', '84103', '2', ['at the hub', ''], [40.77477275, -111.8859662], 'UT', 'Can only be on truck 2'],
    ['380 W 2880 S', 'EOD', 'Salt Lake City', '84115', '4', ['at the hub', ''], [40.7090191, -111.90193302315416], 'UT', ''],
    ['450 S State St', 'EOD', 'Salt Lake City', '84111', '5', ['at the hub', ''], [40.75956505, -111.88909256720231], 'UT', ''],
    ['3060 Lester St', '10:30 AM', 'West Valley City', '84119', '88', ['at the hub', ''], [40.70554249041934, -111.93634152444814], 'UT', 'Delayed on flight---will not arrive to depot until 9:05 am'],
    ['1330 2100 S', 'EOD', 'Salt Lake City', '84106', '8', ['at the hub', ''], [40.725437547437885, -111.84380349915963], 'UT', ''],
    ['300 State St', 'EOD', 'Salt Lake City', '84103', '9', ['at the hub', ''], [40.77554485, -111.8877297], 'UT', ''],
    ['300 State St', 'EOD', 'Salt Lake City', '84103', '2', ['at the hub', ''], [40.77554485, -111.8877297], 'UT', 'Wrong address listed, cannot have correct address (450 S State St, Salt Lake City, UT 84111) until 10:20 a.m'],
    ['600 E 900 South', 'EOD', 'Salt Lake City', '84105', '1', ['at the hub', ''], [40.74984, -111.909955], 'UT', ''],
    ['2600 Taylorsville Blvd', 'EOD', 'Salt Lake City', '84118', '1', ['at the hub', ''], [40.654619249999996, -111.955456775], 'UT', ''],
    ['West Valley Central Station', 'EOD', 'West Valley City', '84119', '1', ['at the hub', ''], [40.6933219, -111.9606171], 'UT', ''],
    ['2010 W 500 S', '10:30 AM', 'Salt Lake City', '84104', '2', ['at the hub', ''], [40.75851355431876, -111.94768934779822], 'UT', ''],
    ['4300 S 1300 E', '10:30 AM', 'Millcreek', '84117', '88', ['at the hub', ''], [40.676338, -111.85421], 'UT', 'Must be delivered with 15, 19'],
    ['4580 S 2300 E', '9:00 AM', 'Holladay', '84117', '4', ['at the hub', ''], [40.671442125, -111.8246463125], 'UT', ''],
    ['4580 S 2300 E', '10:30 AM', 'Holladay', '84117', '88', ['at the hub', ''], [40.671442125, -111.8246463125], 'UT', 'Must be delivered with 13, 19'],
    ['3148 S 1100 W', 'EOD', 'Salt Lake City', '84119', '2', ['at the hub', ''], [40.702959, -111.92551170210548], 'UT', ''],
    ['1488 4800 S', 'EOD', 'Salt Lake City', '84123', '6', ['at the hub', ''], [40.66421465374496, -111.93332964058986], 'UT', 'Can only be on truck 2'],
    ['177 W Price Ave', 'EOD', 'Salt Lake City', '84115', '37', ['at the hub', ''], [40.6918197, -111.8958107], 'UT', ''],
    ['3595 Main St', '10:30 AM', 'Salt Lake City', '84115', '37', ['at the hub', ''], [40.693347499753145, -111.8910192084904], 'UT', 'Must be delivered with 13, 15'],
    ['3595 Main St', 'EOD', 'Salt Lake City', '84115', '3', ['at the hub', ''], [40.693347499753145, -111.8910192084904], 'UT', ''],
    ['6351 South 900 East', 'EOD', 'Murray', '84121', '2', ['at the hub', ''], [40.6351415, -111.8640934], 'UT', ''],
    ['5100 South 2700 West', 'EOD', 'Salt Lake City', '84118', '5', ['at the hub', ''], [40.65905080929819, -111.9580028631501], 'UT', ''],
    ['5025 State St', 'EOD', 'Murray', '84107', '7', ['at the hub', ''], [40.66252675, -111.88752926034994], 'UT', ''],
    ['5383 South 900 East', '10:30 AM', 'Salt Lake City', '84117', '7', ['at the hub', ''], [40.65408634735715, -111.86581630694714], 'UT', 'Delayed on flight---will not arrive to depot until 9:05 am'],
    ['5383 South 900 East', 'EOD', 'Salt Lake City', '84117', '25', ['at the hub', ''], [40.65408634735715, -111.86581630694714], 'UT', ''],
    ['1160 Dalton Ave', 'EOD', 'Salt Lake City', '84104', '5', ['at the hub', ''], [40.74600233728327, -111.92372726468476], 'UT', ''],
    ['2835 Main St', 'EOD', 'Salt Lake City', '84115', '7', ['at the hub', ''], [40.7096065, -111.89082078488806], 'UT', 'Delayed on flight---will not arrive to depot until 9:05 am'],
    ['1330 2100 S', '10:30 AM', 'Salt Lake City', '84106', '2', ['at the hub', ''], [40.725437547437885, -111.84380349915963], 'UT', ''],
    ['300 State St', '10:30 AM', 'Salt Lake City', '84103', '1', ['at the hub', ''], [40.77554485, -111.8877297], 'UT', ''],
    ['3365 S 900 W', '10:30 AM', 'Salt Lake City', '84119', '1', ['at the hub', ''], [40.6986231, -111.91635], 'UT', ''],
    ['3365 S 900 W', 'EOD', 'Salt Lake City', '84119', '1', ['at the hub', ''], [40.6986231, -111.91635], 'UT', 'Delayed on flight---will not arrive to depot until 9:05 am'],
    ['2530 S 500 E', 'EOD', 'Salt Lake City', '84106', '1', ['at the hub', ''], [40.7155193, -111.8774493], 'UT', ''],
    ['4580 S 2300 E', '10:30 AM', 'Holladay', '84117', '2', ['at the hub', ''], [40.671442125, -111.8246463125], 'UT', ''],
    ['1160 Dalton Ave', 'EOD', 'Salt Lake City', '84104', '88', ['at the hub', ''], [40.74600233728327, -111.92372726468476], 'UT', ''],
    ['2300 Parkway Blvd', 'EOD', 'West Valley City', '84119', '88', ['at the hub', ''], [40.712313, -111.954034], 'UT', 'Can only be on truck 2'],
    ['450 S State St', '10:30 AM', 'Salt Lake City', '84111', '2', ['at the hub', ''], [40.75956505, -111.88909256720231], 'UT', ''],
    ['450 S State St', 'EOD', 'Salt Lake City', '84111', '9', ['at the hub', ''], [40.75956505, -111.88909256720231], 'UT', 'Can only be on truck 2'],
    ['2010 W 500 S', 'EOD', 'Salt Lake City', '84104', '9', ['at the hub', ''], [40.75851355431876, -111.94768934779822], 'UT', ''],
    ['380 W 2880 S', '10:30 AM', 'Salt Lake City', '84115', '45', ['at the hub', ''], [40.7090191, -111.90193302315416], 'UT', '']
]

const table = document.getElementById('tbody')

let i = 0
for (let eachPackage of packages){
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

    i ++
} 

