const std = @import("std");
const utils = @import("utils.zig");

const days = .{
    .{ "2023-01", @import("2023/01.zig") },
    .{ "2023-02", @import("2023/02.zig") },
    .{ "2023-07", @import("2023/07.zig") },
};

const RunFunctionType = *const fn (*utils.Input) anyerror!utils.Result;
fn buildYears() !std.StringHashMap(RunFunctionType) {
    var years = std.StringHashMap(RunFunctionType).init(std.heap.page_allocator);

    inline for (days) |info| {
        years.putNoClobber(info[0], info[1].run) catch unreachable;
    }

    return years;
}

fn fail(_stdout: anytype, msg: []const u8) !void {
    var stdout = _stdout;
    try stdout.writer().print("err, {s}\n", .{msg});
    try stdout.flush();
}

pub fn main() !void {
    var years = try buildYears();
    defer years.deinit();

    var args = try std.process.argsWithAllocator(std.heap.page_allocator);
    defer args.deinit();

    var out = std.io.getStdOut();
    defer out.close();
    var stdout = std.io.bufferedWriter(out.writer());

    _ = args.next().?;
    while (args.next()) |identifier| {
        const runner = years.get(identifier);
        if (runner == null) {
            _ = args.next().?;
            _ = args.next().?;
            try fail(&stdout, "day is not implemented");
            continue;
        }

        // TODO: implement this
        _ = args.next().?; // orelse fail(&stdout, "missing part parameter");
        // const parts = switch (try std.fmt.parseUnsigned(u8, part, 3)) {
        //     0 => utils.Parts.Both,
        //     1 => utils.Parts.PartA,
        //     2 => utils.Parts.PartB,
        //     else => unreachable,
        // };

        // TODO: implement this
        const path = args.next().?; // orelse fail(&stdout, "missing path parameter");
        const file = try std.fs.cwd().openFile(path, .{});
        const contents = try file.reader().readAllAlloc(std.heap.page_allocator, std.math.maxInt(usize));
        file.close();

        var input = std.mem.tokenizeAny(u8, contents, "\r\n");
        const result = try runner.?(&input);

        try stdout.writer().print("res, {?}, {?}\n", result);
        try stdout.flush();
    }
}
