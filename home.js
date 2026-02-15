let energyType = "electric";
let billMode = "clear";

const root = document.documentElement;

function updateTheme() {
    if (energyType === "electric") {
        root.style.setProperty("--accent", "#ff3b3b");
    } else {
        root.style.setProperty("--accent", "#2196f3");
    }
}

function updateLabels() {
    const unit = energyType === "electric" ? "kWh" : "m³";
    document.getElementById("totalUnitsLabel").textContent = `Συνολική Κατανάλωση (${unit})`;
    document.getElementById("initialALabel").textContent = `Αρχική Μέτρηση (${unit})`;
    document.getElementById("finalALabel").textContent = `Τελική Μέτρηση (${unit})`;
    document.getElementById("initialBLabel").textContent = `Αρχική Μέτρηση (${unit})`;
    document.getElementById("finalBLabel").textContent = `Τελική Μέτρηση (${unit})`;
}

document.querySelectorAll("#energyType button").forEach(btn => {
    btn.addEventListener("click", () => {
        if (btn.classList.contains("active")) return;
        document.querySelectorAll("#energyType button").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        energyType = btn.dataset.type;
        updateTheme();
        updateLabels();
    });
});

document.querySelectorAll("#billType button").forEach(btn => {
    btn.addEventListener("click", () => {
        document.querySelectorAll("#billType button").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        billMode = btn.dataset.mode;
    });
});

function round2(n) { return Math.round(n * 100) / 100; }

document.getElementById("calculateBtn").addEventListener("click", () => {

    const totalBill = parseFloat(document.getElementById("totalBill").value);
    const totalUnits = parseFloat(document.getElementById("totalUnits").value);
    const initialA = parseFloat(document.getElementById("initialA").value);
    const finalA = parseFloat(document.getElementById("finalA").value);
    const initialB = parseFloat(document.getElementById("initialB").value);
    const finalB = parseFloat(document.getElementById("finalB").value);

    if ([totalBill, initialA, finalA, initialB, finalB].some(isNaN)) {
        alert("Συμπλήρωσε όλα τα πεδία.");
        return;
    }

    const consumptionA = finalA - initialA;
    const consumptionB = finalB - initialB;
    const totalReal = consumptionA + consumptionB;

    if (consumptionA < 0 || consumptionB < 0) {
        alert("Λάθος μετρήσεις.");
        return;
    }

    let payA, payB, info;

    if (billMode === "clear") {

        if (isNaN(totalUnits)) {
            alert("Συμπλήρωσε συνολική κατανάλωση.");
            return;
        }

        const unitPrice = totalBill / totalUnits;
        payA = round2(consumptionA * unitPrice);
        payB = round2(consumptionB * unitPrice);
        info = `Τιμή μονάδας: ${round2(unitPrice)} €`;

    } else {

        const percentA = consumptionA / totalReal;
        const percentB = consumptionB / totalReal;

        payA = round2(totalBill * percentA);
        payB = round2(totalBill * percentB);
        info = "Αναλογικός διαμοιρασμός (Έναντι)";
    }

    const params = new URLSearchParams({
        energyType,
        billMode,
        consumptionA,
        consumptionB,
        payA,
        payB,
        info
    });

    window.location.href = "result.html?" + params.toString();

});