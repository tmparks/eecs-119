//! Programming Assignment 2: Part One

use std::fs;

/// Print the length of the longest word in each line of a file.
fn main() {
    let file_name = "lab02a.txt";
    let content = fs::read_to_string(file_name).unwrap_or(String::new());
    for line in content.lines() {
        let longest = line
            .split_whitespace()
            .map(|word| word.chars().count())
            .max()
            .unwrap_or(0);
        println!("{longest}");
    }
}
