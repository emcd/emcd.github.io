const std = @import("std");
const allocator = std.heap.page_allocator;

pub fn main() void {
    printOptionIfExists(null);
    printOptionIfExists(42);
    //formatTitle("Hello, world!", null, null);
}

fn printOptionIfExists(option: ?i32) void {
    if (option) |data| {
        std.debug.print("{}\n", .{data});
    }
}

// TODO: Finish or use https://github.com/suirad/zig-strings/blob/master/strings.zig.
// Reference: https://ziglang.org/documentation/master/std/#std;ArrayList
//fn formatTitle(
//    base: []const u8, variant: ?[]const u8, version: ?[]const u8
//) std.mem.Allocator.Error![]u8 {
//    var output = std.ArrayList([]const u8).init(allocator);
//    try output.append(base);
//    if (variant) |data| {
//        try output.append(data);
//    }
//    if (version) |data| {
//        try output.append(data);
//    }
//}
