// this file helps in fetching and showing real-time updates dynamically.
// created using ajax:
// - Asynchronous Javascript and XML 
// - allows webpages to communicate with a web server asynchronously.
// - it can send and recieve data without interfering with the usr's interaction on the page.

document.addEventListener("DOMContentLoaded", function () {
    console.log("dashboard.js loaded");
    // helps in fetching updates.
    function fetchUpdates() {
        fetch("/dashboard/api/dashboard-updates/")
            .then(response => response.json())
            .then(data => {
                console.log("API Response:", data);
                updateEquipmentList(data.equipment);
                updateFacilityList(data.facilities);
                updateNotifications(data.notifications);
            })
            .catch(error => console.error("Error fetching updates:", error));
    }

    // updates equipmentlist
    function updateEquipmentList(equipment) {
        const equipmentList = document.getElementById("equipment-list");
        equipmentList.innerHTML = "";
        equipment.forEach(item => {
            equipmentList.innerHTML += `
                <li class="p-2 border-b flex justify-between">
                    ${item.name} (${item.quantity} available)
                    <button onclick="bookEquipment(${item.id})" 
                            class="bg-blue-500 text-white px-4 py-1 rounded hover:scale-105">
                        Book
                    </button>
                </li>`;
        }); 
    }

    function updateFacilityList(facilities) {
        const facilityList = document.getElementById("facility-list");
        facilityList.innerHTML = "";
        facilities.forEach(item => {
            facilityList.innerHTML += `
                <li class="p-2 border-b flex justify-between">
                    ${item.name} (${item.location})
                    <button onclick="bookFacility(${item.id})" 
                            class="bg-blue-500 text-white px-4 py-1 rounded hover:scale-105">
                        Book
                    </button>
                </li>`;
        });
    }

    // updates notifications and related errors.
    function updateNotifications(notifications) {
        const notificationList = document.getElementById("notification-list");
        notificationList.innerHTML = "";
        notifications.forEach(notification => {
            notificationList.innerHTML += `<li class="p-2 border-b">${notification.message}</li>`;
        });
    }

    // helps in booking an equipment.
    // function bookEquipment(equipmentId) {
    //     fetch(`/book_equipment/${equipmentId}/`, {
    //         method: "POST",
    //         headers: {
    //             "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
    //             "Content-Type": "application/json"
    //         }
    //     })
    //     .then(response => response.json())
    //     .then(data => {
    //         if (data.success) {
    //             alert("Booking successful!");
    //             fetchUpdates(); // Refresh equipment list & notifications
    //         } else {
    //             alert(data.error || "Failed to book equipment.");
    //         }
    //     })
    //     .catch(error => console.error("Error:", error));

    // document.querySelectorAll(".book-equipment-btn").forEach(button => {
    //     button.addEventListener("click", function () {
    //         const equipmentId = this.dataset.equipmentId;
    //         console.log(`Book button clicked for Equipment ID: ${equipmentId}`);
    //         bookEquipment(equipmentId);
    //     });
    // });

    function bookEquipment(equipmentId) {
        
        fetch(`/dashboard/book-equipment/${equipmentId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                "Content-Type": "application/json"
            },
        })
        .then(response => response.json())
        .then(data => {

            if (data.success) {
                alert("Booking successful!");
                location.reload();
            } else {
                alert(data.error);
            }
        })
        .catch(error => console.error("Error:", error));
    }

    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("book-equipment-btn")) {
            const equipmentId = event.target.dataset.equipmentId;
            console.log(`Book button clicked for Equipment ID: ${equipmentId}`); // Debugging log
            bookEquipment(equipmentId);
        }
    });

    async function fetchDashboardUpdates() {
        try {
            const response = await fetch('/api/dashboard-updates/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`  // Ensure the user is authenticated
                }
            });
    
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
    
            const data = await response.json();
            console.log('Dashboard Updates:', data);
            // Update your UI with the fetched data
    
        } catch (error) {
            console.error('Error fetching updates:', error);
        }
    }
    
    // Run function when page loads
    document.addEventListener("DOMContentLoaded", fetchDashboardUpdates);
    
    
    setInterval(fetchUpdates, 5000); // Fetch updates every 5 seconds
});

