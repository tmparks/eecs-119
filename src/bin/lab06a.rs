//! Programming Assignment 6: Quicksort

/// Demonstrate sorting.
fn main() {
    for size in 1..30 {
        let mut numbers = Vec::new();
        numbers.resize(size, size as f64);
        for i in 1..size {
            // TODO: use random numbers
            numbers[i] = (i as f64) - numbers[i - 1];
        }
        let mut result = numbers.clone();
        sort(&mut result);
        println!(" input: {numbers:?}");
        println!("result: {result:?}");
    }
}

/// Sort a collection of numbers.
fn sort(numbers: &mut Vec<f64>) {
    quicksort(numbers, 0, numbers.len() - 1);
}

/// Recursively sort a collection of numbers using the Quicksort algorithm.
fn quicksort(numbers: &mut Vec<f64>, i: usize, j: usize) {
    let i = i as isize; // use signed integers internally
    let j = j as isize;
    let mut left = i;
    let mut right = j;
    let pick = numbers[i as usize];
    while left <= right {
        while numbers[left as usize] < pick {
            left += 1; // adjust left until an element is out of place
        }
        while numbers[right as usize] > pick {
            right -= 1; // adjust right until an element is out of place
        }
        if left <= right {
            let temp = numbers[left as usize]; // interchange elements
            numbers[left as usize] = numbers[right as usize];
            numbers[right as usize] = temp;
            left += 1;
            right -= 1;
        }
    }
    // recurse on smaller problems
    if i < right {
        quicksort(numbers, i as usize, right as usize);
    }
    if left < j {
        quicksort(numbers, left as usize, j as usize);
    }
}
