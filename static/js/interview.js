





document.addEventListener("DOMContentLoaded", function() {

    const introductionInterviewButton = document.getElementById("introduction-interview-button");
    const discussionInterviewButton = document.getElementById("discussion-interview-button");
    const interviewReportButton = document.getElementById("interview-report-button");
    const goBackButton = document.getElementById("go-back-button");

    introductionInterviewButton.addEventListener("click", function() {
      
        const quickModal = document.getElementById("quickBackdrop");
        const quickModalInstance = bootstrap.Modal.getInstance(quickModal);
        quickModalInstance.hide();

        
        setTimeout(function() {
            window.location.href = "/introductionInterview";
        }, 300); 
    });

    
    discussionInterviewButton.addEventListener("click", function() {
       
        const discussionModal = document.getElementById("discussionBackdrop");
        const discussionModalInstance = bootstrap.Modal.getInstance(discussionModal);
        discussionModalInstance.hide();

        setTimeout(function() {
            window.location.href = "/discussioninterview";
        }, 300); 
    });

    interviewReportButton.addEventListener("click", function() {
        window.location.href = "/interview_report";
    });

    goBackButton.addEventListener("click", function() {
  
        window.location.href = "/dashboard";
      });
});
