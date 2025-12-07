#!/usr/bin/env bash

solution() {
    local line after resultA resultB
    local -A rays splits

    read -r line
    after="${line#*S}"
    rays=(
        ["$(( ${#line} - ${#after} - 1 ))"]=1
    )

    resultA=0
    while read -r line; do
        splits=()
        for ray in "${!rays[@]}"; do
            if [[ "${line:${ray}:1}" == "^" ]]; then
                (( resultA += 1 ))
                (( splits[$((ray - 1))] += rays[${ray}] ))
                (( splits[$((ray + 1))] += rays[${ray}] ))
                unset "rays[${ray}]"
            fi
        done
        for split in "${!splits[@]}"; do
            (( rays[${split}] += splits[${split}] ))
        done
    done

    resultB=0
    for ray in "${!rays[@]}"; do
        (( resultB += rays[$ray] ))
    done

    printf '%d\n' "${resultA}" "${resultB}"
}

solution <"${1}"
