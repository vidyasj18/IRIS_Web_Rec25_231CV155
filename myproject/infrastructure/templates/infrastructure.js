document.addEventListener("DOMContentLoaded", function () {
    fetchInfrastructure();
});

async function fetchInfrastructure() {
    try {
        const response = await fetch("http://127.0.0.1:8000/api/infrastructure/", {
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("token")}`
            }
        });

        if (!response.ok) {
            throw new Error("Failed to fetch infrastructure data");
        }

        const infrastructures = await response.json();
        displayInfrastructure(infrastructures);
    } catch (error) {
        console.error("Error:", error);
    }
}

function displayInfrastructure(infrastructures) {
    const infrastructureContainer = document.getElementById("infrastructure-list");
    infrastructureContainer.innerHTML = "";

    infrastructures.forEach(infra => {
        const infraElement = document.createElement("div");
        infraElement.classList.add("bg-white", "shadow-md", "rounded-lg", "p-4", "m-2");

        infraElement.innerHTML = `
            <h2 class="text-xl font-bold">${infra.name}</h2>
            <p class="text-gray-600">${infra.description}</p>
            <p class="text-green-500">${infra.availability ? "Available" : "Under Maintenance"}</p>
            ${infra.availability ? `<button onclick="bookInfrastructure(${infra.id})" class="bg-blue-500 text-white px-4 py-2 mt-2 rounded">Book Now</button>` : ""}
        `;

        infrastructureContainer.appendChild(infraElement);
    });
}
