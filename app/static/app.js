async function loadDashboardStats() {
    try {
        const response = await fetch("/api/stats");

        if (!response.ok) {
            throw new Error("Unable to load dashboard statistics");
        }

        const data = await response.json();

        document.getElementById("observationCount").textContent =
            data.observations ?? 0;

        document.getElementById("sourceCount").textContent =
            data.sources ?? 0;

        document.getElementById("changeCount").textContent =
            data.changes ?? 0;

    } catch (error) {
        console.error("Dashboard statistics error:", error);
    }
}

async function loadExposureScore() {
    try {
        const personId = "4869e231-8d64-43d3-b1a5-c1bf9ef0bfb5";

        const response = await fetch(`/exposure/${personId}`);

        if (!response.ok) {
            throw new Error("Unable to load exposure score");
        }

        const data = await response.json();

        const scoreElement = document.getElementById("exposureScore");

        if (scoreElement) {
            scoreElement.textContent = `${data.score}/100`;
            scoreElement.title = `Risk level: ${data.risk_level}`;
        }

        console.log("Exposure score loaded:", data);

    } catch (error) {
        console.error("Exposure score error:", error);

        const scoreElement = document.getElementById("exposureScore");

        if (scoreElement) {
            scoreElement.textContent = "Unavailable";
        }
    }
}

async function loadDashboard() {
    await Promise.all([
        loadDashboardStats(),
        loadExposureScore()
    ]);
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", loadDashboard);
} else {
    loadDashboard();
}