// JavaScript file for customerCurrentTrip.

// Open new window to display the current trip.
function openCustomerCurrentTripPopup() {
  const popupWindow = window.open(
    "../templates/customerCurrentTrip.html",
    "Current Trips",
    "height=600,width=400,scrollbars=yes,resizable=yes"
  );
  if (window.focus) {
    popupWindow.focus();
  }
}

// Fetch username from the opener window.
function getUsernameFromOpener() {
  if (window.opener && !window.opener.closed) {
    return window.opener.sessionStorage.getItem("username");
  }
  return null;
}

// Fetch customer details using the username.
async function fetchCustomerDetails() {
  const username = getUsernameFromOpener();
  const response = await fetch(
    `http://localhost:5002/customers/details/${username}`
  );
  if (!response.ok) {
    console.error("Failed to fetch customer details");
    return null;
  }
  const customerDetails = await response.json();
  return customerDetails;
}

// Fetch driver details using the driver ID.
async function fetchDriverDetails(driverId) {
  const response = await fetch(`http://localhost:5003/drivers/${driverId}`);
  if (!response.ok) {
    console.error("Failed to fetch customer details");
    return null;
  }
  const driverDetails = await response.json();
  return driverDetails;
}

// Fetch trip request details using the trip request ID.
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
async function fetchConfirmedTrips() {
  const customerDetails = await fetchCustomerDetails();
  const customerId = customerDetails.customer_id;
  const response = await fetch(
    `http://localhost:5005/trips/confirmed/customer/${customerId}`
  );
  if (!response.ok) {
    console.error("Failed to fetch confirmed trips");
    return;
  }
  const confirmedTrips = await response.json();
  const container = document.getElementById("customerCurrentTrips");
  container.innerHTML = "";
  for (const req of confirmedTrips) {
    const driverDetails = await fetchDriverDetails(req.driver_id);
    if (!driverDetails) {
      console.error("Failed to fetch driver details");
      continue;
    }
    const tripRequestDetails = await fetchTripRequestDetails(
      req.trip_request_id
    );
    if (!tripRequestDetails) {
      console.error("Failed to fetch trip request details");
      continue;
    }
    // If the trip date is today, display the trip details
    var today = new Date();
    var tripDate = new Date(tripRequestDetails.date);
    if (today.toDateString() == tripDate.toDateString()) {
      const div = document.createElement("div");
      div.innerHTML = `
        
                <p>Trip Request ID: ${req.trip_request_id}</p>
                <p>Date: ${tripRequestDetails.date}</p>
                <p>Time: ${tripRequestDetails.time}</p>
                <p>Confirmation Date: ${req.confirmation_date}</p>
                <p>Confirmation Time: ${req.confirmation_time}</p>
                <p>Purpose: ${tripRequestDetails.purpose}</p>
                <p>Destination: ${tripRequestDetails.destination}</p>
                <p>Additional Passenger: ${tripRequestDetails.additional_passenger}</p>
                <p>Driver's Name: ${driverDetails.first_name} ${driverDetails.last_name}</p>
                <p>Car Make: ${driverDetails.car_make}</p>
                <p>Car Model: ${driverDetails.car_model}</p>
                <p>Car Colour: ${driverDetails.car_colour}</p>
                <p>Car Registration: ${driverDetails.car_registration}</p>
                <p>Driver's Email: ${driverDetails.email}</p> 
                <button onclick="cancelTrip(${req.confirmed_trip_id})">Cancel Trip</button>
            `;
      container.appendChild(div);
    }
  }
}

// Cancel the trip.
async function cancelTrip(confirmedTripId) {
  const response = await fetch(
    `http://localhost:5005/trips/confirmed/${confirmedTripId}`,
    {
      method: "DELETE",
    }
  );
  if (!response.ok) {
    console.error("Failed to cancel trip");
    return;
  } else {
    alert("Trip Cancelled");
  }

  fetchConfirmedTrips();
}
document.addEventListener("DOMContentLoaded", fetchConfirmedTrips);
