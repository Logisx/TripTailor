document.getElementById('startDate').addEventListener('change', validateDates);
document.getElementById('endDate').addEventListener('change', validateDates);

function validateDates() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const nextButton = document.getElementById('nextButton');
    
    if (startDate && endDate && new Date(startDate) > new Date(endDate)) {
        alert("Start date cannot be later than the end date.");
        document.getElementById('endDate').setCustomValidity("End date must be later than start date.");
        nextButton.disabled = true; // Disable the button if the dates are invalid
    } else {
        document.getElementById('endDate').setCustomValidity(""); // Reset custom validity
        nextButton.disabled = false; // Enable the button if the dates are valid
    }
}


function updatePeopleCount(change) {
    const peopleInput = document.getElementById('people');
    let currentValue = parseInt(peopleInput.value);

    // Prevent the value from going below 1
    if (currentValue + change >= 1) {
        peopleInput.value = currentValue + change;
    }
}


// Handle vibe selection (single selection)
const vibeTiles = document.querySelectorAll('.vibe-tile');
const vibeInput = document.getElementById('vibe');

vibeTiles.forEach(tile => {
    tile.addEventListener('click', () => {
        // Remove selected class from all vibe tiles
        vibeTiles.forEach(t => t.classList.remove('selected'));
        
        // Add selected class to the clicked tile
        tile.classList.add('selected');
        
        // Set the hidden input value to the selected tile's data-value
        vibeInput.value = tile.getAttribute('data-value');
    });
});

// Handle interests selection (multiple selections)
const interestTiles = document.querySelectorAll('.interest-tile');
const interestsInput = document.getElementById('interests');

interestTiles.forEach(tile => {
    tile.addEventListener('click', () => {
        // Toggle the selected state of the tile
        tile.classList.toggle('selected');
        
        // Gather all selected values
        const selectedValues = Array.from(interestTiles)
            .filter(t => t.classList.contains('selected'))
            .map(t => t.getAttribute('data-value'));
        
        // Update the hidden input field with selected values (comma-separated)
        interestsInput.value = selectedValues.join(',');
    });
});





let currentStep = 1;
function nextStep(step) {
    document.getElementById(`step${currentStep}`).classList.remove('active');
    currentStep = step;
    document.getElementById(`step${currentStep}`).classList.add('active');
    updateProgressBar();
}

function updateProgressBar() {
    const progress = (currentStep - 1) * 25;
    document.getElementById('progressBar').style.width = `${progress}%`;
    document.getElementById('progressBar').setAttribute('aria-valuenow', progress);
}

function submitForm() {
    const userData = {
        tripDescription: document.getElementById('tripDescription')?.value || '',
        budget: document.getElementById('budget')?.value || '',
        startDate: document.getElementById('startDate')?.value || '',
        endDate: document.getElementById('endDate')?.value || '',
        people: document.getElementById('people')?.value || '',
        vibe: document.getElementById('vibe')?.value || '',
        interests: document.getElementById('interests')?.value || '' // Ensure it's populated
    };

    // Show the loading overlay
    document.getElementById('loadingOverlay').style.display = 'flex';

    // Start the text switching effect
    const loadingMessages = [
        "Analysing your preferences...",
        "Finding the best destinations for you...",
        "Optimizing your travel plan...",
        "Searching for pictures to show...",
        "Generating Itinerary...",
        "Almost there...",
        "May take up to a minute..."
    ];

    let currentMessageIndex = 0;
    const loadingTextElement = document.getElementById('loadingText');

    const switchText = () => {
        setTimeout(() => {
            loadingTextElement.innerHTML = `<p>${loadingMessages[currentMessageIndex]}</p>`;
            currentMessageIndex = (currentMessageIndex + 1) % loadingMessages.length;
        }, 5000); 
    };

    // Change the message every 2 seconds
    const textSwitchInterval = setInterval(switchText, 2000);

    fetch('/itinerary/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Generated Itinerary:', data);
        window.location.href = '/itinerary';
    })
    .catch(error => {
        console.error('Error generating itinerary:', error);
    })
    .finally(() => {
        // Clear the text switch interval and hide the loading overlay once done
        clearInterval(textSwitchInterval);
        document.getElementById('loadingOverlay').style.display = 'none';
    });
}