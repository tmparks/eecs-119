//! Programming Assignment 1: Part One

fn main() {
    println!("32 Bias 0: {sum}", sum = reciprocal_sum_32(1000, 0.0));
    println!("32 Bias 1e12: {sum}", sum = reciprocal_sum_32(1000, 1e12));
    println!("64 Bias 0: {sum}", sum = reciprocal_sum_64(1000, 0.0));
    println!("64 Bias 1e12: {sum}", sum = reciprocal_sum_64(1000, 1e12));
}

/// Compute the 32-bit sum of reciprocals from 1 up to (and including)
/// the given limit. A bias is applied before (and removed after) computing
/// the sum in order to demonstrate the limited precision of real numbers.
fn reciprocal_sum_32(limit: i32, bias: f32) -> f32 {
    let mut sum = bias;
    for n in 1..=limit {
        sum += 1.0 / (n as f32);
    }
    sum - bias
}

/// Compute the 64-bit sum of reciprocals from 1 up to (and including)
/// the given limit. A bias is applied before (and removed after) computing
/// the sum in order to demonstrate the limited precision of real numbers.
fn reciprocal_sum_64(limit: i64, bias: f64) -> f64 {
    let mut sum: f64 = bias;
    for n in 1..=limit {
        sum += 1.0 / (n as f64);
    }
    sum - bias
}
