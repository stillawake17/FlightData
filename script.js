let flightData = {};  // Initialize as an empty object

// Use Fetch API to load the JSON data
fetch('combined_flights_data.json')
    .then(response => response.json())
    .then(data => {
        flightData = data[0];  // Assuming you want the first flight data entry
        initialize();  // Call a function to proceed with your logic after loading data
    })
    .catch(error => console.error('Error fetching the JSON:', error));

function unixToHumanReadable(unixTimestamp) {
    const date = new Date(unixTimestamp * 1000); // Convert to milliseconds
    return date.toLocaleString(); // Convert to local date and time
}

function initialize() {
    // Populate the HTML elements with data
    document.getElementById('icao24').textContent = flightData.icao24;
    document.getElementById('firstSeen').textContent = unixToHumanReadable(flightData.firstSeen);
    document.getElementById('estDepartureAirport').textContent = flightData.estDepartureAirport;
    document.getElementById('lastSeen').textContent = unixToHumanReadable(flightData.lastSeen);
    document.getElementById('estArrivalAirport').textContent = flightData.estArrivalAirport;
    document.getElementById('callsign').textContent = flightData.callsign.trim();

    const processedData = processOpenSkyData(flightData);
    console.log(processedData);
}

function processOpenSkyData(flightData) {
    const LandedDate = unixToHumanReadable(flightData.lastSeen).split(',')[0];  // Splitting the date from date-time string
    const LandedTime = unixToHumanReadable(flightData.lastSeen).split(',')[1].trim();
    const FLIGHT = flightData.callsign.trim();
    const FROM = flightData.estDepartureAirport;  // This is ICAO code, not full name
    // AIRLINE and AIRCRAFT would need additional sources or logic to determine
    const AIRLINE = "Unknown";  // Placeholder
    const AIRCRAFT = "Unknown";  // Placeholder
    const STATUS = "Landed " + LandedTime;  // Simple status logic

    return {
        LandedDate,
        LandedTime,
        FLIGHT,
        FROM,
        AIRLINE,
        AIRCRAFT,
        STATUS
    };
}
