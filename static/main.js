// XOR two messages
async function xorMessages() {
    const msg1 = document.getElementById("msg1").value;
    const msg2 = document.getElementById("msg2").value;

    if (msg1.length !== msg2.length) {
        alert("Messages must be the same length.");
        return;
    }

    try {
        const resp = await fetch("/api/xor_messages", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ msg1, msg2 })
        });
        const j = await resp.json();
        if (j.error) {
            alert(j.error);
            return;
        }
        document.getElementById("xorOutput").value = j.xor_bin;
    } catch (err) {
        console.error(err);
        alert("Error computing XOR");
    }
}

// decode XOR using known message
async function decodeXor() {
    const xor_bin = document.getElementById("xorInput").value.trim();
    const known_msg = document.getElementById("knownMsg").value;

    if (!xor_bin || !known_msg) {
        alert("Please enter both XOR binary and the known message");
        return;
    }

    try {
        const resp = await fetch("/api/decode_xor", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ xor_bin, known_msg })
        });
        const j = await resp.json();
        if (j.error) {
            alert(j.error);
            return;
        }
        document.getElementById("decodedOutput").value = j.recovered;
    } catch (err) {
        console.error(err);
        alert("Error decoding XOR");
    }
}

// decode baudot
async function decodeBaudot() {
    const fragment = document.getElementById("baudotInput").value.trim();
    if (!fragment) {
        alert("Enter Baudot 5-bit codes separated by spaces");
        return;
    }

    try {
        const resp = await fetch("/decode", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ data: fragment })
        });
        const result = await resp.json();
        document.getElementById("plaintextOutput").value = result.plaintext;
    } catch (err) {
        console.error(err);
        document.getElementById("plaintextOutput").value = "Error decoding";
    }
}

// event listeners
document.getElementById("computeXor").addEventListener("click", xorMessages);
document.getElementById("decodeXorBtn").addEventListener("click", decodeXor);
document.getElementById("baudotBtn").addEventListener("click", decodeBaudot);
