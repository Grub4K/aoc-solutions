const std = @import("std");
const utils = @import("../utils.zig");

const size = i32;
const resultType = struct {
    first: []size,
    second: []size,
    counts: []size,
};

fn prepareInput(input: *utils.Input) !resultType {
    var col_first = std.ArrayList(size).init(std.heap.page_allocator);
    var col_second = std.ArrayList(size).init(std.heap.page_allocator);

    while (input.next()) |line| {
        var tokens = std.mem.tokenizeAny(u8, line, " \t");
        try col_first.append(try std.fmt.parseInt(size, tokens.next().?, 10));
        try col_second.append(try std.fmt.parseInt(size, tokens.next().?, 10));
    }
    const first = col_first.items;
    const second = col_second.items;

    const asc = comptime std.sort.asc(size);
    std.mem.sort(size, first, {}, asc);
    std.mem.sort(size, second, {}, asc);

    const max = @max(first[first.len - 1], second[second.len - 1]);
    const counts = try std.heap.page_allocator.alloc(i32, @abs(max) + 1);
    @memset(counts, 0);
    for (second) |item| {
        counts[@abs(item)] += 1;
    }

    return .{
        .first = first,
        .second = second,
        .counts = counts,
    };
}

pub fn run(input: *utils.Input) !utils.Result {
    const parsed = try prepareInput(input);

    var sum_a: u32 = 0;
    for (parsed.first, parsed.second) |a, b| {
        sum_a += @abs(a - b);
    }

    var sum_b: u32 = 0;
    for (parsed.first) |a| {
        const unsigned: u32 = @intCast(a);
        sum_b += unsigned * @as(u32, @intCast(parsed.counts[unsigned]));
    }

    return utils.Result{
        sum_a,
        sum_b,
    };
}
