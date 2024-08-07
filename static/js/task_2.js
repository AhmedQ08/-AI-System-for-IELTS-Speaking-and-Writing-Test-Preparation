var timeLimitInMinutes = 1;
var timeLimitInSeconds = timeLimitInMinutes * 60;
var timerElement = document.getElementById('timer');

// Function to start the timer and hide the modal
function startTimer() {
    var startTime = Date.now();
    var interval = 1000; // Initial interval of 1000 milliseconds (1 second)

    var timerInterval = setInterval(function() {
        var elapsedTime = Date.now() - startTime; // Time elapsed since starting the timer
        var remainingTime = (timeLimitInMinutes * 60 * 1000) - elapsedTime; // Time remaining in milliseconds

        if (remainingTime <= 0) {
            clearInterval(timerInterval);
            timerElement.textContent = '00:00';
            showLoader();
            document.getElementById('taskForm').submit();
            return;
        }

        var minutes = Math.floor((remainingTime / 1000) / 60);
        var seconds = Math.floor((remainingTime / 1000) % 60);

        if (minutes < 10) {
            minutes = '0' + minutes;
        }
        if (seconds < 10) {
            seconds = '0' + seconds;
        }

        timerElement.textContent = minutes + ':' + seconds;
    }, interval);

    // Hide the modal after starting the timer
    var modalElement = document.getElementById('containerModal');
    var modalInstance = bootstrap.Modal.getInstance(modalElement);
    modalInstance.hide();
}

// Function to show loader
function showLoader() {
    document.querySelector('.outer_container').classList.add('blur');
    document.getElementById('loader').classList.remove('hidden');
    document.getElementById('overlay').classList.remove('hidden');
}

// Function to show the container div as a modal on page load
function showInstructionsModal() {
    var containerModal = new bootstrap.Modal(document.getElementById('containerModal'), {
        keyboard: false,
        backdrop: 'static'
    });
    containerModal.show();
}

// Event listener to start the timer after the user closes the container modal
document.getElementById('containerModal').addEventListener('hidden.bs.modal', function () {
    startTimer();
});

// Call function to show instructions modal on page load
window.onload = showInstructionsModal;
