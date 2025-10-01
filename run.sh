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

print_rsa_test_data() {
    echo "Method| ${1}"
    echo "Text| ${2}"
    echo "Encrypted| ${3}"
    echo "Decrypted| ${4}"
    echo "PrivKey| ${5}"
    echo "PubKey| ${6}"
    echo ""
}

ENCODED_PAYLOAD=$(./cryptobase.py -k ${CAESAR_KEY} -m mapping.txt -s caesar_mapped -t encode "${PAYLOAD}")
DECODED_PAYLOAD=$(./cryptobase.py -k ${CAESAR_KEY} -m mapping.txt -s caesar_mapped -t decode "${ENCODED_PAYLOAD}")

print_test_data "Lab1: Caesar with substitute alphabet" $CAESAR_KEY "${PAYLOAD}" "${ENCODED_PAYLOAD}" "${DECODED_PAYLOAD}" | column -tL  -s "|"

ENCODED_PAYLOAD=$(./cryptobase.py -k ${CAESAR_KEY} -m mapping.txt -s caesar_simple -t encode "${PAYLOAD}")
DECODED_PAYLOAD=$(./cryptobase.py -k ${CAESAR_KEY} -m mapping.txt -s caesar_simple -t decode "${ENCODED_PAYLOAD}")

print_test_data "Caesar basic" $CAESAR_KEY "${PAYLOAD}" "${ENCODED_PAYLOAD}" "${DECODED_PAYLOAD}" | column -tL  -s "|"

ENCODED_PAYLOAD=$(./cryptobase.py -k ${SUBST_KEY} -m mapping.txt -s subst_cfb -t encode "${PAYLOAD}")
DECODED_PAYLOAD=$(./cryptobase.py -k ${SUBST_KEY} -m mapping.txt -s subst_cfb -t decode "${ENCODED_PAYLOAD}")

print_test_data "Modified Vigenere + CFB" $SUBST_KEY "${PAYLOAD}" "${ENCODED_PAYLOAD}" "${DECODED_PAYLOAD}" | column -tL  -s "|"

ENCODED_PAYLOAD=$(./cryptobase.py -k ${SUBST_KEY} -m mapping.txt -s bytes_cfb -t encode "${PAYLOAD}" | base64 -w 0)
DECODED_PAYLOAD=$(echo "${ENCODED_PAYLOAD}" | base64 -d | ./cryptobase.py -k ${SUBST_KEY} -m mapping.txt -s bytes_cfb -t decode)

print_test_data "ASCII Bytes + CFB" $SUBST_KEY "${PAYLOAD}" "base64:${ENCODED_PAYLOAD}" "${DECODED_PAYLOAD}" | column -tL  -s "|"

# start RSA example

./cryptobase.py -y -s rsa_base -t keygen > /dev/null

ENCODED_PAYLOAD_RSA=$( ./cryptobase.py -s rsa_base -t encode "${PAYLOAD_RSA}" )
DECODED_PAYLOAD_RSA=$( echo "${ENCODED_PAYLOAD_RSA}" | ./cryptobase.py -s rsa_base -t decode )
PRIVATE_KEY=$(cat id_rsa.priv)
PUBLIC_KEY=$(cat id_rsa.pub)

print_rsa_test_data "Lab2: RSA" "${PAYLOAD_RSA}" "${ENCODED_PAYLOAD_RSA}" "${DECODED_PAYLOAD_RSA}" "${PRIVATE_KEY}" "${PUBLIC_KEY}" | column -tL  -s "|"
