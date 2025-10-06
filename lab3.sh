#!/bin/bash

PAYLOADS=(
    'Привет!'
    'Hello, my friend! Stay awhile and listeN! Sooome loooong striiing chaaaaain.'
    'Смешанный text :) Ра3nыe символы over 100500!',
    'Aaaaaaaaaaaaaaa AAA aaaaaaaaaaaa',
    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
)

for PAYLOAD in "${PAYLOADS[@]}"; do
    echo $PAYLOAD
done;
