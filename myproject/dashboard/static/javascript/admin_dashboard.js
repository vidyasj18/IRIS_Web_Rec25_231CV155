document.addEventListener("DOMContentLoaded", function () {
    console.log("hii");

    // Function to handle booking approval/rejection
    function updateBookingStatus(bookingId, action) {
        fetch(`/dashboard/update-booking/${bookingId}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({ status: action }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`Booking ${action} successfully!`);
                location.reload(); // Refresh page to reflect changes
            } else {
                alert("Failed to update booking.");
            }
        })
        .catch(error => console.error("Error:", error));
    }

    // Function to set up booking actions
    function setupBookingActions() {
        document.body.addEventListener("click", function (event) {
            if (event.target.classList.contains("approve-btn")) {
                const bookingId = event.target.getAttribute("data-booking-id");
                updateBookingStatus(bookingId, "Approved");
            } else if (event.target.classList.contains("reject-btn")) {
                const bookingId = event.target.getAttribute("data-booking-id");
                updateBookingStatus(bookingId, "Rejected");
            }
        });
    }

    // Function to handle waitlist actions
    function setupWaitlistActions() {
        document.body.addEventListener("click", function (event) {
            if (event.target.classList.contains("manage-waitlist")) {
                alert("Waitlist management feature is not implemented yet.");
            }
        });
    }

    // Function to delete notifications
    function setupNotificationActions() {
        document.body.addEventListener("click", function (event) {
            if (event.target.classList.contains("delete-notification")) {
                const notificationId = event.target.getAttribute("data-notification-id");

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
                        location.reload();
                    } else {
                        alert("Failed to delete notification.");
                    }
                })
                .catch(error => console.error("Error:", error));
            }
        });
    }

    // // Attach event listeners for Approve/Reject buttons
    // document.body.addEventListener("click", function (event) {
    //     if (event.target.classList.contains("approve-btn")) {
    //         const bookingId = event.target.getAttribute("data-booking-id");
    //         updateBookingStatus(bookingId, "Approved");
    //     } 
    //     else if (event.target.classList.contains("reject-btn")) {
    //         const bookingId = event.target.getAttribute("data-booking-id");
    //         updateBookingStatus(bookingId, "Rejected");
    //     }
    // });

    // Initialize all actions
    setupBookingActions();
    setupWaitlistActions();
    setupNotificationActions();

    // Helper function to get CSRF token from the hidden input field
    function getCSRFToken() {
        return document.querySelector("input[name='csrfmiddlewaretoken']")?.value;
    }
});
