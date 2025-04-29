//! Programming Assignment 1: Part Two

use std::fs;

/// Read a sequence of words from a file and print them.
/// Line breaks in the input are discarded.
/// Any input after the % character is discarded.
/// A new line is started after any word that starts with r, s, or t.
/// One blank is printed between words on the same line.
fn main() {
    let file_name = "lab01c.txt";
    let mut content = String::new(); //initially empty
    if let Ok(file_content) = fs::read_to_string(file_name) {
        content = file_content;
    }
    if let Some(new_length) = content.find('%') {
        content.truncate(new_length);
    }
    let mut new_line = true;
    for word in content.split_whitespace() {
        if !new_line {
            print!(" ");
        }
        print!("{word}");
        new_line = word.starts_with(&['r', 's', 't']);
        if new_line {
            println!();
        }
    }
    if !new_line {
        println!();
    }
}
