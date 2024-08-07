document.addEventListener("DOMContentLoaded", function() {

    const written = document.getElementById("written_test");
    const interview = document.getElementById("interview");
    const settings = document.getElementById("settings");


    written.addEventListener("click", function() {
        window.location.href = "/writtentest";
    });

    interview.addEventListener("click", function() {
        window.location.href = "/interview";
    });

    settings.addEventListener("click", function() {
        window.location.href = "/settings";
    });
});
