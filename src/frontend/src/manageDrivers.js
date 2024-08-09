// Javascript file for managing drivers.

// Open new window to manage drivers.
function openManageDrivers() {
  const popupWindow = window.open(
    "../templates/manageDrivers.html",
    "Manage Drivers",
    "height=600,width=400,scrollbars=yes"
  );
  if (window.focus) {
    popupWindow.focus();
  }
}

// Fetch drivers and display in window.
async function fetchDrivers() {
  const response = await fetch("http://localhost:5003/drivers/all");
  const drivers = await response.json();
  const container = document.getElementById("manageDrivers");
  container.innerHTML = "";
  for (const driver of drivers) {
    const div = document.createElement("div");
    div.innerHTML = `
            <p>Driver ID: ${driver.driver_id}</p>
            <p>Username: ${driver.username}</p>
            <p>First Name: ${driver.first_name}</p>
            <p>Last Name: ${driver.last_name}</p>
            <p>License: ${driver.license}</p>
            <p>Car Make: ${driver.car_make}</p>
            <p>Car Model: ${driver.car_model}</p>
            <p>Car Registration: ${driver.car_reg}</p>
            <p>Car Colour: ${driver.car_colour}</p>
            <p>Email: ${driver.email}</p>
            <p>Mobile: ${driver.mobile}</p>
            <button onclick="editDriver(${driver.driver_id})">Edit</button>
            <button onclick="deleteDriver(${driver.driver_id})">Delete</button>
        `;
    container.appendChild(div);
  }
}

// Open new window to edit driver.
async function editDriver(driverId) {
  const popupWindow = window.open(
    `../templates/editDrivers.html?driverId=${driverId}`,
    "Edit Driver",
    "height=600,width=400,scrollbars=yes"
  );
  if (window.focus) {
    popupWindow.focus();
  }
}

// Delete driver.
async function deleteDriver(driverId) {
  const response = await fetch(`http://localhost:5003/drivers/${driverId}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    console.error("Failed to delete customer");
    return;
  } else if (response.ok) {
    alert("Driver deleted");
  }
  fetchCustomers();
}
document.addEventListener("DOMContentLoaded", fetchDrivers);
