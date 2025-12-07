#!/usr/bin/env bash

function solution {
    mapfile -t lines
    read -ra ops <<< "${lines[-1]}"
    unset "lines[-1]"

    columns=()
    column=()

    index=0
    while (( index < ${#lines[0]} )); do
        (( space = 1 ))
        for line in "${lines[@]}"; do
            if [[ "${line:${index}:1}" != " " ]]; then
                (( space = 0 ))
            fi
        done

        if (( !space )); then
            (( i = 0 ))
            for line in "${lines[@]}"; do
                column[i]+="${line:${index}:1}"
                (( i++ ))
            done
        else
            printf -v colStr ':%s' "${column[@]}"
            columns+=("${colStr:1}")
            column=()
        fi
        (( index++ ))
    done
    printf -v colStr ':%s' "${column[@]}"
    columns+=("${colStr:1}")

    resultA=0
    resultB=0
    for (( i = 0; i < ${#columns[@]}; i++ )); do
        op="${ops[${i}]}"
        # evil word splitting
        IFS=: column=( ${columns[${i}]} )

        total="${column[0]}"
        for num in "${column[@]:1}"; do
            (( total = total ${op} ${num} ))
        done
        (( resultA += total ))

        columnB=()
        for (( j = 0; j < "${#column[0]}"; j++ )); do
            for line in "${column[@]}"; do
                columnB[${j}]+="${line:${j}:1}"
            done
        done
        total="${columnB[0]}"
        for num in "${columnB[@]:1}"; do
            (( total = total ${op} ${num} ))
        done
        (( resultB += total ))
    done
    printf '%d\n' "${resultA}" "${resultB}"
}

solution <"${1}"
