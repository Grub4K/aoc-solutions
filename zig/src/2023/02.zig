const std = @import("std");
const utils = @import("../utils.zig");

const valid = .{
    .red = 12,
    .green = 13,
    .blue = 14,
};

pub fn run(input: *utils.Input) !utils.Result {
    var result = utils.Result{};

    var index: usize = 0;
    while (input.next()) |line| {
        index += 1;
        var it = std.mem.tokenizeAny(u8, line, ";, ");
        _ = it.next();
        _ = it.next();

        var game_valid = true;
        var required_red: u32 = 0;
        var required_green: u32 = 0;
        var required_blue: u32 = 0;

        while (it.next()) |raw_amount| {
            const amount = try std.fmt.parseInt(u32, raw_amount, 10);
            const color = it.next().?;
            if (color.len == "red".len) {
                if (amount > valid.red) game_valid = false;
                if (amount > required_red) required_red = amount;
            } else if (color.len == "green".len) {
                if (amount > valid.green) game_valid = false;
                if (amount > required_green) required_green = amount;
            } else if (color.len == "blue".len) {
                if (amount > valid.blue) game_valid = false;
                if (amount > required_blue) required_blue = amount;
            }
        }
        if (game_valid) result[0] += index;
        result[1] += required_red * required_green * required_blue;
    }

    return result;
}
