// ---------------- XOR Two Messages ----------------
function xorMessages() {
    const msg1 = document.getElementById("msg1").value;
    const msg2 = document.getElementById("msg2").value;

    if (msg1.length !== msg2.length) {
        alert("Messages must be the same length.");
        return;
    }

    let xorResult = "";
    for (let i = 0; i < msg1.length; i++) {
        const xorChar = msg1.charCodeAt(i) ^ msg2.charCodeAt(i);
        xorResult += xorChar.toString(2).padStart(8, "0");
    }

    document.getElementById("xorOutput").value = xorResult;
}

// ---------------- Decode XOR using Known Message ----------------
function decodeXor() {
    const xor_bin = document.getElementById("xorInput").value.trim();
    const known_msg = document.getElementById("knownMsg").value;

    if (xor_bin.length !== known_msg.length * 8) {
        alert("Length mismatch: XOR binary and known message must match.");
        return;
    }

    let recovered = "";
    for (let i = 0; i < known_msg.length; i++) {
        const byteStr = xor_bin.slice(i * 8, i * 8 + 8);
        const byteVal = parseInt(byteStr, 2);
        recovered += String.fromCharCode(byteVal ^ known_msg.charCodeAt(i));
    }

    document.getElementById("decodedOutput").value = recovered;
}

// ---------------- Baudot Decoder ----------------
const BAUDOT_LETTERS = {
    "00000": "A","00001": "B","00010": "C","00011": "D","00100": "E",
    "00101": "F","00110": "G","00111": "H","01000": "I","01001": "J",
    "01010": "K","01011": "L","01100": "M","01101": "N","01110": "O",
    "01111": "P","10000": "Q","10001": "R","10010": "S","10011": "T",
    "10100": "U","10101": "V","10110": "W","10111": "X","11000": "Y",
    "11001": "Z","11010": " ","11011": ".","11100": ",","11101": "?",
    "11110": "'","11111": "<SH>"
};

function decodeBaudot() {
    const input = document.getElementById("baudotInput").value.trim();
    const groups = input.split(/\s+/);
    let decoded = "";

    groups.forEach(g => {
        if (BAUDOT_LETTERS[g]) {
            decoded += BAUDOT_LETTERS[g];
        } else {
            decoded += "?";
        }
    });

    document.getElementById("plaintextOutput").value = decoded;
}

// ---------------- Event Listeners ----------------
document.getElementById("computeXor").addEventListener("click", xorMessages);
document.getElementById("decodeXorBtn").addEventListener("click", decodeXor);
document.getElementById("baudotBtn").addEventListener("click", decodeBaudot);
