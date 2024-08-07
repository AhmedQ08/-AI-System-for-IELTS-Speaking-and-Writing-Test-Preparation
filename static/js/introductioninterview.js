var timerElement = document.getElementById('timer');

function startTimer() {
    var timeLimitInMinutes = 1;
    var startTime = Date.now();
    var interval = 1000; // Interval of 1000 milliseconds (1 second)

    var timerInterval = setInterval(function() {
        var elapsedTime = Date.now() - startTime; // Time elapsed since starting the timer
        var remainingTime = (timeLimitInMinutes * 60 * 1000) - elapsedTime; // Remaining time in milliseconds

        if (remainingTime <= 0) {
            clearInterval(timerInterval);
            timerElement.textContent = '00:00';
            submitForm();
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

function submitForm() {
    document.getElementById("audioForm").submit();
}

document.getElementById("startButton").addEventListener("click", function() {
    document.getElementById("startButton").style.display = "none";
    document.getElementById("stopButton").style.display = "block";

    fetch("/start_recording", { method: "POST" })
        .then(response => console.log(response.text()))
        .catch(error => console.error(error));
});

document.getElementById("stopButton").addEventListener("click", function() {
    document.getElementById("startButton").style.display = "block";
    document.getElementById("stopButton").style.display = "none";

    fetch("/stop_recording", { method: "POST" })
        .then(response => console.log(response.text()))
        .catch(error => console.error(error));
});

document.getElementById("submitBtn").addEventListener("click", submitForm);

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
