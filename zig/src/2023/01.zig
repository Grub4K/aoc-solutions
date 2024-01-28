const std = @import("std");
const utils = @import("../utils.zig");

const Direction = enum {
    Left,
    Right,
};

const number_words = [_][]const u8{
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
};

fn findNumber(comptime allow_words: bool, comptime dir: Direction, data: []const u8) u8 {
    var index: usize = if (dir == Direction.Right) 0 else data.len - 1;

    while (true) {
        if ('0' <= data[index] and data[index] <= '9') return data[index] - '0';

        if (allow_words) {
            for (0.., number_words) |number, word| {
                if (index + word.len > data.len) continue;
                if (std.mem.eql(u8, data[index .. index + word.len], word)) {
                    return @intCast(number);
                }
            }
        }

        if (dir == Direction.Right) {
            index += 1;
        } else {
            index -= 1;
        }
    }
}

inline fn calcNumber(comptime allow_words: bool, line: []const u8) u128 {
    return 10 * findNumber(allow_words, Direction.Right, line) + findNumber(allow_words, Direction.Left, line);
}

pub fn run(input: *utils.Input) !utils.Result {
    var result = utils.Result{};

    while (input.next()) |line| {
        result[0] += calcNumber(false, line);
        result[1] += calcNumber(true, line);
    }

    return result;
}
