// JavaScript file for the driverCurrentTrip.

// Open new window to display the current trip.
function openCurrentTrips() {
  const popupWindow = window.open(
    "../templates/driverCurrentTrip.html",
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

// Fetch driver details using the driver ID.
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
  const container = document.getElementById("currentTrips");
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
    // If the trip date is today, display the trip details
    var today = new Date();
    var tripDate = new Date(tripRequestDetails.date);
    if (today.toDateString() == tripDate.toDateString()) {
      const div = document.createElement("div");
      div.innerHTML = `
                <p>Trip Request ID: ${req.trip_request_id}</p>
                <p>Date: ${tripRequestDetails.date}</p>
                <p>Time: ${tripRequestDetails.time}</p>
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
                <div id="map-${req.trip_request_id}" style="height: 400px; width: 100%;"></div>
                <button onclick="cancelTrip(${req.confirmed_trip_id})">Cancel Trip</button>
            `;
      container.appendChild(div);

      // Initialize the map for this trip
      initMap(customerDetails.postcode, `map-${req.trip_request_id}`);
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

// Fetch the coordinates from the postcode.
async function getCoordinatesFromPostcode(postcode) {
  const response = await fetch(
    `https://nominatim.openstreetmap.org/search?format=json&limit=1&q=${encodeURIComponent(
      postcode
    )}`
  );
  if (!response.ok) {
    console.error("Failed to fetch coordinates");
    return null;
  }
  const data = await response.json();
  if (data.length === 0) {
    console.error("No results found for the postcode");
    return null;
  }
  const coordinates = {
    lat: parseFloat(data[0].lat),
    lon: parseFloat(data[0].lon),
  };
  return coordinates;
}

// Initialize map.
async function initMap(postcode, mapId) {
  const coords = await getCoordinatesFromPostcode(postcode);
  if (!coords) {
    console.error("Could not get coordinates for postcode:", postcode);
    return;
  }
  const map = L.map(mapId).setView([coords.lat, coords.lon], 13);

  // Set up OpenStreetMap.
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

  // Add coordinates.
  L.marker([coords.lat, coords.lon])
    .addTo(map)
    .bindPopup(`<b>${postcode}</b>`)
    .openPopup();
}
document.addEventListener("DOMContentLoaded", fetchConfirmedTrips);
