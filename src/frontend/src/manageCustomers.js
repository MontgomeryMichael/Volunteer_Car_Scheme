// JavaScript file for manageCustomers.

// Open new window to display the manage customers.
function openManageCustomers() {
  const popupWindow = window.open(
    "../templates/manageCustomers.html",
    "Manage Customers",
    "height=600,width=400,scrollbars=yes"
  );
  if (window.focus) {
    popupWindow.focus();
  }
}
// Fetch customers and display in window.
async function fetchCustomers() {
  const response = await fetch("http://localhost:5002/customers/all");
  const customers = await response.json();
  const container = document.getElementById("manageCustomers");
  container.innerHTML = "";
  for (const customer of customers) {
    const div = document.createElement("div");
    div.innerHTML = `
            <p>Customer ID: ${customer.customer_id}</p>
            <p>First Name: ${customer.first_name}</p>
            <p>Last Name: ${customer.last_name}</p>
            <p>Email: ${customer.email}</p>
            <p>Address: ${customer.address_line1}, ${customer.address_line2}, ${customer.town}, ${customer.county}, ${customer.postcode}</p>
            <p>Mobile: ${customer.mobile}</p>
            <button onclick="editCustomer(${customer.customer_id})">Edit</button>
            <button onclick="deleteCustomer(${customer.customer_id})">Delete</button>
            <button onclick="openRequestTrip(${customer.customer_id})", 'Request Trip', 'height=600,width=400,scrollbars=yes')">Request Trip</button>
        `;
    container.appendChild(div);
  }
}
// Open window to request a trip.
async function openRequestTrip(customerId) {
  const popupWindow = window.open(
    `../templates/requestTrip.html?customer_id=${customerId}`,
    "Request Trip",
    "height=600,width=400,scrollbars=yes"
  );
  if (window.focus) {
    popupWindow.focus();
  }
}

// Open new window to edit customer.
async function editCustomer(customerId) {
  const popupWindow = window.open(
    `../templates/editCustomers.html?customerId=${customerId}`,
    "Edit Customer",
    "height=600,width=400,scrollbars=yes"
  );
  if (window.focus) {
    popupWindow.focus();
  }
}

// Delete customer.
async function deleteCustomer(customerId) {
  const response = await fetch(
    `http://localhost:5002/customers/${customerId}`,
    {
      method: "DELETE",
    }
  );
  if (!response.ok) {
    console.error("Failed to delete customer");
    return;
  } else if (response.ok) {
    alert("Customer deleted");
  }
  fetchCustomers();
}
document.addEventListener("DOMContentLoaded", fetchCustomers);
