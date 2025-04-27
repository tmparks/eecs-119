use std::fs;

fn main() {
    let file_name = "lab01c.txt";
    let mut content = String::new();
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
