// Javascript file for coordinatorTripRequests.

// Open a new window to display trip requests.
function openTripRequestsPopup() {
  const popupWindow = window.open(
    "../templates/coordinatorTripRequests.html",
    "Trip Requests",
    "height=600,width=400,scrollbars=yes,resizable=yes"
  );
  if (window.focus) {
    popupWindow.focus();
  }
}

// Fetch customer details using the customer ID.
async function fetchCustomerDetails(customerId) {
  const response = await fetch(`http://localhost:5002/customers/${customerId}`);
  if (!response.ok) {
    console.error("Failed to fetch customer details");
    return null;
  }
  const customerDetails = await response.json();
  return customerDetails;
}

// Get the drivers details using the driver Id.
async function fetchDriverDetails(driverId) {
  const response = await fetch(`http://localhost:5003/drivers/${driverId}`);
  if (!response.ok) {
    console.error("Failed to fetch customer details");
    return null;
  }
  const driverDetails = await response.json();
  return driverDetails;
}

// Fetch trip request details.
async function fetchConfirmedTrips() {
  const response = await fetch("http://localhost:5005/trips/requests");
  if (!response.ok) {
    console.error("Failed to fetch confirmed trips");
    return;
  }
  const tripRequests = await response.json();
  const container = document.getElementById("tripRequests");
  container.innerHTML = "";
  for (const req of tripRequests) {
    const customerDetails = await fetchCustomerDetails(req.customer_id);
    if (!customerDetails) {
      continue;
    }
    const div = document.createElement("div");
    div.innerHTML = `
        
            <p>Trip Request ID: ${req.trip_request_id}</p>
            <p>Date: ${req.date}</p>
            <p>Time: ${req.time}</p>
            <p>Destination: ${req.destination}</p>
            <p>Status: ${req.status}</p>
            <p>Customer Name: ${customerDetails.first_name} ${customerDetails.last_name}</p>
            <p>Customer Email: ${customerDetails.email}</p>
            <p>Address: ${customerDetails.address_line1}, 
            ${customerDetails.address_line2}, ${customerDetails.town}, ${customerDetails.county}, 
            ${customerDetails.postcode}</p>
            <p>Mobile: ${customerDetails.mobile}</p>
            <p>Additional Passenger: ${req.additional_passenger}</p>
            <p>Purpose: ${req.purpose}</p>
            <button onclick="deleteTrip(${req.trip_request_id})">Delete</button>
        `;
    container.appendChild(div);
  }
}

// Delete the trip request.
async function deleteTrip(confirmedTripId) {
  const response = await fetch(
    `http://localhost:5005/trips/requests/${confirmedTripId}`,
    {
      method: "DELETE",
    }
  );
  if (!response.ok) {
    console.error("Failed to delete trip");
    return;
  } else {
    alert("Trip deleted successfully!");
  }

  fetchConfirmedTrips();
}
document.addEventListener("DOMContentLoaded", fetchConfirmedTrips);
