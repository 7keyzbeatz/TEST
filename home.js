let energyType = "electric";
let billMode = "clear";
let autoFilledA = false;
let autoFilledB = false;

const root = document.documentElement;

function updateTheme() {
    root.style.setProperty("--accent", energyType === "electric" ? "#ff3b3b" : "#2196f3");
    document.querySelectorAll(".auto-badge").forEach(b => {
        b.className = "auto-badge " + (energyType === "electric" ? "electric" : "gas");
    });
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

function round2(n) {
    return Math.round(n * 100) / 100;
}

function setAutoField(id, value, badgeId, isAuto) {
    const el = document.getElementById(id);
    const badge = document.getElementById(badgeId);
    if (isAuto) {
        el.value = value !== null && value !== "" ? value : "";
        el.classList.add("auto-filled");
        el.readOnly = true;
        if (badge) badge.style.display = "";
    } else {
        el.value = "";
        el.classList.remove("auto-filled");
        el.readOnly = false;
        if (badge) badge.style.display = "none";
    }
}

function clearAutoA() {
    autoFilledA = false;
    setAutoField("initialA", "", "badgeInitialA", false);
    setAutoField("finalA", "", "badgeFinalA", false);
}

function clearAutoB() {
    autoFilledB = false;
    setAutoField("initialB", "", "badgeInitialB", false);
    setAutoField("finalB", "", "badgeFinalB", false);
}

function tryAutoFill() {
    const totalUnits = parseFloat(document.getElementById("totalUnits").value);
    const initialA = parseFloat(document.getElementById("initialA").value);
    const finalA = parseFloat(document.getElementById("finalA").value);
    const initialB = parseFloat(document.getElementById("initialB").value);
    const finalB = parseFloat(document.getElementById("finalB").value);

    const hasTotalUnits = !isNaN(totalUnits) && totalUnits > 0;
    if (!hasTotalUnits) return;

    const hasA = !isNaN(initialA) && !isNaN(finalA) && !autoFilledA;
    const hasB = !isNaN(initialB) && !isNaN(finalB) && !autoFilledB;

    if (hasA && !hasB) {
        const consA = finalA - initialA;
        const consB = round2(totalUnits - consA);
        if (consB >= 0) {
            autoFilledB = true;
            setAutoField("initialB", 0, "badgeInitialB", true);
            setAutoField("finalB", consB, "badgeFinalB", true);
        }
    } else if (hasB && !hasA) {
        const consB = finalB - initialB;
        const consA = round2(totalUnits - consB);
        if (consA >= 0) {
            autoFilledA = true;
            setAutoField("initialA", 0, "badgeInitialA", true);
            setAutoField("finalA", consA, "badgeFinalA", true);
        }
    }
}

// Ενοικιαστής input → reset auto B, ξαναυπολόγισε
["initialA", "finalA"].forEach(id => {
    document.getElementById(id).addEventListener("input", () => {
        if (autoFilledB) clearAutoB();
        autoFilledA = false;
        tryAutoFill();
    });
});

// Ιδιοκτήτης input → reset auto A, ξαναυπολόγισε
["initialB", "finalB"].forEach(id => {
    document.getElementById(id).addEventListener("input", () => {
        if (autoFilledA) clearAutoA();
        autoFilledB = false;
        tryAutoFill();
    });
});

// Αλλαγή totalUnits → reset τα πάντα και ξαναυπολόγισε
document.getElementById("totalUnits").addEventListener("input", () => {
    if (autoFilledA) clearAutoA();
    if (autoFilledB) clearAutoB();
    tryAutoFill();
});

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
        alert("Λάθος μετρήσεις. Η τελική πρέπει να είναι μεγαλύτερη από την αρχική.");
        return;
    }

    let payA, payB, info;

    if (billMode === "clear") {
        if (isNaN(totalUnits) || totalUnits <= 0) {
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
