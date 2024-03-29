const builtin = @import("builtin");
const std = @import("std");

pub const Input = std.mem.TokenIterator(u8, .any);

pub const Parts = enum {
    PartA,
    PartB,
    Both,
};

pub const Result = struct {
    u128 = 0,
    u128 = 0,
};

pub const Info = struct {
    input: Input,
    parts: Parts = Parts.Both,
    result: Result = Result{},
};
