#!/bin/bash

CAESAR_KEY=7
SUBST_KEY='HIDEMEWELL'

PAYLOADS=(
    'Привет!'
    'HELLO, MY FRIEND! STAY AWHILE AND LISTEN! SOOOME LOOOONG STRIIING CHAAAAAIN.'
    'Смешанный text :) Ра3nыe символы over 100500!'
)

echo ""

print_rsa_test_data() {
    echo "Method| ${1}"
    echo "Text| ${2}"
    echo "Encrypted| ${3}"
    echo "Decrypted| ${4}"
    echo "PrivKey| ${5}"
    echo "PubKey| ${6}"
    echo ""
}

./cryptobase.py -y -s rsa_base -t keygen > /dev/null

for PAYLOAD_RSA in "${PAYLOADS[@]}"; do

    ENCODED_PAYLOAD_RSA=$( ./cryptobase.py -s rsa_base -t encode "${PAYLOAD_RSA}" )
    DECODED_PAYLOAD_RSA=$( echo "${ENCODED_PAYLOAD_RSA}" | ./cryptobase.py -s rsa_base -t decode )
    PRIVATE_KEY=$(cat id_rsa.priv)
    PUBLIC_KEY=$(cat id_rsa.pub)

    print_rsa_test_data "Lab2: RSA" "${PAYLOAD_RSA}" "${ENCODED_PAYLOAD_RSA}" "${DECODED_PAYLOAD_RSA}" "${PRIVATE_KEY}" "${PUBLIC_KEY}" | column -tL  -s "|"
    
done;
