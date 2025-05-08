//! Programming Assignment 2: Part Two

fn main() {
    for x in [0.352234607, 0.587040260] {
        let (value, error, reason) = integral(x);
        println!("integral({x}) = {value} +/- {error:e}");
        println!("{reason}");
    }
}

/// Approximate an integral by summing the terms of a series.
/// The argument must be in the interval (0,1]
fn integral(x: f64) -> (f64, f64, String) {
    assert!(
        0.0 < x && x <= 1.0,
        "argument must be in the interval (0,1]"
    );
    let mut result = x;
    let mut term = x;
    let mut numerator = x;
    let mut factorial = 1.0;
    let small_enough = 1e-6;
    let limit = 15;
    let mut reason = format!("Aborted after {} iterations", limit);
    for n in 1..limit {
        let denominator = factorial * (2.0 * (n as f64) + 1.0);
        term = numerator / denominator;
        result += term;
        numerator *= -x * x;
        factorial *= n as f64;
        if term.abs() < small_enough {
            reason = format!("Accurate after {} iterations", n + 1);
            break;
        }
    }
    (result, term.abs(), reason)
}
