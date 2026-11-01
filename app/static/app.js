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
    loadExposureAnalysis();

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

    const personId = "4869e231-8d64-43d3-b1a5-c1bf9ef0bfb5";

    try {
        activityContainer.innerHTML =
            '<p class="empty-state">Loading footprint activity...</p>';

        const response = await fetch(`/timeline/${personId}?limit=50&offset=0`);

        if (!response.ok) {
            throw new Error(`Timeline request failed: ${response.status}`);
        }

        const data = await response.json();

        if (!Array.isArray(data) || data.length === 0) {
            activityContainer.innerHTML =
                '<p class="empty-state">No timeline data available yet.</p>';
            return;
        }

        activityContainer.innerHTML = data
            .slice()
            .reverse()
            .map(item => {
                const date = new Date(item.timestamp).toLocaleString();

                const type = item.type === "snapshot"
                    ? "snapshot"
                    : (item.change_type || "modified").toLowerCase();

                const label = type === "snapshot"
                    ? "Footprint snapshot created"
                    : `Footprint ${type} — ${item.new_value ?? "Unknown"} → ${item.old_value ?? "Unknown"}`;

                return `
                    <div class="activity-item ${type}">
                        <strong>${label}</strong>
                        <small>${date}</small>
                    </div>
               `;
            })
            .join("");
    } catch (error) {
        console.error("Timeline loading error:", error);

        activityContainer.innerHTML =
            '<p class="empty-state">Unable to load timeline data.</p>';
    }
}



async function loadExposureAnalysis() {
    const personId = "4869e231-8d64-43d3-b1a5-c1bf9ef0bfb5";

    const scoreElement = document.getElementById("analysisScore");
    const badgeElement = document.getElementById("riskBadge");
    const descriptionElement = document.getElementById("riskDescription");
    const factorsElement = document.getElementById("exposureFactors");
    const recommendationsElement = document.getElementById("privacyRecommendations");

    try {
        const [exposureResponse, recommendationsResponse] =
            await Promise.all([
                fetch(`/exposure/${personId}`),
                fetch(`/recommendations/${personId}`)
            ]);

        if (!exposureResponse.ok || !recommendationsResponse.ok) {
            throw new Error("Unable to load exposure analysis.");
        }

        const exposure = await exposureResponse.json();
        const recommendationData = await recommendationsResponse.json();

        scoreElement.textContent = `${exposure.score}/100`;

        const risk = exposure.risk_level.toLowerCase();

        badgeElement.textContent = risk.toUpperCase();
        badgeElement.className = `risk-badge ${risk}`;

        descriptionElement.textContent =
            risk === "high"
                ? "Your public digital footprint has significant exposure. Review the factors below."
                : risk === "medium"
                    ? "Your digital footprint has moderate exposure. Some privacy improvements are recommended."
                    : "Your digital footprint currently has relatively low exposure.";

        factorsElement.innerHTML = exposure.factors.map(item => `
            <div class="factor-item">
                <span>${item.factor}</span>
                <strong>${item.points} pts</strong>
            </div>
        `).join("");

        recommendationsElement.innerHTML =
            recommendationData.recommendations.map(item => `
                <div class="recommendation-item">
                    <span>✓</span>
                    <p>${item}</p>
                </div>
            `).join("");

    } catch (error) {
        console.error("Exposure analysis error:", error);

        badgeElement.textContent = "Unavailable";
        descriptionElement.textContent =
            "Unable to load exposure analysis. Check the API response.";
    }
}