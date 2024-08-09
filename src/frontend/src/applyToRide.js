// Javascript file for the apply to ride.

// Open a new window to display apply to ride form.
function openApplyToRidePopup() {
  const popupWindow = window.open(
    "templates/applyToRide.html",
    "Apply to Ride",
    "height=600,width=400"
  );
  if (window.focus) {
    popupWindow.focus();
  }
}

// Apply to ride submission form.
function handleApplyToRideFormSubmission() {
  const form = document.getElementById("applyToRideForm");
  if (!form) return;

  form.onsubmit = function (e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = {};
    formData.forEach((value, key) => {
      data[key] = value;
    });

    fetch("http://localhost:5004/coordinators/pending-customer-registrations", {
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
document.addEventListener("DOMContentLoaded", handleApplyToRideFormSubmission);
