document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ Admin Dashboard JS Loaded"); // Debugging

    setupBookingActions();  // Set up approve/reject event listeners
    setupNotificationActions();  // Set up notifications
});

// ✅ Function to handle Approve/Reject button clicks
function setupBookingActions() {
    document.body.addEventListener("click", function (event) {
        if (!event.target) return; // Prevent errors if event.target is null

        if (event.target.classList.contains("approve-btn") || event.target.classList.contains("reject-btn")) {
            const bookingId = event.target.getAttribute("data-booking-id");
            if (!bookingId) return; // Prevent errors if bookingId is null

            const action = event.target.classList.contains("approve-btn") ? "Approved" : "Rejected";

            console.log(`📌 Booking ID: ${bookingId}, Action: ${action}`); // Debugging

            updateBookingStatus(bookingId, action);
        }
    });
}

// ✅ Function to send Approve/Reject request
function updateBookingStatus(bookingId, status) {
    fetch(`/dashboard/update-booking/${bookingId}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ status: status }),
    })
    .then(response => {
        console.log("🔄 Response Status:", response.status); // Debugging
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert(`✅ Booking ${status} successfully!`);
            location.reload(); // Refresh to update UI
        } else {
            alert("❌ Failed to update booking.");
        }
    })
    .catch(error => console.error("⚠️ Error:", error));
}

// ✅ Function to handle notifications
function setupNotificationActions() {
    document.body.addEventListener("click", function (event) {
        if (!event.target) return; // Prevent errors if event.target is null

        if (event.target.classList.contains("delete-notification")) {
            const notificationId = event.target.getAttribute("data-notification-id");
            if (!notificationId) return; // Prevent errors if notificationId is null

            fetch(`/dashboard/delete-notification/${notificationId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("✅ Notification deleted!");
                    location.reload();
                } else {
                    alert("❌ Failed to delete notification.");
                }
            })
            .catch(error => console.error("⚠️ Error:", error));
        }
    });
}

// ✅ Function to get CSRF Token
function getCSRFToken() {
    const csrfTokenInput = document.querySelector("input[name='csrfmiddlewaretoken']");
    return csrfTokenInput ? csrfTokenInput.value : "";
}
