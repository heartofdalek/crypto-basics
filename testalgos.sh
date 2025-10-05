#!/bin/bash

CAESAR_KEY=7
SUBST_KEY='HIDEMEWELL'

PAYLOAD='HELLO, MY FRIEND! STAY AWHILE AND LISTEN! SOOOME LOOOONG STRIIING CHAAAAAIN.'
PAYLOAD_RSA=$PAYLOAD

echo ""

print_test_data() {
    echo "Method| ${1}"
    echo "Key| ${2}"
    echo "Text| ${3}"
    echo "Encrypted| ${4}"
    echo "Decrypted| ${5}"
    echo ""
}

ENCODED_PAYLOAD=$(./cryptobase.py -k ${SUBST_KEY} -m mapping.txt -s bytes_cfb -t encode "${PAYLOAD}" | base64 -w 0)
DECODED_PAYLOAD=$(echo "${ENCODED_PAYLOAD}" | base64 -d | ./cryptobase.py -k ${SUBST_KEY} -m mapping.txt -s bytes_cfb -t decode)

print_test_data "ASCII Bytes + CFB" $SUBST_KEY "${PAYLOAD}" "base64:${ENCODED_PAYLOAD}" "${DECODED_PAYLOAD}" | column -tL  -s "|"
