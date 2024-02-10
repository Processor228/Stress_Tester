#!/bin/bash

g++ -o gen gen.cpp
g++ -o tested opt.cpp
g++ -o brute bru.cpp

for((i = 0; i < 130; ++i)); do
    echo $i
    ./gen $i > generated_input

	cat generated_input >> report.txt

    ./tested < generated_input > out1 # out1 is for tested
    ./brute < generated_input > out2  # out2 is for bruteforce

    diff -w out1 out2

    # so diff returns 1 in case outputs are different, and break will occur
    if [ $? -eq  1 ]; then
        break
    fi

done

rm gen tested brute generated_input out1 out2
