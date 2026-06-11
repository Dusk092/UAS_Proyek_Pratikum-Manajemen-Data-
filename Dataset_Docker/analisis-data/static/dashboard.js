const bulanLabels = JSON.parse(
    document.getElementById("bulanLabels").textContent
);

const bulanData = JSON.parse(
    document.getElementById("bulanData").textContent
);

new Chart(
    document.getElementById("barChart"),
    {
        type: "bar",

        data: {
            labels: bulanLabels,

            datasets: [{
                label: "Pengeluaran",
                data: bulanData,
                backgroundColor: "#2952d5"
            }]
        }
    }
);

const kategoriLabels = JSON.parse(
    document.getElementById("kategoriLabels").textContent
);

const kategoriData = JSON.parse(
    document.getElementById("kategoriData").textContent
);

new Chart(
    document.getElementById("pieChart"),
    {
        type: "doughnut",

        data: {
            labels: kategoriLabels,

            datasets: [{
                data: kategoriData,

                backgroundColor: [
                    "#3b82f6",
                    "#ef4444",
                    "#f59e0b",
                    "#10b981",
                    "#8b5cf6",
                    "#ec4899",
                    "#06b6d4",
                    "#84cc16",
                    "#f97316",
                    "#14b8a6"
                ]
            }]
        }
    }
);

const themeSelect =
    document.getElementById("themeSelect");

if (themeSelect) {

    const savedTheme =
        localStorage.getItem("theme");

    if (savedTheme) {
        document.body.className = savedTheme;
        themeSelect.value = savedTheme;
    }

    themeSelect.addEventListener(
        "change",
        function () {

            document.body.className =
                this.value;

            localStorage.setItem(
                "theme",
                this.value
            );

        }
    );
}

function showNotification(text) {

    let notif =
        document.createElement("div");

    notif.className =
        "notification";

    notif.innerHTML =
        text;

    document
        .getElementById("notifBox")
        .appendChild(notif);

    setTimeout(() => {
        notif.remove();
    }, 5000);
}

function saveSettings() {

    showNotification(
        "Pengaturan berhasil disimpan"
    );

}
