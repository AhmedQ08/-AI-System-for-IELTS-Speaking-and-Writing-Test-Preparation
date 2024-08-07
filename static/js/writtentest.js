
const goBackButton = document.getElementById("go-back-button");


goBackButton.addEventListener("click", function() {
  // Redirect to the dashboard.html page
  window.location.href = "/dashboard";
});

const reportButton = document.getElementById("report-button");

// Add a click event listener to the button
reportButton.addEventListener("click", function() {
  // Redirect to the dashboard.html page
  window.location.href = "/writtentest_report";
});



document.addEventListener("DOMContentLoaded", function() {
    // Find the button elements for all modals
    const quickTestBoardButton = document.getElementById("quick-test-board-button");
    const intermediateTestBoardButton = document.getElementById("intermediate-test-board-button");
    const advancedTestBoardButton = document.getElementById("advanced-test-board-button");

    // Add click event listener to quick test board button
    quickTestBoardButton.addEventListener("click", function() {
        // Close the quick test modal
        const quickModal = document.getElementById("quickBackdrop");
        const quickModalInstance = bootstrap.Modal.getInstance(quickModal);
        quickModalInstance.hide();

        // Redirect to the quick_test_board.html page after a short delay
        setTimeout(function() {
            window.location.href = "/quicktestboard";
        }, 300); // Adjust the delay time as needed
    });

    // Add click event listener to intermediate test board button
    intermediateTestBoardButton.addEventListener("click", function() {
        // Close the intermediate test modal
        const intermediateModal = document.getElementById("intermediateBackdrop");
        const intermediateModalInstance = bootstrap.Modal.getInstance(intermediateModal);
        intermediateModalInstance.hide();

        // Redirect to the intermediate_test_board.html page after a short delay
        setTimeout(function() {
            window.location.href = "/task_2";
        }, 300); // Adjust the delay time as needed
    });
});







