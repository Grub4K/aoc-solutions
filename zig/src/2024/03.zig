const std = @import("std");
const utils = @import("../utils.zig");

const size = u32;

fn scanNum(line: []const u8, start_index: usize, comptime sep: u8) struct { result: ?size, index: usize } {
    var index = start_index;
    var result: ?size = null;
    while (true) {
        switch (line[index]) {
            '0'...'9' => {
                if (result == null) result = 0;
                result.? *= 10;
                result.? += line[index] - '0';
                index += 1;
            },
            sep => {
                break;
            },
            else => {
                result = null;
                break;
            },
        }
    }
    return .{
        .result = result,
        .index = index,
    };
}

pub fn run(input: *utils.Input) !utils.Result {
    var enabled = true;
    var sumA: size = 0;
    var sumB: size = 0;
    while (input.next()) |line| {
        var index: usize = 0;

        while (std.mem.indexOfAnyPos(u8, line, index, "md")) |i| {
            if (line[i] == 'd') {
                if (std.mem.startsWith(u8, line[i + 1 ..], "o()")) {
                    index = i + "do()".len;
                    enabled = true;
                } else if (std.mem.startsWith(u8, line[i + 1 ..], "on't()")) {
                    index = i + "don't()".len;
                    enabled = false;
                } else {
                    index = i + 1;
                }
                continue;
            }
            if (!std.mem.startsWith(u8, line[i + 1 ..], "ul(")) {
                index = i + 1;
                continue;
            }
            index = i + "mul(".len;

            var result = scanNum(line, index, ',');
            index = result.index;
            const resultA = result.result orelse continue;
            index += 1;

            result = scanNum(line, index, ')');
            index = result.index;
            const resultB = result.result orelse continue;
            index += 1;

            sumA += resultA * resultB;
            if (enabled) {
                sumB += resultA * resultB;
            }
        }
    }
    return utils.Result{
        @as(u128, sumA),
        @as(u128, sumB),
    };
}
