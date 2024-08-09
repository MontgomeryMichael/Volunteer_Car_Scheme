// JavaScript file for the apply to drive.

// Open new window to display apply to drive form.
function openApplyToDrivePopup() {
  const popupWindow = window.open(
    "templates/applyToDrive.html",
    "Apply to Drive",
    "height=600,width=400"
  );
  if (window.focus) {
    popupWindow.focus();
  }
}

// Apply to Drive submission form.
function handleApplyToDriveFormSubmission() {
  const form = document.getElementById("applyToDriveForm");
  if (!form) return;

  form.onsubmit = function (e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = {};
    formData.forEach((value, key) => {
      data[key] = value;
    });

    fetch("http://localhost:5004//coordinators/pending-driver-registrations", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        alert("Application submitted successfully!");
        window.close();
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Failed to submit application. Please try again later.");
      });
  };
}
document.addEventListener("DOMContentLoaded", handleApplyToDriveFormSubmission);
