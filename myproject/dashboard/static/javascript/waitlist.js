// This helps in displaying ones waitlist status and what position they are in the waitlist.
function joinWaitlist(facilityId) {
    fetch(`/dashboard/waitlist/${facilityId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        let waitlistStatus = document.getElementById(`waitlist-status-${facilityId}`);
        if (data.waitlisted) {
            waitlistStatus.innerText = `You are on the waitlist. Your position: ${data.position}`;
        } else {
            waitlistStatus.innerText = "Slots are available, no waitlist needed!";
        }
    })
    .catch(error => console.error('Error:', error));
}
