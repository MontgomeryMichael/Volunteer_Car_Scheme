// Javascript to display confirmed trips.

// Open a new window to display trips.
function openConfirmedTrips() {
  const popupWindow = window.open(
    "../templates/coordinatorConfirmedTrips.html",
    "Confirmed Trips",
    "height=600,width=400,scrollbars=yes,resizable=yes"
  );
  if (window.focus) {
    popupWindow.focus();
  }
}

// Fetch the customers details using the customer ID.
async function fetchCustomerDetails(customerId) {
  const response = await fetch(`http://localhost:5002/customers/${customerId}`);
  if (!response.ok) {
    console.error("Failed to fetch customer details");
    return null;
  }
  const customerDetails = await response.json();
  return customerDetails;
}

// Fetch the drivers details using the driver ID.
async function fetchDriverDetails(driverId) {
  const response = await fetch(`http://localhost:5003/drivers/${driverId}`);
  if (!response.ok) {
    console.error("Failed to fetch customer details");
    return null;
  }
  const driverDetails = await response.json();
  return driverDetails;
}

// Fetch the trip request details using the trip request ID.
async function fetchTripRequestDetails(tripRequestId) {
  const response = await fetch(
    `http://localhost:5005/trips/requests/${tripRequestId}`
  );
  if (!response.ok) {
    console.error("Failed to fetch trip request details");
    return null;
  }
  const tripRequestDetails = await response.json();
  return tripRequestDetails;
}

// Fetch the confirmed trips and display them in the window.
// For each trip there is a button to delete the trip.
async function fetchConfirmedTrips() {
  const response = await fetch("http://localhost:5005/trips/confirmed");
  if (!response.ok) {
    console.error("Failed to fetch confirmed trips");
    return;
  }
  const confirmedTrips = await response.json();
  const container = document.getElementById("confirmedTrips");
  container.innerHTML = "";
  for (const req of confirmedTrips) {
    const customerDetails = await fetchCustomerDetails(req.customer_id);
    if (!customerDetails) {
      continue;
    }
    const driverDetails = await fetchDriverDetails(req.driver_id);
    if (!driverDetails) {
      continue;
    }
    const tripRequestDetails = await fetchTripRequestDetails(
      req.trip_request_id
    );
    if (!tripRequestDetails) {
      continue;
    }
    const div = document.createElement("div");
    div.innerHTML = `
        
            <p>Trip Request ID: ${req.trip_request_id}</p>
            <p>Date: ${tripRequestDetails.date}</p>
            <p>Time: ${tripRequestDetails.time}</p>
            <p>Destination: ${tripRequestDetails.destination}</p>
            <p>Status: ${tripRequestDetails.status}</p>
            <p>Customer Name: ${customerDetails.first_name} ${customerDetails.last_name}</p>
            <p>Customer Email: ${customerDetails.email}</p>
            <p>Address: ${customerDetails.address_line1}, ${customerDetails.address_line2}, 
             ${customerDetails.town}, ${customerDetails.county}, ${customerDetails.postcode}</p>
            <p>Mobile: ${customerDetails.mobile}</p>
            <p>Additional Passenger: ${tripRequestDetails.additional_passenger}</p>
            <p>Purpose: ${tripRequestDetails.purpose}</p>
            <p>Driver ID: ${req.driver_id}</p>
            <p>Driver Name: ${driverDetails.first_name} ${driverDetails.last_name}</p>
            <p>Driver Email: ${driverDetails.email}</p>
            <p>Driver Mobile: ${driverDetails.mobile}</p>
            <p>Driver Vehicle Make: ${driverDetails.car_make}</p>
            <p>Driver Vehicle Model: ${driverDetails.car_model}</p>
            <button onclick="deleteTrip(${req.trip_request_id})">Delete</button>
        `;
    container.appendChild(div);
  }
}

// Delete the trip using the confirmed trip ID.
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
