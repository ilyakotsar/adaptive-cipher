# Adaptive Cipher

Symmetric text encryption with unique vigenere table generation. Python (Tkinter)

![image](https://github.com/ilyakotsar/adaptive-cipher/blob/main/screenshot-encryption.png)

## Installation

- Install Python https://www.python.org/downloads/
- If you are using Linux install Tkinter
```
    sudo apt install python3-tk
```
- Download and run adaptive-cipher.py
```
    python adaptive-cipher.py
    python3 adaptive-cipher.py
```

## Usage

- Select alphabet, you can use any characters (change in code)
- Enter the text you want to encrypt in the plaintext (here you can enter spaces, they will be replaced with _ when decryption)
- Enter a keyword or generate (plaintext length must be greater than zero) and press Encrypt
- Distribution of keyword characters and keyword strength should be as high as possible

This cipher is resistant to frequency analysis, changing one character in the keyword changes the entire text output.


## Vigenere table

The alphabet changes for each character of the keyword according to the algorithm:

- Caesar cipher
- Rail fence cipher
- Transposition cipher for current character and previous
