#!/bin/bash

CAESAR_KEY=7
SUBST_KEY='HIDEMEWELL'

PAYLOAD='HELLO, MY FRIEND! STAY AWHILE AND LISTEN! SOOOME LOOOONG STRIIING CHAAAAAIN.'

echo ""

print_test_data() {
    echo "Method| ${1}"
    echo "Key| ${2}"
    echo "Text| ${3}"
    echo "Encrypted| ${4}"
    echo "Decrypted| ${5}"
    echo ""
}

ENCODED_PAYLOAD=$(./cryptobase.py -k ${CAESAR_KEY} -m mapping.txt -s caesar_mapped -t encode "${PAYLOAD}")
DECODED_PAYLOAD=$(./cryptobase.py -k ${CAESAR_KEY} -m mapping.txt -s caesar_mapped -t decode "${ENCODED_PAYLOAD}")

print_test_data "Caesar with substitute alphabet" $CAESAR_KEY "${PAYLOAD}" "${ENCODED_PAYLOAD}" "${DECODED_PAYLOAD}" | column -tL  -s "|"

ENCODED_PAYLOAD=$(./cryptobase.py -k ${CAESAR_KEY} -m mapping.txt -s caesar_simple -t encode "${PAYLOAD}")
DECODED_PAYLOAD=$(./cryptobase.py -k ${CAESAR_KEY} -m mapping.txt -s caesar_simple -t decode "${ENCODED_PAYLOAD}")

print_test_data "Caesar basic" $CAESAR_KEY "${PAYLOAD}" "${ENCODED_PAYLOAD}" "${DECODED_PAYLOAD}" | column -tL  -s "|"

ENCODED_PAYLOAD=$(./cryptobase.py -k ${SUBST_KEY} -m mapping.txt -s subst_cfb -t encode "${PAYLOAD}")
DECODED_PAYLOAD=$(./cryptobase.py -k ${SUBST_KEY} -m mapping.txt -s subst_cfb -t decode "${ENCODED_PAYLOAD}")

print_test_data "Modified Vigenere + CFB" $SUBST_KEY "${PAYLOAD}" "${ENCODED_PAYLOAD}" "${DECODED_PAYLOAD}" | column -tL  -s "|"
