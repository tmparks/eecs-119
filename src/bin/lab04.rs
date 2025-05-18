//! Programming Assignment 4: Text formatter

use std::error::Error;
use std::fs;

/// Demonstrate a text formatter.
fn main() -> Result<(), Box<dyn Error>> {
    println!("1234567890123456789012345678901234567890");
    let mut doc = Document::default();
    doc.format("lab04a.txt")?;
    doc.format("lab04b.txt")?;
    doc.format("lab04c.txt")?;
    doc.format("lab04d.txt")?;
    doc.format("lab04e.txt")?;
    Ok(())
}

/// Formatting parameters for a paragraph.
#[derive(Clone, Copy)]
struct Paragraph {
    /// Line width limit.
    width: usize,

    /// Vertical space between lines.
    space: usize,

    /// Indentation. Included in [width][Self::width].
    indent: usize,

    /// Margin. Not included in [width][Self::width].
    margin: usize,

    /// Insert blanks between words so that lines are right justified.
    do_justify: bool,
}

impl Default for Paragraph {
    fn default() -> Paragraph {
        Paragraph {
            width: 40,
            space: 0,
            indent: 0,
            margin: 0,
            do_justify: false,
        }
    }
}

/// Formatting parameters for a document.
struct Document {
    /// Formatting parameters for current paragraph.
    current: Paragraph,

    /// Formatting parameters for next paragraph.
    next: Paragraph,

    /// Buffer for building current line.
    line: String,

    /// Words to be appended to the current [line][Self::line].
    words: Vec<String>,

    /// Current estimate for line length.
    /// Includes [line][Self::line], [words][Self::words]
    /// and space for one blank after each word.
    length: usize,

    /// Format input or reproduce it verbatim.
    do_format: bool,

    /// First line of document.
    is_first_line: bool,
}

impl Default for Document {
    fn default() -> Document {
        Document {
            current: Paragraph::default(),
            next: Paragraph::default(),
            line: String::default(),
            words: Vec::default(),
            length: 0,
            do_format: true,
            is_first_line: true,
        }
    }
}

impl Document {
    /// Produce formatted output from a text file with embedded commands.
    fn format(&mut self, file_name: &str) -> Result<(), Box<dyn Error>> {
        let content = fs::read_to_string(file_name)?;
        for line in content.lines() {
            if !self.do_format && !line.starts_with(".FI") {
                println!("{line}");
            } else if line.starts_with('.') {
                self.command(line)?;
            } else {
                self.text(line)?;
            }
        }
        self.print_line(false) // last line is never justified
    }

    /// Process a command.
    fn command(&mut self, line: &str) -> Result<(), Box<dyn Error>> {
        let (cmd, remainder) = split_once_whitespace(line);
        // commands without arguments
        match cmd {
            ".PP" => self.paragraph(5)?,
            ".LP" => self.paragraph(0)?,
            ".JST" => self.next.do_justify = true,
            ".NJST" => self.next.do_justify = false,
            ".FI" => self.do_format = true,
            ".NF" => {
                self.print_line(false)?;
                self.do_format = false;
            }
            _ => {
                // commands with arguments
                let (arg, remainder) = split_once_whitespace(remainder);
                match cmd {
                    ".IP" => {
                        self.next.indent = arg.parse::<usize>()?;
                        self.paragraph(0)?;
                        self.label(remainder)?;
                    }
                    ".W" => self.next.width = arg.parse::<usize>()?,
                    ".I" => self.next.indent = arg.parse::<usize>()?,
                    ".M" => self.next.margin = arg.parse::<usize>()?,
                    ".SP" => self.next.space = arg.parse::<usize>()?,
                    _ => (), // ignore unrecognized commands
                }
            }
        }
        Ok(())
    }

    /// Process a line of text.
    fn text(&mut self, line: &str) -> Result<(), Box<dyn Error>> {
        for word in line.split_whitespace() {
            let length = word.chars().count();
            if self.length + length > self.current.width {
                self.print_line(self.current.do_justify)?;
            }
            self.words.push(word.to_string());
            self.length += length + 1; // allow for blank space between words
        }
        Ok(())
    }

    /// Process a paragraph.
    fn paragraph(&mut self, indent: usize) -> Result<(), Box<dyn Error>> {
        self.print_line(false)?; // last line is never justified
        if !self.is_first_line {
            println!(); // blank line
        }
        self.current = self.next;
        self.length = self.current.indent + indent; // exclude margin
        self.line = " ".repeat(self.current.margin + self.length);
        Ok(())
    }

    /// Process a paragraph label.
    fn label(&mut self, mut label: &str) -> Result<(), Box<dyn Error>> {
        if label.starts_with('<') && label.ends_with('>') {
            label = label.strip_prefix('<').ok_or("missing prefix")?;
            label = label.strip_suffix('>').ok_or("missing suffix")?;
        }
        let length = label.chars().count();
        let mut pad = 1;
        if self.current.indent > length {
            pad = self.current.indent - length;
        }
        self.length = length + pad; // exclude margin
        self.line = " ".repeat(self.current.margin) + &label + &" ".repeat(pad);
        Ok(())
    }

    /// Print a line of text (with optional justification)
    fn print_line(&mut self, do_justify: bool) -> Result<(), Box<dyn Error>> {
        if self.words.len() > 0 {
            let mut width = self.length - 1; // remove blank after last word
            if do_justify {
                width = self.current.width;
            }
            let gaps = self.words.len() - 1;
            self.length -= self.words.len(); // remove blank after each word
            let mut remaining_pad = width - self.length;
            for n in 0..gaps {
                let remaining_gaps = gaps - n;
                let pad = rounding_div(remaining_pad, remaining_gaps);
                self.line += &self.words[n];
                self.line += &" ".repeat(pad);
                remaining_pad -= pad;
            }
            self.line += self.words.last().ok_or("missing word")?;
            println!("{}{}", self.line, "\n".repeat(self.current.space));
            self.words.clear();
            self.length = self.current.indent; // exclude margin
            self.line = " ".repeat(self.current.margin + self.length);
            self.is_first_line = false;
        }
        Ok(())
    }
}

/// Split a string on the first occurence of whitespace
/// and return the prefix/suffix before/after the whitespace.
/// The suffix is empty if the string contains no whitespace.
fn split_once_whitespace(text: &str) -> (&str, &str) {
    let (prefix, suffix) = text.split_once(char::is_whitespace).unwrap_or((text, ""));
    (prefix, suffix.trim_start())
}

/// Rounding division operator.
fn rounding_div(numerator: usize, denominator: usize) -> usize {
    (numerator + denominator / 2) / denominator
}
