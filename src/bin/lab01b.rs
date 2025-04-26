use std::fs;

fn main() {
    two_largest(read_sequence("lab01b.txt"));
}

fn read_sequence(file_name: &str) -> Vec<i32> {
    let content = fs::read_to_string(file_name).unwrap();
    let mut iterator = content
        .split_whitespace()
        .map(|word| word.parse::<i32>().unwrap());
    let length = iterator.next().unwrap();
    let sequence: Vec<_> = iterator.collect();
    assert_eq!(length as usize, sequence.len());
    sequence
}

fn two_largest(sequence: Vec<i32>) {
    let mut largest = i32::MIN;
    let mut next_largest = i32::MIN;
    for number in sequence {
        if largest < number {
            next_largest = largest;
            largest = number;
        } else if next_largest < number && number != largest {
            next_largest = number;
        }
    }
    println!("Largest value in sequence: {largest}");
    println!("Next largest value: {next_largest}");
}
