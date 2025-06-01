//! Programming Assignment 6: Quicksort

use std::cmp::Ordering;
use std::iter::zip;

/// Demonstrate sorting.
fn main() {
    for size in 1..30 {
        let mut input = Vec::new();
        input.resize(size, size as f64);
        for i in 1..size {
            input[i] = (i as f64) - input[i - 1];
        }
        if size > 5 {
            // some special values
            input[0] = f64::NAN;
            input[1] = f64::INFINITY;
            input[2] = 0.0;
            input[3] = -0.0;
            input[4] = f64::NEG_INFINITY;
            input[5] = -f64::NAN;
        }
        let mut expected = input.clone();
        expected.sort_by(|a, b| a.total_cmp(b));
        let mut result = input.clone();
        sort(&mut result);
        if !zip(&result, &expected).all(|pair| pair.0.total_cmp(&pair.1) == Ordering::Equal) {
            println!("   input: {input:?}");
            println!("  result: {result:?}");
            println!("expected: {expected:?}");
        }
    }
}

/// Sort a collection of numbers.
fn sort(numbers: &mut Vec<f64>) {
    quicksort(numbers, 0, (numbers.len() - 1) as isize);
}

/// Recursively sort a collection of numbers using the Quicksort algorithm.
fn quicksort(numbers: &mut Vec<f64>, i: isize, j: isize) {
    let mut left = i;
    let mut right = j;
    let pick = numbers[i as usize];
    while left <= right {
        while numbers[left as usize].total_cmp(&pick) == Ordering::Less {
            left += 1; // adjust left until an element is out of place
        }
        while numbers[right as usize].total_cmp(&pick) == Ordering::Greater {
            right -= 1; // adjust right until an element is out of place
        }
        if left <= right {
            numbers.swap(left as usize, right as usize);
            left += 1;
            right -= 1;
        }
    }
    // recurse on smaller problems
    if i < right {
        quicksort(numbers, i, right);
    }
    if left < j {
        quicksort(numbers, left, j);
    }
}
