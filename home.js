let energyType = "electric";
let billMode = "clear";

const root = document.documentElement;

const totalUnitsInput = document.getElementById("totalUnits");
const initialAInput = document.getElementById("initialA");
const finalAInput = document.getElementById("finalA");
const initialBInput = document.getElementById("initialB");
const finalBInput = document.getElementById("finalB");

function updateTheme() {
    if (energyType === "electric") {
        root.style.setProperty("--accent", "#ff3b3b");
    } else {
        root.style.setProperty("--accent", "#2196f3");
    }
}

function updateLabels() {

    const unit = energyType === "electric" ? "kWh" : "m³";

    document.getElementById("totalUnitsLabel").textContent =
        `Συνολική Κατανάλωση (${unit})`;

    document.getElementById("initialALabel").textContent =
        `Αρχική Μέτρηση (${unit})`;

    document.getElementById("finalALabel").textContent =
        `Τελική Μέτρηση (${unit})`;

    document.getElementById("initialBLabel").textContent =
        `Αρχική Μέτρηση (${unit})`;

    document.getElementById("finalBLabel").textContent =
        `Τελική Μέτρηση (${unit})";
}

document.querySelectorAll("#energyType button").forEach(btn => {

    btn.addEventListener("click", () => {

        if (btn.classList.contains("active"))
            return;

        document.querySelectorAll("#energyType button")
            .forEach(b => b.classList.remove("active"));

        btn.classList.add("active");

        energyType = btn.dataset.type;

        updateTheme();
        updateLabels();
    });

});

document.querySelectorAll("#billType button").forEach(btn => {

    btn.addEventListener("click", () => {

        document.querySelectorAll("#billType button")
            .forEach(b => b.classList.remove("active"));

        btn.classList.add("active");

        billMode = btn.dataset.mode;
    });

});

function round2(n) {
    return Math.round(n * 100) / 100;
}

/* AUTO TOTAL CALCULATE */

function autoTotal(){

    const a1 = parseFloat(initialAInput.value);
    const a2 = parseFloat(finalAInput.value);
    const b1 = parseFloat(initialBInput.value);
    const b2 = parseFloat(finalBInput.value);

    if([a1,a2,b1,b2].some(isNaN))
        return;

    const consA = a2 - a1;
    const consB = b2 - b1;

    if(consA >= 0 && consB >= 0){

        const total = consA + consB;

        if(!isNaN(total) && total > 0){
            totalUnitsInput.value = round2(total);
        }
    }
}

initialAInput.addEventListener("input",autoTotal);
finalAInput.addEventListener("input",autoTotal);
initialBInput.addEventListener("input",autoTotal);
finalBInput.addEventListener("input",autoTotal);

document.getElementById("calculateBtn")
.addEventListener("click", () => {

    const totalBill =
        parseFloat(document.getElementById("totalBill").value);

    const totalUnits =
        parseFloat(totalUnitsInput.value);

    const initialA =
        parseFloat(initialAInput.value);

    const finalA =
        parseFloat(finalAInput.value);

    const initialB =
        parseFloat(initialBInput.value);

    const finalB =
        parseFloat(finalBInput.value);

    if([totalBill,initialA,finalA,initialB,finalB]
        .some(isNaN)){

        alert("Συμπλήρωσε όλα τα πεδία.");
        return;
    }

    const consumptionA = finalA - initialA;
    const consumptionB = finalB - initialB;

    if(consumptionA < 0 || consumptionB < 0){

        alert("Λάθος μετρήσεις.");
        return;
    }

    const totalReal =
        consumptionA + consumptionB;

    let payA;
    let payB;
    let info;

    if(billMode === "clear"){

        let units = totalUnits;

        /* fallback αν δεν υπάρχει totalUnits */

        if(isNaN(units) || units <= 0){

            units = totalReal;

            totalUnitsInput.value =
                round2(totalReal);
        }

        if(units <= 0){

            alert("Λάθος κατανάλωση.");
            return;
        }

        const unitPrice =
            totalBill / units;

        payA =
            round2(consumptionA * unitPrice);

        payB =
            round2(consumptionB * unitPrice);

        info =
            `Τιμή μονάδας: ${round2(unitPrice)} €`;

    }
    else{

        if(totalReal <= 0){

            alert("Μηδενική κατανάλωση.");
            return;
        }

        const percentA =
            consumptionA / totalReal;

        const percentB =
            consumptionB / totalReal;

        payA =
            round2(totalBill * percentA);

        payB =
            round2(totalBill * percentB);

        info =
            "Αναλογικός διαμοιρασμός (Έναντι)";
    }

    const params =
        new URLSearchParams({

            energyType,
            billMode,

            consumptionA,
            consumptionB,

            payA,
            payB,

            info
        });

    window.location.href =
        "result.html?" +
        params.toString();

});
