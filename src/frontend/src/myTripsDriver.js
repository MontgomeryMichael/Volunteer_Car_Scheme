// JavaScript file for myTripsDriver.

// Open new window to display the my trips.
function openMyTripsPopup() {
  const popupWindow = window.open(
    "../templates/myTripsDriver.html",
    "My Trips",
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

// Fetch customer details using the customer ID.
async function fetchCustomerDetails(customer_id) {
  const response = await fetch(
    `http://localhost:5002/customers/${customer_id}`
  );
  if (!response.ok) {
    console.error("Failed to fetch customer details");
    return null;
  }
  const customerDetails = await response.json();
  return customerDetails;
}

// Fetch driver details using the driver username.
async function fetchDriverDetails() {
  const username = getUsernameFromOpener();
  const response = await fetch(
    `http://localhost:5003/drivers/details/${username}`
  );
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
  const driverDetails = await fetchDriverDetails();
  const response = await fetch(
    "http://localhost:5005/trips/confirmed/driver/" + driverDetails.driver_id
  );
  if (!response.ok) {
    console.error("Failed to fetch confirmed trips");
    return;
  }
  const confirmedTrips = await response.json();
  const container = document.getElementById("myTripsDriver");
  container.innerHTML = "";
  for (const req of confirmedTrips) {
    const tripRequestDetails = await fetchTripRequestDetails(
      req.trip_request_id
    );
    if (!tripRequestDetails) {
      console.error("Failed to fetch trip request details");
      continue;
    }
    const customerDetails = await fetchCustomerDetails(
      tripRequestDetails.customer_id
    );
    if (!customerDetails) {
      console.error("Failed to fetch customer details");
      continue;
    }
    const div = document.createElement("div");
    div.innerHTML = `
            <p>Trip Request ID: ${req.trip_request_id}</p>
            <p>Date: ${tripRequestDetails.date}</p>
            <p>Time: ${tripRequestDetails.time}</p>
            <p>Confirmation Date: ${req.confirmation_date}</p>
            <p>Confirmation Time: ${req.confirmation_time}</p>
            <p>Purpose: ${tripRequestDetails.purpose}</p>
            <p>Destination: ${tripRequestDetails.destination}</p>
            <p>First Name: ${customerDetails.first_name}</p>
            <p>Last Name: ${customerDetails.last_name}</p>
            <p>Additional Passenger: ${tripRequestDetails.additional_passenger}</p>
            <p>Address Line 1: ${customerDetails.address_line1}</p>
            <p>Address Line 2: ${customerDetails.address_line2}</p>
            <p>Town: ${customerDetails.town}</p>
            <p>County: ${customerDetails.county}</p>
            <p>Postcode: ${customerDetails.postcode}</p>
            <p>Mobile: ${customerDetails.mobile}</p>
            <p>Email: ${customerDetails.email}</p>
            <button onclick="cancelTrip(${req.confirmed_trip_id})">Cancel Trip</button>
        `;
    container.appendChild(div);
  }
}

// Cancel trip.
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
