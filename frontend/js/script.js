document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const cvScrapeBtn = document.getElementById("cvScrapeBtn");
    const jobApplyBtn = document.getElementById("jobApplyBtn");

    let action = null;

    // Set the action depending on which button is clicked
    cvScrapeBtn.addEventListener("click", (event) => {
        event.preventDefault();
        action = "cv_scrape";
        loginForm.requestSubmit(); // Trigger form submit programmatically
    });

    jobApplyBtn.addEventListener("click", (event) => {
        event.preventDefault();
        action = "job_apply";
        loginForm.requestSubmit();
    });

    // Form submission handler
    loginForm.addEventListener("submit", (event) => {
        event.preventDefault();

        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value.trim();
        const status = document.getElementById("status");

        // Basic validation (you can extend this)
        if (!username || !password) {
            status.textContent = "Please fill in both fields.";
            status.className = "error";
            return;
        }

        setTimeout(() => {
            status.textContent = "Login successful!";
            status.className = "success";

            // Redirect based on which button was clicked
            if (action === "cv_scrape") {
                window.location.href = "cv_scrape.html";
            } else if (action === "job_apply") {
                window.location.href = "job_apply.html";
            }
        }, 1000);
    });
});
