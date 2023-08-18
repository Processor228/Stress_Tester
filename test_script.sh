g++ -o gen test_gen_src.cpp
g++ -o tested tested_src.cpp
g++ -o brute bruteforce_src.cpp

for((i = 0; i < 130; ++i)); do
    echo $i
    ./gen $i > generated_input
	cat generated_input

    ./tested < generated_input > out1 # out1 is for tested
    ./brute < generated_input > out2  # out2 is for bruteforce

    diff -w out1 out2 || break
    diff -w <(./tested < generated_input) <(./brute < generated_input) || break

done

rm gen tested brute generated_input out1 out2
