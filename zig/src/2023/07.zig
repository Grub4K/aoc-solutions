const std = @import("std");
const utils = @import("../utils.zig");

const Hand = struct {
    value: u8,
    cards: [5]u8,
    bid: u16,
};
const HandValue = enum(u8) {
    FiveOfAKind = 6,
    FourOfAKind = 5,
    FullHouse = 4,
    ThreeOfAKind = 3,
    TwoPairs = 2,
    Pair = 1,
    HighCard = 0,
};

const lookup: [35]u8 = .{ 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0, 0, 0, 0, 14, 0, 0, 0, 0, 0, 0, 0, 0, 11, 13, 0, 0, 0, 0, 0, 12, 0, 0, 10 };

inline fn getHand(data: []const u8, value: []const u8) !Hand {
    return Hand{
        .value = 0,
        .cards = .{
            lookup[data[0] - '2'],
            lookup[data[1] - '2'],
            lookup[data[2] - '2'],
            lookup[data[3] - '2'],
            lookup[data[4] - '2'],
        },
        .bid = try std.fmt.parseInt(u16, value, 10),
    };
}

inline fn calculateHandValue(hand: Hand) HandValue {
    var values = [_]u8{0} ** 15;
    inline for (hand.cards) |item| {
        values[item] += 1;
    }
    const jokers = values[1];
    const amounts = values[2..];
    std.sort.block(u8, amounts, {}, std.sort.desc(u8));

    return switch (amounts[0] + jokers) {
        5 => HandValue.FiveOfAKind,
        4 => HandValue.FourOfAKind,
        3 => if (amounts[1] == 2) HandValue.FullHouse else HandValue.ThreeOfAKind,
        2 => if (amounts[1] == 2) HandValue.TwoPairs else HandValue.Pair,
        else => HandValue.HighCard,
    };
}

fn compareHands(_: void, a: Hand, b: Hand) bool {
    if (a.value != b.value) {
        return a.value < b.value;
    }
    inline for (a.cards[0..4], b.cards[0..4]) |first, second| {
        if (first != second) {
            return first < second;
        }
    }
    return a.cards[4] < b.cards[4];
}

pub fn run(input: *utils.Input) !utils.Result {
    var hands = std.ArrayList(Hand).init(std.heap.page_allocator);
    defer hands.deinit();

    while (input.next()) |line| {
        var iterator = std.mem.tokenizeScalar(u8, line, ' ');
        const hand = try getHand(
            iterator.next() orelse unreachable,
            iterator.next() orelse unreachable,
        );
        try hands.append(hand);
    }

    var result = utils.Result{};
    inline for (0..2) |part| {
        for (hands.items) |*hand| {
            if (part > 0) {
                // XXX: SoA > AoS
                for (0..5) |index| {
                    if (hand.cards[index] == 11) {
                        hand.cards[index] = 1;
                    }
                }
            }
            hand.value = @intFromEnum(calculateHandValue(hand.*));
        }
        std.mem.sort(Hand, hands.items, {}, compareHands);
        for (hands.items, 1..) |hand, multiplier| {
            result[part] += multiplier * hand.bid;
        }
    }

    return result;
}
