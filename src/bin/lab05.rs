//! Programming Assignment 5: A simple graphics language

use std::error::Error;
use std::fs::read_to_string;

/// Demonstrate a plotter.
fn main() -> Result<()> {
    let mut p = Plotter::new(56, 130);
    p.plot("lab05a.txt")?;
    p.plot("lab05b.txt")?;
    p.plot("lab05c.txt")?;
    p.plot("lab05d.txt")?;
    p.plot("lab05e.txt")?;
    Ok(())
}

/// A generic result with any error type.
type Result<T> = std::result::Result<T, Box<dyn Error>>;

/// A page is a sparse collection of points as (row, column) tuples.
type Page = std::collections::BTreeSet<(i32, i32)>;

/// Parameters for a lousy plotter.
struct Plotter {
    /// Collection of points as (row, column) tuples.
    page: Page,

    /// Number of off-page points.
    off: i32,

    /// Number of rows on the page.
    rows: i32,

    /// Number of columns on the page.
    columns: i32,

    /// Vertical position.
    row: f64,

    /// Horizontal position.
    column: f64,

    /// Vertical change for each step.
    row_change: f64,

    /// Horizontal change for each step.
    column_change: f64,
}

impl Default for Plotter {
    fn default() -> Plotter {
        Plotter {
            page: Page::new(),
            off: 0,
            rows: 0,
            columns: 0,
            row: 0.0,
            column: 0.0,
            row_change: 0.0,
            column_change: 0.0,
        }
    }
}

/// Functions for a lousy plotter.
impl Plotter {
    /// Create a new plotter for the specified page size.
    fn new(rows: i32, columns: i32) -> Plotter {
        Plotter {
            rows,
            columns,
            ..Plotter::default()
        }
    }

    /// Read plotting commands from a file.
    fn plot(&mut self, file_name: &str) -> Result<()> {
        let content = read_to_string(file_name)?;
        let mut words = content.split_whitespace();
        let mut word = words.next();
        while word.is_some() {
            let command = first_lowercase_char(word);
            match command {
                Some('m') => self.r#move(next_f64(&mut words)?, next_f64(&mut words)?),
                Some('s') => self.step(next_i32(&mut words)?),
                Some('v') => self.row_change = next_f64(&mut words)?,
                Some('h') => self.column_change = next_f64(&mut words)?,
                Some('p') => self.print(),
                Some('e') => self.page.clear(),
                _ => println!("Unrecognized command {}", word.unwrap_or("")),
            }
            word = words.next(); // attempt to get next command
        }
        Ok(())
    }

    /// Move the imaginary pen without drawing a point.
    fn r#move(&mut self, row: f64, column: f64) {
        self.row = row;
        self.column = column;
    }

    /// Move the imaginary pen, drawing output after each step.
    /// The position of the pen is determined by the previously
    /// specified vertical and horizontal change.
    fn step(&mut self, count: i32) {
        for _ in 0..count {
            self.row += self.row_change;
            self.column += self.column_change;
            let row = self.row.round() as i32;
            let column = self.column.round() as i32;
            if (0..self.rows).contains(&row) && (0..self.columns).contains(&column) {
                self.page.insert((row, column));
            } else {
                self.off += 1;
            }
        }
    }

    /// Print the page.
    fn print(&mut self) {
        println!("╭{}╮", "─".repeat(self.columns as usize));
        // Print rows from top to bottom.
        for row in (0..self.rows).rev() {
            print!("│");
            // Print columns from left to right.
            for column in 0..self.columns {
                if self.page.contains(&(row, column)) {
                    print!("*");
                } else {
                    print!(" ");
                }
            }
            println!("│");
        }
        println!("╰{}╯", "─".repeat(self.columns as usize));
        if self.off > 0 {
            println!("There were {} off-page points", self.off);
            self.off = 0;
        }
    }
}

/// Get the first character and convert to lower case.
fn first_lowercase_char(text: Option<&str>) -> Option<char> {
    text?.chars().next()?.to_lowercase().next()
}

/// Parse next argument as an integer.
fn next_i32(arguments: &mut std::str::SplitWhitespace) -> Result<i32> {
    Ok(arguments.next().ok_or("missing argument")?.parse::<i32>()?)
}

/// Parse next argument as a floating point number.
fn next_f64(arguments: &mut std::str::SplitWhitespace) -> Result<f64> {
    Ok(arguments.next().ok_or("missing argument")?.parse::<f64>()?)
}
