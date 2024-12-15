// Function to save form data and current step
function saveForm() {
    const formData = {
        tripDescription: document.getElementById('tripDescription').value || '',
        budget: document.getElementById('budget').value || '',
        startDate: document.getElementById('startDate').value || '',
        endDate: document.getElementById('endDate').value || '',
        people: document.getElementById('people').value || '',
        vibe: document.getElementById('vibe').value || '',
        interests: document.getElementById('interests').value || '',
        currentStep: currentStep 
    };

    // Save the data to localStorage
    localStorage.setItem('tripData', JSON.stringify(formData));
}

// Function to restore form data from localStorage
function restoreForm() {
    const savedData = JSON.parse(localStorage.getItem('tripData'));

    if (savedData) {
        document.getElementById('tripDescription').value = savedData.tripDescription || '';
        document.getElementById('budget').value = savedData.budget || '';
        document.getElementById('startDate').value = savedData.startDate || '';
        document.getElementById('endDate').value = savedData.endDate || '';
        document.getElementById('people').value = savedData.people || 2; 
        document.getElementById('vibe').value = savedData.vibe || '';
        document.getElementById('interests').value = savedData.interests || '';

        document.querySelectorAll('.vibe-tile').forEach(tile => {
            if (tile.getAttribute('data-value') === savedData.vibe) {
                tile.classList.add('selected');
            } else {
                tile.classList.remove('selected');
            }
        });

        document.querySelectorAll('.interest-tile').forEach(tile => {
            const interestValues = savedData.interests ? savedData.interests.split(',') : [];
            if (interestValues.includes(tile.getAttribute('data-value'))) {
                tile.classList.add('selected');
            } else {
                tile.classList.remove('selected');
            }
        });
    }
}

// Function to add event listeners to all form fields
function addEventListeners() {
    
    document.getElementById('tripDescription').addEventListener('input', saveForm);
    document.getElementById('budget').addEventListener('input', saveForm);
    document.getElementById('people').addEventListener('input', saveForm);
    document.getElementById('startDate').addEventListener('change', saveForm);
    document.getElementById('endDate').addEventListener('change', saveForm);

    document.querySelectorAll('.vibe-tile').forEach(tile => {
        tile.addEventListener('click', saveForm);
    });

    document.querySelectorAll('.interest-tile').forEach(tile => {
        tile.addEventListener('click', saveForm);
    });
}

// Function to initialize the form (when the page is loaded)
document.addEventListener('DOMContentLoaded', function () {
    addEventListeners();

    const savedData = JSON.parse(localStorage.getItem('tripData'));
    
    if (savedData) {
        document.getElementById('tripDescription').value = savedData.tripDescription;
        document.getElementById('budget').value = savedData.budget;
        document.getElementById('people').value = savedData.people;
        document.getElementById('startDate').value = savedData.startDate;
        document.getElementById('endDate').value = savedData.endDate;
        document.getElementById('vibe').value = savedData.vibe;
        document.getElementById('interests').value = savedData.interests;

        currentStep = savedData.currentStep || 1; 

        const allSteps = document.querySelectorAll('.step');
        allSteps.forEach(step => step.classList.remove('active'));

        document.getElementById(`step${currentStep}`).classList.add('active');
        updateProgressBar();
    }
});



document.getElementById('startDate').addEventListener('change', validateDates);
document.getElementById('endDate').addEventListener('change', validateDates);

function validateDates() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const nextButton = document.getElementById('nextButton');
    
    if (startDate && endDate && new Date(startDate) > new Date(endDate)) {
        alert("Start date cannot be later than the end date.");
        document.getElementById('endDate').setCustomValidity("End date must be later than start date.");
        nextButton.disabled = true; 
    } else {
        document.getElementById('endDate').setCustomValidity(""); 
        nextButton.disabled = false;
    }
}


function updatePeopleCount(change) {
    const peopleInput = document.getElementById('people');
    let currentValue = parseInt(peopleInput.value);

    if (currentValue + change >= 1) {
        peopleInput.value = currentValue + change;
    }
}


// Handle vibe selection (single selection)
const vibeTiles = document.querySelectorAll('.vibe-tile');
const vibeInput = document.getElementById('vibe');

vibeTiles.forEach(tile => {
    tile.addEventListener('click', () => {
        vibeTiles.forEach(t => t.classList.remove('selected'));
        
        tile.classList.add('selected');
        
        vibeInput.value = tile.getAttribute('data-value');
    });
});

// Handle interests selection (multiple selections)
const interestTiles = document.querySelectorAll('.interest-tile');
const interestsInput = document.getElementById('interests');

interestTiles.forEach(tile => {
    tile.addEventListener('click', () => {
        tile.classList.toggle('selected');
        
        const selectedValues = Array.from(interestTiles)
            .filter(t => t.classList.contains('selected'))
            .map(t => t.getAttribute('data-value'));
        
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
        interests: document.getElementById('interests')?.value || ''
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
        }, 4000); 
    };

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
        clearInterval(textSwitchInterval);
        document.getElementById('loadingOverlay').style.display = 'none';
    });
}