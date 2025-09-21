#!/bin/bash

CAESAR_KEY=7
SUBST_KEY='HIDEMEWELL'

PAYLOAD='HELLO, MY FRIEND! STAY AWHILE AND LISTEN! SOOOME LOOOONG STRIIING CHAAAAAIN.'

echo ""

print_test_data() {
    echo "Метод| ${1}"
    echo "Ключ| ${2}"
    echo "Текст| ${3}"
    echo "Шифр| ${4}"
    echo "Дешифр| ${5}"
    echo ""
}

ENCODED_PAYLOAD=$(./cryptobase.py -k ${CAESAR_KEY} -s caesar_mapped -t encode "${PAYLOAD}")
DECODED_PAYLOAD=$(./cryptobase.py -k ${CAESAR_KEY} -s caesar_mapped -t decode "${ENCODED_PAYLOAD}")

print_test_data "Цезарь, с подстановочным алфавитом" $CAESAR_KEY "${PAYLOAD}" "${ENCODED_PAYLOAD}" "${DECODED_PAYLOAD}" | column -tL  -s "|"

ENCODED_PAYLOAD=$(./cryptobase.py -k ${CAESAR_KEY} -s caesar_simple -t encode "${PAYLOAD}")
DECODED_PAYLOAD=$(./cryptobase.py -k ${CAESAR_KEY} -s caesar_simple -t decode "${ENCODED_PAYLOAD}")

print_test_data "Цезарь, с базовым алфавитом" $CAESAR_KEY "${PAYLOAD}" "${ENCODED_PAYLOAD}" "${DECODED_PAYLOAD}" | column -tL  -s "|"

ENCODED_PAYLOAD=$(./cryptobase.py -k ${SUBST_KEY} -s subst_cfb -t encode "${PAYLOAD}")
DECODED_PAYLOAD=$(./cryptobase.py -k ${SUBST_KEY} -s subst_cfb -t decode "${ENCODED_PAYLOAD}")

print_test_data "Замена по подстановочному алфавиту + CFB" $SUBST_KEY "${PAYLOAD}" "${ENCODED_PAYLOAD}" "${DECODED_PAYLOAD}" | column -tL  -s "|"
