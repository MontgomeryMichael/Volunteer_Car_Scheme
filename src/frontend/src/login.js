// Javascript for login.

// Listen for the form submission.
document
  .getElementById("actualLoginForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch("http://localhost:5001/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.role === "Customer") {
          sessionStorage.setItem("username", username);
          window.location.href = "templates/customers.html";
        } else if (data.role === "Driver") {
          sessionStorage.setItem("username", username);
          window.location.href = "templates/driver.html";
        } else if (data.role === "Coordinator") {
          sessionStorage.setItem("username", username);
          window.location.href = "templates/coordinator.html";
        } else {
          alert("Login failed or your role does not have a specific homepage.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Login failed. Please try again.");
      });
  });
