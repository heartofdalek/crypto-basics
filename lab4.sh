#!/bin/bash

echo "Лабораторная 4, вариант 2"
echo

./cryptobase.py -d -s dh_curves -t main_task -k 1

echo
echo "Тест на других данных (добавить -d для развернутого вывода):"
echo

for i in $(seq 2 10); do 
    echo "Тест $i: "$(./cryptobase.py -s dh_curves -t main_task -k $i); 
done
