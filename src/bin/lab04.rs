//! Programming Assignment 4: Text formatter

use std::error::Error;
use std::fs::read_to_string;

/// An empty, generic result.
type Result = std::result::Result<(), Box<dyn Error>>;

/// Demonstrate a text formatter.
fn main() -> Result {
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
    /// Line length limit.
    limit: usize,

    /// Vertical space between lines.
    space: usize,

    /// Indentation. Included in [`limit`][Self::limit].
    indent: usize,

    /// Margin. Not included in [`limit`][Self::limit].
    margin: usize,

    /// Insert blanks between words so that lines are right justified.
    do_justify: bool,
}

impl Default for Paragraph {
    fn default() -> Paragraph {
        Paragraph {
            limit: 40,
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

    /// Content of the current line before the first word.
    prefix: String,

    /// Words of the current line.
    words: Vec<String>,

    /// Current estimate for line length.
    /// Includes [`prefix`][Self::prefix], [`words`][Self::words]
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
            prefix: String::default(),
            words: Vec::default(),
            length: 0,
            do_format: true,
            is_first_line: true,
        }
    }
}

/// Functions for formatting a document.
impl Document {
    /// Produce formatted output from a text file with embedded commands.
    fn format(&mut self, file_name: &str) -> Result {
        let content = read_to_string(file_name)?;
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
    fn command(&mut self, line: &str) -> Result {
        let (cmd, remainder) = split_once_whitespace(line);
        // commands without arguments
        match cmd {
            ".PP" => self.paragraph(5, "")?,
            ".LP" => self.paragraph(0, "")?,
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
                        self.paragraph(0, remainder)?;
                    }
                    ".W" => self.next.limit = arg.parse::<usize>()?,
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
    fn text(&mut self, line: &str) -> Result {
        for word in line.split_whitespace() {
            let length = word.chars().count();
            if self.length + length > self.current.limit {
                self.print_line(self.current.do_justify)?;
            }
            self.words.push(word.to_string());
            self.length += length + 1; // allow for blank space between words
        }
        Ok(())
    }

    /// Process a paragraph.
    fn paragraph(&mut self, indent: usize, mut label: &str) -> Result {
        self.print_line(false)?; // last line is never justified
        if !self.is_first_line {
            println!(); // blank line
        }
        self.current = self.next;
        if label.starts_with('<') && label.ends_with('>') {
            label = label.strip_prefix('<').ok_or("missing prefix")?;
            label = label.strip_suffix('>').ok_or("missing suffix")?;
        }
        let length = label.chars().count();
        let indent = indent + self.current.indent;
        let indent = if indent > length || length == 0 {
            indent - length
        } else {
            1
        };
        self.length = length + indent; // exclude margin
        self.prefix = " ".repeat(self.current.margin) + &label + &" ".repeat(indent);
        Ok(())
    }

    /// Print a line of text (with optional justification)
    fn print_line(&mut self, do_justify: bool) -> Result {
        if self.words.len() > 0 {
            let gaps = self.words.len() - 1;
            let limit = if do_justify {
                self.current.limit
            } else {
                self.length - 1 // remove blank after last word
            };
            let length = self.length - self.words.len(); // remove blank after each word
            let mut remaining_pad = limit - length;

            print!("{}", self.prefix);
            for n in 0..gaps {
                let remaining_gaps = gaps - n;
                let pad = rounding_div(remaining_pad, remaining_gaps);
                print!("{}{}", self.words[n], " ".repeat(pad));
                remaining_pad -= pad;
            }
            println!("{}", self.words.last().ok_or("missing word")?);
            print!("{}", "\n".repeat(self.current.space));

            self.words.clear();
            self.length = self.current.indent; // exclude margin
            self.prefix = " ".repeat(self.current.margin + self.length);
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
