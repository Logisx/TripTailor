let map;
const markers = [];
const itineraryData = [
    {% for day in daily_itineraries %}
        [
            {% for activity_group in day.activities %}
                {% for activity in activity_group.main_activity %}
                    { lat: {{ activity.geolocation.lat }}, lng: {{ activity.geolocation.lng }}, name: "{{ activity.name }}" },
                {% endfor %}
            {% endfor %}
        ],
    {% endfor %}
];

function initializeMap() {
    map = L.map('map').setView([41.8902, 12.4922], 10); // Default location
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);
    showMarkers(0); // Show Day 1 markers initially
}

function showMarkers(dayIndex) {
    // Remove old markers
    markers.forEach(marker => map.removeLayer(marker));
    markers.length = 0;

    const bounds = [];
    itineraryData[dayIndex].forEach(activity => {
        const marker = L.marker([activity.lat, activity.lng])
            .addTo(map)
            .bindPopup(activity.name);
        markers.push(marker);
        bounds.push([activity.lat, activity.lng]);
    });

    // Adjust the map to fit the new markers
    if (bounds.length > 0) {
        map.fitBounds(bounds, { padding: [50, 50] });
    }
}

function showDay(dayIndex) {
    // Update visible tiles
    document.querySelectorAll('.itinerary-day').forEach((day, index) => {
        day.style.display = index === dayIndex ? 'block' : 'none';
    });

    // Update active tab
    document.querySelectorAll('.day-tab').forEach(tab => tab.classList.remove('active'));
    document.getElementById(`day-tab-${dayIndex}`).classList.add('active');

    // Update map markers and region
    showMarkers(dayIndex);
}

function downloadPDF() {
    alert("Download PDF feature is in development.");
}

document.addEventListener('DOMContentLoaded', initializeMap);