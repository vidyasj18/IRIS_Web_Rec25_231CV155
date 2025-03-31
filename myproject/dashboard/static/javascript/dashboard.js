// this file helps in fetching and showing real-time updates dynamically.
// created using ajax:
// - Asynchronous Javascript and XML 
// - allows webpages to communicate with a web server asynchronously.
// - it can send and recieve data without interfering with the usr's interaction on the page.

// 

document.addEventListener("DOMContentLoaded", function () {
    console.log("Dashboard JS Loaded!");

    // Fetch updates for equipment list dynamically
    function fetchUpdates() {
        fetch("/dashboard/api/dashboard-updates/")
            .then(response => response.json())
            .then(data => {
                console.log("API Response:", data);
                updateEquipmentList(data.equipment);
            })
            .catch(error => console.error("Error fetching updates:", error));
    }

    // Update equipment list dynamically
    function updateEquipmentList(equipment) {
        const equipmentList = document.getElementById("equipment-list");
        if (!equipmentList) {
            console.error("Error: 'equipment-list' not found in the DOM.");
            return;
        }

        equipmentList.innerHTML = "";
        equipment.forEach(item => {
            const listItem = document.createElement("li");
            listItem.className = "equipment-item";
            listItem.innerHTML = `
                <span>${item.name} (${item.quantity} available)</span>
                <button class="book-equipment-btn" data-equipment-id="${item.id}">
                    Book
                </button>
            `;
            equipmentList.appendChild(listItem);
        });

        attachBookEventListeners();
    }

    // Function to book equipment
    function bookEquipment(equipmentId) {
        const requestedSlot = new Date().toISOString();
        fetch(`/book-equipment/${equipmentId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ requested_slot: requestedSlot })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Booking successful!");
                fetchUserBookings();
            } else {
                alert(data.error);
            }
        })
        .catch(error => console.error("Error:", error));
    }

    function attachBookEventListeners() {
        document.querySelectorAll(".book-equipment-btn").forEach(button => {
            button.addEventListener("click", function () {
                console.log("Book button clicked! Equipment ID:", this.dataset.equipmentId);
                bookEquipment(this.dataset.equipmentId);
            });
        });
    }

    // Display user bookings dynamically
    function displayBookings(bookings) {
        let bookingsContainer = document.getElementById("bookings-list");
        if (!bookingsContainer) {
            console.error("Error: 'bookings-list' not found in the DOM.");
            return;
        }

        bookingsContainer.innerHTML = ""; // Clear previous bookings

        if (bookings.length === 0) {
            bookingsContainer.innerHTML = "<p>No bookings found.</p>";
            return;
        }

        bookings.forEach(booking => {
            let bookingCard = document.createElement("div");
            bookingCard.classList.add("booking-card");

            let statusColor = "gray";
            if (booking.status === "Approved") statusColor = "green";
            else if (booking.status === "Pending") statusColor = "orange";
            else if (booking.status === "Rejected") statusColor = "red";

            bookingCard.innerHTML = `
                <p><strong>Equipment:</strong> ${booking.equipment}</p>
                <p><strong>Requested Slot:</strong> ${new Date(booking.requested_slot).toLocaleString()}</p>
                <p><strong>Status:</strong> <span style="color: ${statusColor};">${booking.status}</span></p>
                <button class="cancel-booking-btn" data-id="${booking.id}" ${booking.status !== "Approved" ? "disabled" : ""}>
                    Cancel Booking
                </button>
            `;

            bookingsContainer.appendChild(bookingCard);
        });

        attachCancelEventListeners();
    }

    // Function to cancel a booking
    function cancelBooking(bookingId) {
        fetch(`/cancel-booking/${bookingId}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert("Your cancellation request has been submitted.");
                fetchUserBookings();
            } else {
                alert("Cancellation failed: " + data.error);
            }
        })
        .catch(error => console.error("Error canceling booking:", error));
    }

    function attachCancelEventListeners() {
        document.querySelectorAll(".cancel-booking-btn").forEach(button => {
            button.addEventListener("click", function () {
                console.log("Cancel button clicked!");
                cancelBooking(this.dataset.id);
            });
        });
    }

    // Fetch user bookings
    function fetchUserBookings() {
        const bookingsContainer = document.getElementById("bookings-list");
        if (!bookingsContainer) {
            console.warn("Warning: 'bookings-list' not found in the DOM. Skipping fetchUserBookings().");
            return; // Stop execution if element is missing
        }
        
        fetch("/dashboard/api/user-bookings/")
            .then(response => response.json())
            .then(data => {
                console.log("User Bookings:", data);
                displayBookings(data);
            })
            .catch(error => console.error("Error fetching bookings:", error));
    }


    fetchUserBookings();

    // Book an infrastructure slot
    function bookInfrastructure(infraId) {
        fetch("/api/bookings/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({
                infrastructure: infraId,
                start_time: new Date().toISOString(), // Adjust as needed
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert("Booking request submitted!");
                fetchUserBookings();
            }
        })
        .catch(error => console.error("Error booking infrastructure:", error));
    }

    // Fetch and display available infrastructures
    function fetchInfrastructure() {
        fetch("/api/infrastructures/")
            .then(response => response.json())
            .then(data => {
                const infraContainer = document.getElementById("infrastructure-list");
                infraContainer.innerHTML = "";
                data.forEach(infra => {
                    const infraCard = `
                        <div class="infra-card">
                            <h3>${infra.name}</h3>
                            <p>Location: ${infra.location}</p>
                            <p>Capacity: ${infra.capacity}</p>
                            <p>Operating Hours: ${infra.operating_hours}</p>
                            <button onclick="bookInfrastructure(${infra.id})">Book</button>
                        </div>
                `   ;
                    infraContainer.innerHTML += infraCard;
                });
            })
            .catch(error => console.error("Error fetching infrastructures:", error));
    }

    function fetchUserBookings() {
        fetch("/api/user/bookings/")
            .then(response => response.json())
            .then(data => {
                const bookingContainer = document.getElementById("user-bookings");
                bookingContainer.innerHTML = "";
                data.forEach(booking => {
                    const bookingItem = `
                        <div class="booking-card">
                            <p>Infrastructure: ${booking.infrastructure.name}</p>
                            <p>Status: ${booking.status}</p>
                            ${booking.status === "Pending" ? `<button onclick="cancelBooking(${booking.id})">Cancel</button>` : ""}
                        </div>
                    `;
                    bookingContainer.innerHTML += bookingItem;
                });
            })
            .catch(error => console.error("Error fetching bookings:", error));
    }

    // Cancel a booking
    function cancelBooking(bookingId) {
        fetch(`/api/cancel-booking/${bookingId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
            },
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            fetchUserBookings();
        })
        .catch(error => console.error("Error canceling booking:", error));
    }

    // Get CSRF token
    function getCSRFToken() {
        return document.cookie.split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
    }

    // Fetch bookings 
    fetchUserBookings();
});
