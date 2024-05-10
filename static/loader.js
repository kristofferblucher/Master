
document.addEventListener("DOMContentLoaded", function() {
    window.addEventListener('beforeunload', function () {
        document.getElementById('loading').style.display = 'block';
    });
});

window.onload = function() {
    document.getElementById('loading').style.display = 'none';
};

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })

  