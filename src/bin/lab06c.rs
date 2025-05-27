//! Programming Assignment 6: Strange function

/// Demonstrate strange function.
fn main() {
    for x in 0..200 {
        println!("f({x}) = {}", f(x));
    }
}

/// A strange function.
fn f(x: i32) -> i32 {
    if x > 100 {
        return x - 10;
    } else {
        return g(f(x + 11));
    }
}

/// Another strange function.
fn g(x: i32) -> i32 {
    if x > 100 {
        return x - 10;
    } else {
        return f(g(x + 11));
    }
}
