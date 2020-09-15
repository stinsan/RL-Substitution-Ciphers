import os
import random

PLAINTEXT_FOLDER = os.path.join(os.getcwd(), 'plaintexts')
CIPHERTEXT_FOLDER = os.path.join(os.getcwd(), 'ciphertexts')
KEY_FOLDER = os.path.join(os.getcwd(), 'keys')


def encode_shift(file_list):
    for f in file_list:
        print('Encoding file by shift cipher: ' + os.path.basename(f))

        plaintext_file = open(f, 'r')
        plaintext = plaintext_file.read()

        shift_key = random.randint(0, 26)

        ciphertext = ""
        # Traverse plaintext.
        for char in plaintext:

            # DO NOT ENCODE NON-ALPHABETIC CHARACTERS.
            if not char.isalpha():
                ciphertext += char
                continue

            # Encrypting uppercase characters.
            if char.isupper():
                ciphertext += chr((ord(char) + shift_key - 65) % 26 + 65)

            # Encrypting lowercase characters.
            else:
                ciphertext += chr((ord(char) + shift_key - 97) % 26 + 97)

        # Save ciphertext and shift key.
        ciphertext_filename = os.path.splitext(os.path.basename(f))[0].replace('plain', 'shift_cipher.txt')
        ciphertext_file = open(os.path.join(CIPHERTEXT_FOLDER, 'shift', ciphertext_filename), 'w')
        ciphertext_file.write(ciphertext)

        key_filename = os.path.splitext(os.path.basename(f))[0].replace('plain', 'shift_key.txt')
        key_file = open(os.path.join(KEY_FOLDER, 'shift', key_filename), 'w')
        key_file.write(str(shift_key))


def encode_substitution(file_list):
    alphabet = list('abcdefghijklmnopqrstuvwxyz')

    for f in file_list:
        print('Encoding file by substitution cipher: ' + os.path.basename(f))

        # Make the substitution key.
        substitution_key = alphabet.copy()
        random.shuffle(substitution_key)
        substitution_key = ''.join(substitution_key)

        mapping = dict(zip(alphabet, substitution_key))  # Mapping from real alphabet to the key.

        plaintext_file = open(f, 'r')
        plaintext = plaintext_file.read()

        ciphertext = ""

        for char in plaintext:

            # DO NOT ENCODE NON-ALPHABETIC CHARACTERS.
            if not char.isalpha():
                ciphertext += char
                continue

            # Encrypting uppercase characters.
            if char.isupper():
                ciphertext += mapping.get(char.lower()).upper()

            # Encrypting lowercase characters.
            else:
                ciphertext += mapping.get(char.lower())

        # Save ciphertext and substitution key.
        ciphertext_filename = os.path.splitext(os.path.basename(f))[0].replace('plain', 'substitution_cipher.txt')
        ciphertext_file = open(os.path.join(CIPHERTEXT_FOLDER, 'substitution', ciphertext_filename), 'w')
        ciphertext_file.write(ciphertext)

        key_filename = os.path.splitext(os.path.basename(f))[0].replace('plain', 'substitution_key.txt')
        key_file = open(os.path.join(KEY_FOLDER, 'substitution', key_filename), 'w')
        key_file.write(substitution_key)


if __name__ == '__main__':
    file_list = [os.path.join(PLAINTEXT_FOLDER, f) for f in os.listdir(PLAINTEXT_FOLDER)]
    encode_shift(file_list)
    encode_substitution(file_list)