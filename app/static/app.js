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

        // Load the exposure score separately.
        const personId = "4869e231-8d64-43d3-b1a5-c1bf9ef0bfb5";

        try {
            const exposureResponse = await fetch(`/exposure/${personId}`);

            if (exposureResponse.ok) {
                const exposure = await exposureResponse.json();

                document.getElementById("exposureScore").textContent =
                    `${exposure.score}/100`;
            }
        } catch (error) {
            console.error("Exposure score error:", error);
        }
    } catch (error) {
        console.error("Dashboard statistics error:", error);
    }
}

async function runGitHubScan() {
    const username = prompt("Enter a GitHub username:");

    if (!username || !username.trim()) {
        return;
    }

    const button = document.querySelector(".scan-button");
    const status = document.getElementById("scanStatus");

    try {
        if (button) {
            button.disabled = true;
            button.textContent = "Scanning...";
        }

        if (status) {
            status.textContent = "Scanning GitHub profile...";
        }

        const response = await fetch(
            `/api/scan/github/${encodeURIComponent(username.trim())}`,
            { method: "POST" }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.detail || result.message || "GitHub scan failed."
            );
        }

        const message =
            `Scan completed successfully!\n\n` +
            `Username: ${result.username}\n` +
            `Observations collected: ${result.observations_collected}`;

        if (status) {
            status.textContent =
                `Scan completed! ${result.observations_collected} observations collected.`;
        }

        alert(message);

        await loadDashboardStats();

    } catch (error) {
        console.error("GitHub scan error:", error);

        if (status) {
            status.textContent = `Scan failed: ${error.message}`;
        }

        alert(`Scan failed: ${error.message}`);

    } finally {
        if (button) {
            button.disabled = false;
            button.textContent = "Run Scan";
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadTimeline();
    loadDashboardStats();

    const scanButton = document.getElementById("runScanButton");

    if (scanButton) {
        scanButton.addEventListener("click", (event) => {
            event.preventDefault();
            runGitHubScan();
        });
    }
});



async function loadTimeline() {
    const activityContainer = document.getElementById("dailyActivity");

    if (!activityContainer) return;

    try {
        const response = await fetch("/timeline/4869e231-8d64-43d3-b1a5-c1bf9ef0bfb5");

        if (!response.ok) {
            throw new Error("Unable to load timeline");
        }

        const data = await response.json();

        if (!Array.isArray(data) || data.length === 0) {
            activityContainer.innerHTML =
                '<p class="empty-state">No timeline data available yet.</p>';
            return;
        }

        activityContainer.innerHTML = data.map(item => {
            const date = new Date(item.timestamp).toLocaleString();
            const label = item.type === "snapshot"
                ? "Footprint snapshot created"
                : `Footprint change: ${item.change_type}`;

            return `
                <div class="activity-item">
                    <strong>${label}</strong>
                    <small>${date}</small>
                </div>
            `;
        }).join("");
    } catch (error) {
        console.error("Timeline loading error:", error);
        activityContainer.innerHTML =
            '<p class="empty-state">Unable to load timeline.</p>';
    }
}