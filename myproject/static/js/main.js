async function bookInfrastructure(infrastructureId) {
    try {
        const response = await fetch('/api/bookings/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}` // Ensure token is stored after login
            },
            body: JSON.stringify({
                infrastructure: infrastructureId,
                start_time: new Date().toISOString() // You can modify this to select a time
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            alert('Booking successful!');
            location.reload(); // Reload to reflect changes
        } else {
            alert(data.error || 'Booking failed.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong.');
    }
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".book-equipment-btn").forEach(button => {
        button.addEventListener("click", function () {
            const infrastructureId = this.getAttribute("data-id");
            bookInfrastructure(infrastructureId);
        });
    });
});
