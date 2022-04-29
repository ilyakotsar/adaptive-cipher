import random
import string
import tkinter as tk


addition = "_.,?!-+*/%():;'" + '"' + string.digits
en_letters = ''
for i, j in zip(string.ascii_uppercase, string.ascii_lowercase):
    en_letters += i + j

EN = en_letters + addition
RU = 'АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя' + addition


def encrypt():
    try:
        if langs.get() == 0:
            alphabet = EN
        else:
            alphabet = RU
        plaintext = ''
        for i in text_pt.get('1.0', 'end-1c'):
            if i == ' ':
                plaintext += '_'
            else:
                plaintext += i
        keyword = text_kw.get('1.0', 'end-1c')
        if len(keyword) == 0:
            return False
        elif len(plaintext) == 0:
            return False
        else:
            kw_strength = round(len(keyword) / len(plaintext) * 100, 1)
            keyword = expand_keyword(keyword, plaintext)
            alphabet = shift_alphabet(alphabet, keyword)
            ciphertext = ''
            for i in range(len(plaintext)):
                x = caesar_encrypt(alphabet, alphabet.index(plaintext[i]), alphabet)
                ciphertext += x[alphabet.index(keyword[i])]
            text_ct.delete('1.0', tk.END)
            text_ct.insert('1.0', ciphertext)
            label_new_alpha['text'] = '\nAdapted alphabet: ' + alphabet
            ch_distr = frequency_analysis(keyword, alphabet)
            label_ch_distr['text'] = f'Distribution of keyword characters: {ch_distr}%'
            label_kw_strength['text'] = f'Keyword strength: {kw_strength}%'
    except ValueError:
        return False


def decrypt():
    try:
        if langs.get() == 0:
            alphabet = EN
        else:
            alphabet = RU
        ciphertext = text_ct.get('1.0', 'end-1c')
        keyword = text_kw.get('1.0', 'end-1c')
        if len(keyword) == 0:
            return False
        elif len(ciphertext) == 0:
            return False
        else:
            kw_strength = round(len(keyword) / len(ciphertext) * 100, 1)
            keyword = expand_keyword(keyword, ciphertext)
            alphabet = shift_alphabet(alphabet, keyword)
            plaintext = ''
            for i in range(len(ciphertext)):
                x = caesar_encrypt(alphabet, alphabet.index(keyword[i]), alphabet)
                plaintext += alphabet[x.index(ciphertext[i])]
            text_pt.delete('1.0', tk.END)
            text_pt.insert('1.0', plaintext)
            label_new_alpha['text'] = '\nAdapted alphabet: ' + alphabet
            ch_distr = frequency_analysis(keyword, alphabet)
            label_ch_distr['text'] = f'Distribution of keyword characters: {ch_distr}%'
            label_kw_strength['text'] = f'Keyword strength: {kw_strength}%'
    except ValueError:
        return False


def generate_keyword():
    if langs.get() == 0:
        alphabet = EN
    else:
        alphabet = RU
    plaintext = text_pt.get('1.0', 'end-1c')
    if len(plaintext) > 0:
        while True:
            keyword = ''
            for i in range(len(plaintext)):
                while True:
                    letter = alphabet[random.randint(0, len(alphabet) - 1)]
                    if i > 0:
                        if letter != keyword[i - 1]:
                            keyword += letter
                            break
                        else:
                            continue
                    else:
                        keyword += letter
                        break
            if frequency_analysis(keyword, alphabet) < 50:
                continue
            else:
                break
        text_kw.delete('1.0', tk.END)
        text_kw.insert('1.0', keyword)
        ch_distr = frequency_analysis(keyword, alphabet)
        label_ch_distr['text'] = f'Distribution of keyword characters: {ch_distr}%'
        kw_strength = round(len(keyword) / len(plaintext) * 100, 1)
        label_kw_strength['text'] = f'Keyword strength: {kw_strength}%'
    else:
        return False


def shift_alphabet(alphabet, keyword):
    for i in range(len(keyword)):
        shift = alphabet.index(keyword[i])
        alphabet = caesar_encrypt(alphabet, shift, alphabet)
        if shift > 1:
            alphabet = rail_fence_encrypt(alphabet, shift)
            a = alphabet[shift - 1] + alphabet[shift]
            b = alphabet[shift] + alphabet[shift - 1]
            pair = str.maketrans(a, b)
            alphabet = alphabet.translate(pair)
    return alphabet


def caesar_core(letter, shift, alphabet):
    for i in range(len(alphabet)):
        if alphabet[i] == letter:
            a = i + shift
            b = a % len(alphabet)
            return alphabet[b]


def caesar_encrypt(plaintext, shift, alphabet):
    ciphertext = ''
    for i in range(len(plaintext)):
        ciphertext += caesar_core(plaintext[i], shift, alphabet)
    return ciphertext


def rail_fence_encrypt(plaintext, key):
    fence = [[None] * len(plaintext) for _ in range(key)]
    rails = list(range(key - 1)) + list(range(key - 1, 0, -1))
    for key, x in enumerate(plaintext):
        fence[rails[key % len(rails)]][key] = x
    ciphertext = ''.join([c for rail in fence for c in rail if c is not None])
    return ciphertext


def expand_keyword(keyword, text):
    exp_keyword = ''
    while len(exp_keyword) <= len(text):
        exp_keyword += keyword
    return exp_keyword[:len(text)]


def frequency_analysis(keyword, alphabet):
    if len(keyword) == 0:
        return 1
    elif len(keyword) <= len(alphabet):
        value = [(1 / keyword.count(i) * 100) for i in alphabet if keyword.count(i) != 0]
        return round(sum(value) / len(keyword), 1)
    else:
        value = [keyword.count(i) * 100 / len(keyword) for i in alphabet]
        ideal = 100 / len(alphabet)
        diff = []
        for i in value:
            if i < ideal:
                diff.append(i / ideal * 100)
            elif i > ideal:
                diff.append(ideal / i * 100)
            elif i == ideal:
                diff.append(100)
        return round(sum(diff) / len(diff))


window = tk.Tk()
window.geometry('1250x820')
window.title('Adaptive Cipher')

label_ch = tk.Label(text='\nAlphabet')
label_ch.pack()
langs = tk.IntVar()
radio_en = tk.Radiobutton(text=EN, variable=langs, value=0)
radio_ru = tk.Radiobutton(text=RU, variable=langs, value=1)
radio_en.pack()
radio_ru.pack()

label_pt = tk.Label(text='\nPlaintext')
text_pt = tk.Text(width=150, height=7)
label_pt.pack()
text_pt.pack()

label_kw = tk.Label(text='\nKeyword')
text_kw = tk.Text(width=150, height=7)
label_kw.pack()
text_kw.pack()

label_ct = tk.Label(text='\nCiphertext')
text_ct = tk.Text(width=150, height=7)
label_ct.pack()
text_ct.pack()

label_x = tk.Label(text='')
label_x.pack()
btn_encrypt = tk.Button(text='Encrypt', command=encrypt)
btn_encrypt.pack()
btn_decrypt = tk.Button(text='Decrypt', command=decrypt)
btn_decrypt.pack()
btn_generate_kw = tk.Button(text='Generate keyword', command=generate_keyword)
btn_generate_kw.pack()

label_new_alpha = tk.Label(text='\n')
label_new_alpha.pack()
label_ch_distr = tk.Label(text='')
label_ch_distr.pack()
label_kw_strength = tk.Label(text='')
label_kw_strength.pack()
label_copyright = tk.Label(text='\n© Ilya Kotsar https://github.com/ilyakotsar')
label_copyright.pack()

window.mainloop()

# © Ilya Kotsar https://github.com/ilyakotsar
