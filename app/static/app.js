async function loadDashboardStats() {
    try {
        const response = await fetch("/api/stats");

        if (!response.ok) {
            throw new Error("Unable to load dashboard statistics");
        }

        const data = await response.json();

        console.log("Footprint Flux stats loaded:", data);

        const observationCount =
            document.getElementById("observationCount");

        const sourceCount =
            document.getElementById("sourceCount");

        const changeCount =
            document.getElementById("changeCount");

        const exposureScore =
            document.getElementById("exposureScore");

        if (observationCount) {
            observationCount.textContent = data.observations;
        }

        if (sourceCount) {
            sourceCount.textContent = data.sources;
        }

        if (changeCount) {
            changeCount.textContent = data.changes;
        }

        if (exposureScore) {
            exposureScore.textContent = "—";
        }

    } catch (error) {
        console.error(
            "Dashboard statistics error:",
            error
        );
    }
}


if (document.readyState === "loading") {
    document.addEventListener(
        "DOMContentLoaded",
        loadDashboardStats
    );
} else {
    loadDashboardStats();
}