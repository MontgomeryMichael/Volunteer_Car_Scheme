// Javascript file for pendingDrivers.

// Open new window to display the pending driver registrations.
function pendingDriver() {
  const popupWindow = window.open(
    "../templates/pendingDrivers.html",
    "Pending Drivers Registration",
    "height=600,width=400,scrollbars=yes"
  );
  if (window.focus) {
    popupWindow.focus();
  }
}

// Fetch the pending driver registrations and display.
async function fetchPendingDriverRegistrations() {
  const response = await fetch(
    "http://localhost:5004/coordinators/pending-driver-registrations"
  );
  const registrations = await response.json();
  const container = document.getElementById("driver_registrations");
  container.innerHTML = "";
  registrations.forEach((reg) => {
    const div = document.createElement("div");
    div.innerHTML = `
            <p>Registration ID: ${reg.registration_id}</p>
            <p>Status: ${reg.status}</p>
            <p>Username: ${reg.username}</p>
            <p>Name: ${reg.first_name} ${reg.last_name}</p>
            <p>License: ${reg.license}</p>
            <p>Car Make: ${reg.car_make}</p>
            <p>Car Model: ${reg.car_model}</p>
            <p>Car Registration: ${reg.car_reg}</p>
            <p>Car Colour: ${reg.car_colour}</p>
            <p>Email: ${reg.email}</p>
            <p>Mobile: ${reg.mobile}</p>
            <button onclick="approveDriverRegistration(${reg.registration_id})">Accept</button>
            <button onclick="rejectDriverRegistration(${reg.registration_id})">Reject</button>
        `;
    container.appendChild(div);
  });
}

// Reject driver registration.
async function rejectDriverRegistration(registrationId) {
  const response = await fetch(
    `http://localhost:5004/coordinators/pending-driver-registrations/${registrationId}/reject`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  if (response.ok) {
    alert("Registration rejected successfully!");
    fetchPendingDriverRegistrations();
  } else {
    alert("Failed to reject registration.");
  }
}

// Approve driver registration.
async function approveDriverRegistration(registrationId) {
  const response = await fetch(
    `http://localhost:5004/coordinators/pending-driver-registrations/${registrationId}/approve`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  if (response.ok) {
    alert("Registration approved successfully!");
    fetchPendingDriverRegistrations();
  } else {
    alert("Failed to approve registration.");
  }
}
document.addEventListener("DOMContentLoaded", fetchPendingDriverRegistrations);
