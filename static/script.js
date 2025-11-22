// Tourism AI - Frontend Script
const API_URL = window.location.origin || 'http://localhost:8000';

function fillExample(text) {
    const input = document.getElementById('queryInput');
    if (input) {
        input.value = text;
    }
}

async function search() {
    const query = document.getElementById('queryInput').value.trim();
    if (!query) {
        alert('Please enter a query');
        return;
    }

    const btn = document.getElementById('searchBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    const results = document.getElementById('results');
    
    // Show loading state
    btn.disabled = true;
    btnText.classList.add('hidden');
    btnLoader.classList.remove('hidden');
    results.classList.add('hidden');
    
    // Hide previous results
    document.getElementById('errorBox').classList.add('hidden');
    document.getElementById('weatherCard').classList.add('hidden');
    document.getElementById('placesCard').classList.add('hidden');

    try {
        const response = await fetch(`${API_URL}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();
        results.classList.remove('hidden');

        if (data.error) {
            showError(data.message || 'An error occurred');
        } else {
            displayResults(data);
        }
    } catch (error) {
        results.classList.remove('hidden');
        showError('Failed to connect to the API. Make sure the server is running on ' + API_URL);
        console.error('Error:', error);
    } finally {
        // Hide loading state
        btn.disabled = false;
        btnText.classList.remove('hidden');
        btnLoader.classList.add('hidden');
    }
}

function showError(message) {
    const errorBox = document.getElementById('errorBox');
    errorBox.textContent = message;
    errorBox.classList.remove('hidden');
}

function displayResults(data) {
    // Display weather
    if (data.weather) {
        const weatherCard = document.getElementById('weatherCard');
        document.getElementById('temperature').textContent = Math.round(data.weather.temperature);
        document.getElementById('rainProb').textContent = Math.round(data.weather.rain_probability);
        weatherCard.classList.remove('hidden');
    }

    // Display places
    if (data.places && data.places.length > 0) {
        const placesCard = document.getElementById('placesCard');
        const placesList = document.getElementById('placesList');
        placesList.innerHTML = '';
        
        data.places.forEach(place => {
            const li = document.createElement('li');
            li.textContent = place.name;
            placesList.appendChild(li);
        });
        
        placesCard.classList.remove('hidden');
    } else if (!data.weather && !data.places) {
        // If no weather and no places, show error
        showError(data.message || 'No results found');
    }
}

// Allow Enter key to trigger search
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('queryInput');
    if (input) {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                search();
            }
        });
    }
    
    // Check if API is accessible
    fetch(`${API_URL}/health`)
        .then(response => response.json())
        .then(data => {
            console.log('API is accessible:', data);
        })
        .catch(error => {
            console.error('API connection error:', error);
        });
});

