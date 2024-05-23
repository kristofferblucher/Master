
document.addEventListener("DOMContentLoaded", function() {
    // Hide the loading screen once the page is fully loaded
    window.onload = function() {
        document.getElementById('loading').style.display = 'none';
    };

    // Optional: Explicitly show the loading screen when starting to navigate away
    window.onbeforeunload = function() {
        document.getElementById('loading').style.display = 'block';
    };
});

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })

  document.getElementById('goBack').addEventListener('click', function() {
    window.location.href = this.getAttribute('data-url');
});

//Funksjon for bytting av engelsk og norsk versjon

// Global storage for checkbox states
// Global storage for checkbox states
// Global storage for checkbox states
var checkboxStates = {
    'sentence-container_no': {},
    'sentence-container_en': {}
};

function storeCheckboxStates(containerId) {
    var checkboxes = document.getElementById(containerId).getElementsByClassName('sentence-checkbox');
    var stateObj = checkboxStates[containerId];
    Array.from(checkboxes).forEach(function(checkbox, index) {
        stateObj[index] = checkbox.checked;
    });
}

function restoreCheckboxStates(containerId, defaultState = false) {
    var checkboxes = document.getElementById(containerId).getElementsByClassName('sentence-checkbox');
    var stateObj = checkboxStates[containerId];
    Array.from(checkboxes).forEach(function(checkbox, index) {
        if (containerId === 'sentence-container_en' && stateObj[index] === undefined) {
            checkbox.checked = defaultState;
        } else {
            checkbox.checked = stateObj[index] !== undefined ? stateObj[index] : defaultState;
        }
    });
}

function toggleLanguage() {
    var en = document.getElementById('sentence-container_en');
    var no = document.getElementById('sentence-container_no');
    var button = document.getElementById('button-vis-engelsk');

    if (en.style.display === "none") {
        storeCheckboxStates('sentence-container_no'); // Store state before toggling
        en.style.display = "block";
        no.style.display = "none";
        button.textContent = "Vis norsk versjon";
        restoreCheckboxStates('sentence-container_en', false); // Restore state and default to unchecked if undefined
    } else {
        storeCheckboxStates('sentence-container_en'); // Store state before toggling
        en.style.display = "none";
        no.style.display = "block";
        button.textContent = "Vis engelsk versjon";
        restoreCheckboxStates('sentence-container_no', true); // Restore state and default to checked if undefined
    }
}

// Ensure Norwegian sentences are checked by default on initial load
document.addEventListener("DOMContentLoaded", function() {
    restoreCheckboxStates('sentence-container_no', true);
});





//Funskjon for bytting av språkversjon bakgrunnsinfo
function toggleLanguageInfo() {
    var en = document.getElementById('article-en');
    var no = document.getElementById('article-no');
    var button = document.getElementById('button-vis-engelsk-info')

    if (en.style.display === "none") {
        en.style.display = "block";
        no.style.display = "none";
        button.textContent = "Vis norsk versjon";
    } else {
        en.style.display = "none";
        no.style.display = "block";
        button.textContent = "Vis engelsk versjon";
    }
}
    