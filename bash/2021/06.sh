#!/bin/bash



input_file="../input/06.txt"

function solution {
    local -a fish
    local from to start stop end counter

    fish=(0 0 0 0 0 0 0 0 0)
    read -r input
    for i in ${input//,/ }; do
        (( fish[i]++ ))
    done

    stop=0 from=0 to=6
    for end in "$@"; do
        start=$stop
        stop=$end

        for (( i = start; i < stop; i++ )); do
            (( to=(to+1) % 9, fish[to]+=fish[from], from=(from+1) % 9 ))
        done

        counter=0
        for (( i = 0; i < 9; i++ )); do
            (( counter+= fish[i]))
        done

        printf '%s\n' "$counter"
    done
}

solution 80 256 <"$input_file"
