// JavaScript file for the pending customers page.

// Open new window to display the pending customers.
function pendingCustomer() {
  const popupWindow = window.open(
    "../templates/pendingCustomers.html",
    "Pending Customer Registration",
    "height=600,width=400,scrollbars=yes"
  );
  if (window.focus) {
    popupWindow.focus();
  }
}

// Fetch pending customer registrations and display in window.
async function fetchPendingRegistrations() {
  const response = await fetch(
    "http://localhost:5004/coordinators/pending-customer-registrations"
  );
  const registrations = await response.json();
  const container = document.getElementById("registrations");
  container.innerHTML = "";
  registrations.forEach((reg) => {
    const div = document.createElement("div");
    div.innerHTML = `
            <p>Registration ID: ${reg.registration_id}</p>
            <p>Status: ${reg.status}</p>
            <p>Username: ${reg.username}</p>
            <p>Name: ${reg.first_name} ${reg.last_name}</p>
            <p>Address: ${reg.address_line1} ${reg.address_line2}, ${reg.town}, ${reg.county}, ${reg.postcode}</p>
            <p>Email: ${reg.email}</p>
            <p>Mobile: ${reg.mobile}</p>
            <button onclick="approveRegistration(${reg.registration_id})">Accept</button>
            <button onclick="rejectRegistration(${reg.registration_id})">Reject</button>
        `;
    container.appendChild(div);
  });
}

// Approve registration.
async function approveRegistration(registrationId) {
  const response = await fetch(
    `http://localhost:5004/coordinators/pending-customer-registrations/${registrationId}/approve`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  if (response.ok) {
    alert("Registration approved successfully!");
    fetchPendingRegistrations();
  } else {
    alert("Failed to approve registration.");
  }
}

// Reject registration.
async function rejectRegistration(registrationId) {
  const response = await fetch(
    `http://localhost:5004/coordinators/pending-customer-registrations/${registrationId}/reject`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  if (response.ok) {
    alert("Registration rejected successfully!");
    fetchPendingRegistrations();
  } else {
    alert("Failed to reject registration.");
  }
}
document.addEventListener("DOMContentLoaded", fetchPendingRegistrations);
