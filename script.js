// Sample data
const flightData = {
    "icao24": "400f02",
    "firstSeen": 1691704050,
    "estDepartureAirport": "EGPH",
    "lastSeen": 1691707577,
    "estArrivalAirport": "EGGD",
    "callsign": "EZY42AB ",
    // ... other fields ...
};

function unixToHumanReadable(unixTimestamp) {
    const date = new Date(unixTimestamp * 1000); // Convert to milliseconds
    return date.toLocaleString(); // Convert to local date and time
}

// Populate the HTML elements with data
document.getElementById('icao24').textContent = flightData.icao24;
document.getElementById('firstSeen').textContent = unixToHumanReadable(flightData.firstSeen);
document.getElementById('estDepartureAirport').textContent = flightData.estDepartureAirport;
document.getElementById('lastSeen').textContent = unixToHumanReadable(flightData.lastSeen);
document.getElementById('estArrivalAirport').textContent = flightData.estArrivalAirport;
document.getElementById('callsign').textContent = flightData.callsign.trim();

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

const processedData = processOpenSkyData(sampleFlightData);
console.log(processedData);

