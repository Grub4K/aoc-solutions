#!/usr/bin/env bash

isSafeA() {
    local -n list="${1}"
    local i diffs diff


    for (( i = 1; i < ${#list[@]}; i++ )); do
        if [[ -z "${diffs}" ]]; then
            if (( list[i-1] < list[i] )); then
                diffs=" 1 2 3 "
            else
                diffs=" -1 -2 -3 "
            fi
        fi

        (( diff = list[i] - list[i-1] ))
        if [[ "${diffs/ ${diff} /}" == "${diffs}" ]]; then
            return 1
        fi
    done

    return 0
}

isSafeB() {
    local -n list="${1}"
    local i diffs diff skip prev

    for (( skip = 0; skip < ${#list[@]}; skip++ )); do
        unset diffs prev
        (( found = 1 ))
        for (( i = 0; i < ${#list[@]}; i++ )); do
            (( skip == i )) && continue
            if [[ -z "${prev}" ]]; then
                (( prev = list[i] ))
                continue
            fi

            if [[ -z "${diffs}" ]]; then
                if (( prev < list[i] )); then
                    diffs=" 1 2 3 "
                else
                    diffs=" -1 -2 -3 "
                fi
            fi

            (( diff = list[i] - prev ))
            if [[ "${diffs/ ${diff} /}" == "${diffs}" ]]; then
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
