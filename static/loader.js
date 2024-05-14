
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
