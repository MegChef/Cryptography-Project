# baudot.py
from typing import Dict, List
import math

# -------------------------
# LETTERS-only 5-bit mapping (toy mapping)
# This maps 0..25 -> 'A'..'Z', and some other codes for space/punct.
# -------------------------
BAUDOT_LETTERS: Dict[int, str] = {i: chr(ord('A') + i) for i in range(26)}
BAUDOT_LETTERS.update({
    26: ' ',
    27: '.',
    28: ',',
    29: '?',
    30: "'",
    31: '<SH>'  # placeholder
})
REVERSE_LETTERS = {v: k for k, v in BAUDOT_LETTERS.items()}
BAUDOT_FIGURES = {
    "00000": "",       # null
    "00001": "3",
    "00010": "\n",     # Line Feed
    "00011": "-",
    "00100": " ",
    "00101": "'",
    "00110": "8",
    "00111": "7",
    "01000": "\r",     # carriage Return
    "01001": "4",
    "01010": "§",      # Bell or "BEL"
    "01011": ",",
    "01100": "!",
    "01101": ":",
    "01110": "(",
    "01111": "5",
    "10000": "+",
    "10001": ")",
    "10010": "2",
    "10011": "$",
    "10100": "6",
    "10101": "0",
    "10110": "1",
    "10111": "9",
    "11000": "?",
    "11001": "&",
    "11010": "/",
    "11011": ";",
    "11100": ".",
    "11101": "FIGS",   # shift to figures
    "11110": "LTRS",   # shift to letters
    "11111": "="
}

# bit / symbol utilities
def text_to_baudot_symbols(text: str, reverse_map: Dict[str, int]) -> List[int]:
    symbols = []
    for ch in text:
        if ch in reverse_map:
            symbols.append(reverse_map[ch])
        else:
            up = ch.upper()
            if up in reverse_map:
                symbols.append(reverse_map[up])
            elif ' ' in reverse_map:
                symbols.append(reverse_map[' '])
            else:
                symbols.append(0)
    return symbols

def baudot_symbols_to_text(symbols: List[int], letter_map: Dict[int, str]) -> str:
    return ''.join(letter_map.get(s, f'[{s:05b}]') for s in symbols)

def symbols_to_bits(symbols: List[int]) -> List[int]:
    bits = []
    for s in symbols:
        for b in range(4, -1, -1):
            bits.append((s >> b) & 1)
    return bits

def bits_to_symbols(bits: List[int]) -> List[int]:
    syms = []
    for i in range(0, len(bits) - 4, 5):
        val = 0
        for b in range(5):
            val = (val << 1) | bits[i + b]
        syms.append(val)
    return syms

def xor_bitstreams(a_bits: List[int], b_bits: List[int]) -> List[int]:
    n = min(len(a_bits), len(b_bits))
    return [a_bits[i] ^ b_bits[i] for i in range(n)]

# Simple English scorer
ENGLISH_UNIGRAM_FREQ = {
    'E': 12.0, 'T': 9.10, 'A': 8.12, 'O': 7.68, 'I': 7.31, 'N': 6.95,
    'S': 6.28, 'R': 6.02, 'H': 5.92, 'L': 4.02, 'D': 3.82, 'C': 3.61,
    'U': 2.88, 'M': 2.61, 'F': 2.30, 'Y': 2.11, 'W': 2.09, 'G': 2.03,
    'P': 1.82, 'B': 1.49, 'V': 1.11, 'K': 0.69, 'X': 0.17, 'Q': 0.11, 'J': 0.10
}

def score_english(text: str) -> float:
    score = 0.0
    for ch in text:
        if ch.isalpha():
            score += math.log(ENGLISH_UNIGRAM_FREQ.get(ch.upper(), 0.01))
        elif ch == ' ':
            score += math.log(0.5)
        else:
            score -= 2.0
    return score
