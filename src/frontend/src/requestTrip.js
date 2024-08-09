// Javascript file for requestTrip.

// Open new window to request a trip.
function openRequestTrip() {
  const username = sessionStorage.getItem("username");
  const customer_id = sessionStorage.getItem("customer_id") || "";
  if (!username) {
    alert("Please login to request a trip.");
    return;
  }
  const popupWindow = window.open(
    `../templates/requestTrip.html?username=${username}&customer_id=${customer_id}`,
    "Request Trip",
    "height=600,width=400,scrollbars=yes"
  );
  if (window.focus) {
    popupWindow.focus();
  }
}

// Fetch trip requests and display them.
function tripRequestFormSubmission() {
  const form = document.getElementById("tripRequest");
  if (!form) return;

  form.onsubmit = function (e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = {};
    formData.forEach((value, key) => {
      data[key] = value;
    });

    fetch("http://localhost:5005//trips/requests", {
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
document.addEventListener("DOMContentLoaded", tripRequestFormSubmission);
