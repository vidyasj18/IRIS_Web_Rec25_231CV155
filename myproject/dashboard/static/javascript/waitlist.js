// This helps in displaying ones waitlist status and what position they are in the waitlist.
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        let cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrfToken = getCookie("csrftoken");

function joinWaitlist(equipmentId) {
    if (!csrfToken) {
        console.error("CSRF token not found.");
        return;
    }
    
    fetch(`waitlist-booking/${equipmentId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        let waitlistStatus = document.getElementById(`waitlist-status-${equipmentId}`);
        if (!waitlistStatus) {
            console.error(`Element with ID waitlist-status-${equipmentId} not found.`);
            return;
        }
        if (data.waitlisted) {
            waitlistStatus.innerText = `You are on the waitlist. Your position: ${data.position}`;
        } else {
            waitlistStatus.innerText = "Slots are available, no waitlist needed!";
        }
    })
    .catch(error => {
        console.error('Error:', error);
        let waitlistStatus = document.getElementById(`waitlist-status-${equipmentId}`);
        if (waitlistStatus) {
            waitlistStatus.innerHTML = `<span class="text-red-500">Failed to join waitlist. Try again later.</span>`;
        }
    });
}
