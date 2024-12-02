#!/usr/bin/env bash

isSafeA() {
    local -n list="${1}"
    local i diff trend


    for (( i = 1; i < ${#list[@]}; i++ )); do
        if (( !trend )); then
            (( trend = ((list[i-1] < list[i]) << 1) - 1 ))
        fi

        (( diff = list[i] - list[i-1] ))
        if (( diff != trend && diff != 2 * trend && diff != 3 * trend )); then
            return 1
        fi
    done

    return 0
}

isSafeB() {
    local -n list="${1}"
    local i diff trend skip prev found

    for (( skip = 0; skip < ${#list[@]}; skip++ )); do
        unset prev
        (( trend = 0, found = 1 ))
        for (( i = 0; i < ${#list[@]}; i++ )); do
            (( skip == i )) && continue
            if [[ -z "${prev}" ]]; then
                (( prev = list[i] ))
                continue
            fi

            if (( !trend )); then
                (( trend = ((prev < list[i]) << 1) - 1 ))
            fi

            (( diff = list[i] - prev ))
            if (( diff != trend && diff != 2 * trend && diff != 3 * trend )); then
                (( found = 0 ))
                break
            fi

            (( prev = list[i] ))
        done
        if (( found )); then
            return 0
        fi
    done

    return 1
}

solution() {
    local sumA=0 sumB=0

    while read -ra line; do
        if isSafeA line; then
            (( sumA += 1 ))
        fi

        if isSafeB line; then
            (( sumB += 1 ))
        fi
    done

    printf '%s\n' "${sumA}" "${sumB}"
}

solution <"${1}"
