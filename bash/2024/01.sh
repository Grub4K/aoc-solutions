#!/usr/bin/env bash

qsort() {
    local -n items="${1}"
    local -a stack=("${items[@]}")
    local high low index=2 pivot threshold x

    (( stack[0] = 0, stack[1] = ${#items[@]} - 1 ))
    while (( index > 0 )); do
        (( index -= 2, low = stack[index], high = stack[index+1] ))

        (( pivot = items[high], i = low - 1 ))
        for (( j = low; j <= high - 1; j++ )); do
            if (( items[j] <= pivot )); then
                (( i++, temp = items[i], items[i] = items[j], items[j] = temp ))
            fi
        done
        (( i++, temp = items[i], items[i] = items[high], items[high] = temp, pivot = i ))

        if (( pivot - 1 > low )); then
            (( stack[index] = low, stack[index+1] = pivot - 1, index += 2 ))
        fi

        if (( pivot + 1 < high )); then
            (( stack[index] = pivot + 1, stack[index+1] = high, index += 2 ))
        fi
    done
}

solution() {
    local -a left right counts
    local i l r temp mask distance similarity

    while read -r l r; do
        left+=( "${l}" )
        right+=( "${r}" )
        (( counts[r]++ ))
    done

    qsort left
    qsort right

    for (( i = 0; i < ${#left[@]}; i++ )); do
        (( temp = left[i] - right[i], distance += (((temp >= 0) << 1) - 1) * temp ))

        (( similarity += left[i] * counts[left[i]] ))
    done

    printf '%s\n' "${distance}" "${similarity}"
}

solution <"${1}"
