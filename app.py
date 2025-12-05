from flask import Flask, render_template, request, jsonify

# import your Baudot helper functions and tables
from baudot import (
    text_to_baudot_symbols,
    baudot_symbols_to_text,
    symbols_to_bits,
    bits_to_symbols,
    xor_bitstreams,
    BAUDOT_LETTERS, 
    BAUDOT_FIGURES,
    REVERSE_LETTERS,
    score_english
)

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")


# XOR two messages
@app.route("/api/xor_messages", methods=["POST"])
def xor_messages():
    data = request.get_json()
    msg1 = data.get("msg1", "")
    msg2 = data.get("msg2", "")

    # pad the shorter message with spaces
    max_len = max(len(msg1), len(msg2))
    msg1 = msg1.ljust(max_len)
    msg2 = msg2.ljust(max_len)

    # XOR each byte
    xor_result = bytes([b1 ^ b2 for b1, b2 in zip(msg1.encode(), msg2.encode())])

    # convert to binary string
    xor_bin = ''.join(f"{b:08b}" for b in xor_result)

    return jsonify({"xor_bin": xor_bin})

# decode XOR using known message 
@app.route("/api/decode_xor", methods=["POST"])
def decode_xor():
    data = request.get_json()
    xor_bin = data.get("xor_bin", "").replace(" ", "").replace("\n", "")
    known_msg = data.get("known_msg", "")

    if len(xor_bin) % 8 != 0:
        return jsonify({"error": "XOR binary length must be a multiple of 8"}), 400

    # convert binary string to bytes
    xor_bytes_val = bytes(int(xor_bin[i:i+8], 2) for i in range(0, len(xor_bin), 8))

    # pad known message if necessary
    if len(known_msg.encode()) < len(xor_bytes_val):
        known_msg = known_msg.ljust(len(xor_bytes_val))

    recovered = bytes([b1 ^ b2 for b1, b2 in zip(xor_bytes_val, known_msg.encode())])

    return jsonify({"recovered": recovered.decode(errors="replace")})

# baudot decode
@app.route("/decode", methods=["POST"])
def decode_baudot():
    data = request.json.get("data", "")
    # split input by spaces
    bit_groups = data.strip().split()
    decoded = []

    for bits in bit_groups:
        # convert 5-bit string to integer
        try:
            symbol = int(bits, 2)
        except ValueError:
            decoded.append("?")
            continue

        # check in letters first
        if symbol in BAUDOT_LETTERS:
            decoded.append(BAUDOT_LETTERS[symbol])
        # check in figures if needed
        elif bits in BAUDOT_FIGURES:
            decoded.append(BAUDOT_FIGURES[bits])
        else:
            decoded.append("?")

    return jsonify({"plaintext": "".join(decoded)})



if __name__ == "__main__":
    app.run(debug=True)
