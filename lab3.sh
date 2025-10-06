#!/bin/bash

PAYLOAD='Hello, world!'

PAYLOADS_EXTENDED=(
    'Привет!'
    'Hello, my friend! Stay awhile and listeN! Sooome loooong striiing chaaaaain.'
    'Смешанный text :) Ра3nыe символы over 100500!'
    'Aaaaaaaaaaaaaaa AAA aaaaaaaaaaaa'
    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    ''
)

print_test_data() {
    echo "Original message^ ${1}"
    echo "Signed message^ ${2}"
    echo "Check result^ ${3}"
    echo "Check wrong message^ ${4}"
    echo "Check wrong sign^ ${5}"
    echo ""
}

#./cryptobase.py -s digital_signature -t keygen

SIGN_RESULT=$(./cryptobase.py -d -s digital_signature -t sign "${PAYLOAD}")
VERIFY_RESULT=$(./cryptobase.py -d -s digital_signature -t verify "$SIGN_RESULT")
VERIFY_RESULT_WRONG_MESSAGE=$(./cryptobase.py -d -s digital_signature -t verify "N$SIGN_RESULT")
VERIFY_RESULT_WRONG_SIGN=$(./cryptobase.py -d -s digital_signature -t verify "${SIGN_RESULT}1")

print_test_data "$PAYLOAD" "$SIGN_RESULT" "$VERIFY_RESULT" "$VERIFY_RESULT_WRONG_MESSAGE" "$VERIFY_RESULT_WRONG_SIGN" | column -tL  -s "^"

for PAYLOAD in "${PAYLOADS_EXTENDED[@]}"; do
    SIGN_RESULT=$(./cryptobase.py -d -s digital_signature -t sign "${PAYLOAD}")
    VERIFY_RESULT=$(./cryptobase.py -d -s digital_signature -t verify "$SIGN_RESULT")
    VERIFY_RESULT_WRONG_MESSAGE=$(./cryptobase.py -d -s digital_signature -t verify "N$SIGN_RESULT")
    VERIFY_RESULT_WRONG_SIGN=$(./cryptobase.py -d -s digital_signature -t verify "${SIGN_RESULT}1")
    print_test_data "$PAYLOAD" "$SIGN_RESULT" "$VERIFY_RESULT" "$VERIFY_RESULT_WRONG_MESSAGE" "$VERIFY_RESULT_WRONG_SIGN" | column -tL  -s "^"
done;
