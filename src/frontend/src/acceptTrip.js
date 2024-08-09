// Javascript file for the acceptTrip.html.

// Open a new window to display accept trip form.
function openAcceptTrip() {
  const popupWindow = window.open(
    "../templates/acceptTrip.html",
    "Accept Trip",
    "height=600,width=400,scrollbars=yes"
  );
  if (window.focus) {
    popupWindow.focus();
  }
}

// Method to get username from session storage.
function getUsernameFromOpener() {
  if (window.opener && !window.opener.closed) {
    return window.opener.sessionStorage.getItem("username");
  }
  return null;
}

// Fetch the customer details using the customer ID.
async function fetchCustomerDetails(customerId) {
  const response = await fetch(`http://localhost:5002/customers/${customerId}`);
  if (!response.ok) {
    console.error("Failed to fetch customer details");
    return null;
  }
  const customerDetails = await response.json();
  return customerDetails;
}

// Fetch the trip requests and display them in the window.
async function fetchTripRequests() {
  const response = await fetch("http://localhost:5005/trips/requests/pending");
  const tripRequests = await response.json();
  const container = document.getElementById("tripRequests");
  container.innerHTML = "";
  for (const req of tripRequests) {
    const customerDetails = await fetchCustomerDetails(req.customer_id);
    if (!customerDetails) {
      console.error("Failed to fetch customer details");
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
            <p>Address: ${customerDetails.address_line1}, ${customerDetails.address_line2},
            ${customerDetails.town}, ${customerDetails.county}, ${customerDetails.postcode}</p>
            <p>Mobile: ${customerDetails.mobile}</p>
            <p>Additional Passenger: ${req.additional_passenger}</p>
            <p>Purpose: ${req.purpose}</p>
            <button onclick="approveTripRequest(${req.trip_request_id})">Accept</button>
            <button onclick="rejectTripRequest(${req.trip_request_id})">Reject</button>
        `;
    container.appendChild(div);
  }
}

// Approve the trip request.
async function approveTripRequest(tripRequestId) {
  const username = getUsernameFromOpener();
  let driverId = null;
  if (username) {
    try {
      const response = await fetch(`http://localhost:5003/drivers/${username}`);
      const data = await response.json();
      if (data.driver_id) {
        driverId = data.driver_id;
      } else {
        console.error("Driver not found");
        alert("Driver not found.");
        return;
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to fetch driver information.");
      return;
    }
  }
  const currentDate = new Date().toISOString().split("T")[0];
  const currentTime = new Date().toTimeString().split(" ")[0].substring(0, 5);
  const response = await fetch(
    `http://localhost:5005/trips/requests/${tripRequestId}/confirm`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        driver_id: driverId,
        confirmation_date: currentDate,
        confirmation_time: currentTime,
      }),
    }
  );
  if (response.ok) {
    alert("Trip request approved successfully!");
    fetchTripRequests();
  } else {
    alert("Failed to approve trip request.");
  }
}

// Reject the trip request.
async function rejectTripRequest(tripRequestId) {
  const response = await fetch(
    `http://localhost:5005/trips/requests/${tripRequestId}`,
    {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  if (response.ok) {
    alert("Trip request rejected successfully!");
    fetchTripRequests();
  } else {
    alert("Failed to reject trip request.");
  }
}
document.addEventListener("DOMContentLoaded", fetchTripRequests);
