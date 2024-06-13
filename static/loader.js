
document.addEventListener("DOMContentLoaded", function() {
    // Ta vekk loading screen når alt er lastet
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


//Funskjon for bytting av språkversjon sekvens
function toggleLanguage() {
    var en = document.getElementById('sentence-container_en');
    var no = document.getElementById('sentence-container_no');
    var button = document.getElementById('button-vis-engelsk')

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
    