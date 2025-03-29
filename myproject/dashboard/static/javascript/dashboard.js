// this file helps in fetching and showing real-time updates dynamically.
// created using ajax:
// - Asynchronous Javascript and XML 
// - allows webpages to communicate with a web server asynchronously.
// - it can send and recieve data without interfering with the usr's interaction on the page.

document.addEventListener("DOMContentLoaded", function () {
    function fetchUpdates() {
        fetch("/api/dashboard-updates/")
            .then(response => response.json())
            .then(data => {
                updateEquipmentList(data.equipment);
                updateFacilityList(data.facilities);
                updateNotifications(data.notifications);
            })
            .catch(error => console.error("Error fetching updates:", error));
    }

    function updateEquipmentList(equipment) {
        const equipmentList = document.getElementById("equipment-list");
        equipmentList.innerHTML = "";
        equipment.forEach(item => {
            equipmentList.innerHTML += `
                <li class="p-2 border-b flex justify-between">
                    ${item.name} (${item.quantity} available)
                    <a href="/book_equipment/${item.id}" class="bg-blue-500 text-white px-4 py-1 rounded hover:scale-105">Book</a>
                </li>`;
        });
    }

    // function updateFacilityList(facilities) {
    //     const facilityList = document.getElementById("facility-list");
    //     facilityList.innerHTML = "";
    //     facilities.forEach(item => {
    //         facilityList.innerHTML += `
    //             <li class="p-2 border-b flex justify-between">
    //                 ${item.name} (${item.location})
    //                 <a href="/request_facility/${item.id}" class="bg-green-500 text-white px-4 py-1 rounded hover:scale-105">Request</a>
    //             </li>`;
    //     });
    // }

    function updateNotifications(notifications) {
        const notificationList = document.getElementById("notification-list");
        notificationList.innerHTML = "";
        notifications.forEach(notification => {
            notificationList.innerHTML += `<li class="p-2 border-b">${notification.message}</li>`;
        });
    }

    setInterval(fetchUpdates, 5000); // Refresh every 5 seconds
});
