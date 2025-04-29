//! Programming Assignment 1: Part Two

use std::fs;
use std::str::FromStr;

/// Read a sequence of integers from a file
/// and print the two largest distinct values.
/// The sequence is preceded by an integer indicating its length.
fn main() {
    let file_name = "lab01b.txt";
    let mut content = String::new(); // initially empty
    if let Ok(file_content) = fs::read_to_string(file_name) {
        content = file_content;
    }
    let mut sequence = content.split_whitespace().map(i32::from_str).flatten();
    if let Some(expected_length) = sequence.next() {
        let mut largest = i32::MIN;
        let mut next_largest = i32::MIN;
        let mut actual_length = 0;
        for number in sequence {
            if largest < number {
                next_largest = largest;
                largest = number;
            } else if next_largest < number && number != largest {
                next_largest = number;
            }
            actual_length += 1;
        }
        assert_eq!(actual_length, expected_length);
        println!("Largest value in sequence: {largest}");
        println!("Next largest value: {next_largest}");
    }
}
