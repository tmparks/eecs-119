//! Programming Assignment 7: Scene analysis

use std::collections::BTreeMap;
use std::collections::BTreeSet;
use std::error::Error;
use std::fs::read_to_string;

/// Demonstrate scene analysis.
fn main() -> Result<()> {
    let mut p = Picture::default();
    p.read("lab07.txt")?;
    p.color();
    p.print(&p.dark_regions);
    println!("There are {} light regions", p.light_regions.len());
    println!("{} touch an edge", p.light_edge_regions.len());
    println!("There are {} dark regions", p.dark_regions.len());
    println!("{} touch an edge", p.dark_edge_regions.len());
    println!("Regions with 1 to 20 pixels");
    p.print(&p.regions_by_size(&p.dark_regions, 1, 20));
    println!("Regions with 21 to 40 pixels");
    p.print(&p.regions_by_size(&p.dark_regions, 21, 40));
    println!("Regions with 41 to 80 pixels");
    p.print(&p.regions_by_size(&p.dark_regions, 41, 80));
    println!("Regions with more than 80 pixels");
    p.print(&p.regions_by_size(&p.dark_regions, 81, 100 * 100));
    println!("Surrounded regions");
    let surrounded_regions = p.surrounded();
    p.print(&surrounded_regions);
    Ok(())
}

/// A generic result with any error type.
type Result<T> = std::result::Result<T, Box<dyn Error>>;

/// Pixel color value.
type Color = isize;

/// A simple picture.
struct Picture {
    /// Initial value for light pixels.
    light: Color,

    /// Initial value for dark pixels.
    dark: Color,

    /// Temporary value for pixels.
    neutral: Color,

    /// Number of rows in the picture.
    rows: usize,

    /// Number of columns in the picture.
    columns: usize,

    /// Colors of light regions.
    light_regions: BTreeSet<Color>,

    /// Colors of dark regions.
    dark_regions: BTreeSet<Color>,

    /// Colors of light regions that touch an edge.
    light_edge_regions: BTreeSet<Color>,

    /// Colors of dark regions that touch an edge.
    dark_edge_regions: BTreeSet<Color>,

    /// Sizes of regions by color.
    region_sizes: BTreeMap<Color, usize>,

    /// Two-dimensional collection of pixels.
    pixels: Vec<Vec<Color>>,
}

impl Default for Picture {
    fn default() -> Picture {
        Picture {
            light: 1,
            dark: -1,
            neutral: 0,
            rows: 0,
            columns: 0,
            light_regions: BTreeSet::new(),
            dark_regions: BTreeSet::new(),
            light_edge_regions: BTreeSet::new(),
            dark_edge_regions: BTreeSet::new(),
            region_sizes: BTreeMap::new(),
            pixels: Vec::new(),
        }
    }
}

/// Functions for a simple picture.
impl Picture {
    /// Read a picture from a file.
    /// The first number read specifies the number of rows.
    /// The second number read specifies the number of columns.
    /// The '*' character indicates a dark pixel.
    /// The '-' character indicates a light pixel.
    fn read(&mut self, file_name: &str) -> Result<()> {
        let content = read_to_string(file_name)?;
        let mut lines = content.lines();
        let rows = next_usize(&mut lines)?;
        let columns = next_usize(&mut lines)?;
        self.erase(rows, columns);
        for row in 0..self.rows {
            let line = lines.next().ok_or("missing row")?;
            let mut chars = line.chars();
            for column in 0..self.columns {
                let char = chars.next().ok_or("missing column")?;
                match char {
                    '*' => self.pixels[row][column] = self.dark,
                    '-' => self.pixels[row][column] = self.light,
                    _ => (), // ignore unrecognized pixels
                }
            }
        }
        Ok(())
    }

    /// Print the picture.
    /// Only regions with the given pixel values are printed.
    /// The '*' character indicates a dark pixel.
    /// The '-' character indicates a light pixel.
    fn print(&self, regions: &BTreeSet<Color>) {
        for row in &self.pixels {
            for pixel in row {
                if regions.contains(pixel) {
                    print!("*");
                } else {
                    print!("-");
                }
            }
            println!("");
        }
    }

    /// Resize the picture to the given number of rows and columnns
    /// and set all pixels to the light value.
    fn erase(&mut self, rows: usize, columns: usize) {
        self.rows = rows;
        self.columns = columns;
        self.pixels = vec![vec![self.light; columns]; rows];
    }

    /// Color the picture.
    /// Replace dark pixels with negative values.
    /// Replace light pixels with positive values.
    /// Each dark or light region is assigned a unique pixel value.
    /// The size of each region is saved.
    /// The sets of pixel values for light and dark regions,
    /// as well as for edge-touching regions, are also saved.
    fn color(&mut self) {
        for urow in 0..self.rows {
            let irow = urow as isize;
            for ucolumn in 0..self.columns {
                let icolumn = ucolumn as isize;
                let pixel_color = self.pixels[urow][ucolumn];
                if pixel_color == self.light {
                    let color = self.light + self.light_regions.len() as Color + 1;
                    self.light_regions.insert(color);
                    let size = self.flood(irow, icolumn, self.light, color);
                    self.region_sizes.insert(color, size);
                } else if pixel_color == self.dark {
                    let color = self.dark - self.dark_regions.len() as Color - 1;
                    self.dark_regions.insert(color);
                    let size = self.flood(irow, icolumn, self.dark, color);
                    self.region_sizes.insert(color, size);
                }
                self.check_edge(urow, ucolumn);
            }
        }
    }

    /// Recursively color a region by filling the pixel in the given row and
    /// column as well as its four nearest neighbors with a new color.
    /// Returns the number of pixels in the region.
    fn flood(&mut self, irow: isize, icolumn: isize, old_color: Color, new_color: Color) -> usize {
        let urow = irow as usize;
        let ucolumn = icolumn as usize;
        let mut size = 0;
        if (0..self.rows).contains(&urow)
            && (0..self.columns).contains(&ucolumn)
            && self.pixels[urow][ucolumn] == old_color
        {
            self.pixels[urow][ucolumn] = new_color;
            size += 1;
            size += self.flood(irow + 1, icolumn, old_color, new_color);
            size += self.flood(irow - 1, icolumn, old_color, new_color);
            size += self.flood(irow, icolumn + 1, old_color, new_color);
            size += self.flood(irow, icolumn - 1, old_color, new_color);
        }
        size
    }

    /// Check whether or not the pixel in the given row and column
    /// is on the edge of the image.
    /// The sets of pixel values for light and dark edge-touching regions
    /// are updated accordingly.
    fn check_edge(&mut self, row: usize, column: usize) {
        if row == 0 || column == 0 || row == self.rows - 1 || column == self.columns - 1 {
            let color = self.pixels[row][column];
            if color >= self.light {
                self.light_edge_regions.insert(color);
            }
            if color <= self.dark {
                self.dark_edge_regions.insert(color);
            }
        }
    }

    /// Returns the set of pixel values for regions that have a size
    /// between the given bounds.
    fn regions_by_size(
        &self,
        regions: &BTreeSet<Color>,
        min_size: usize,
        max_size: usize,
    ) -> BTreeSet<Color> {
        let mut result = BTreeSet::new();
        for color in regions {
            let size = self.region_sizes[color];
            if (min_size..=max_size).contains(&size) {
                result.insert(*color);
            }
        }
        result
    }

    /// Returns the set of pixel values for dark regions that are completely
    /// surrounded by other dark regions.
    /// Note that such a dark region must neighbor only light regions that
    /// do not touch an edge.
    fn surrounded(&mut self) -> BTreeSet<Color> {
        let mut result = BTreeSet::new();
        let light_regions = &self.light_regions - &self.light_edge_regions;
        let dark_regions = &self.dark_regions - &self.dark_edge_regions;
        for urow in 0..self.rows {
            let irow = urow as isize;
            for ucolumn in 0..self.columns {
                let icolumn = ucolumn as isize;
                let pixel_color = self.pixels[urow][ucolumn];
                if dark_regions.contains(&pixel_color) {
                    if self
                        .neighbors(irow, icolumn, pixel_color)
                        .is_subset(&light_regions)
                    {
                        result.insert(pixel_color);
                    }
                    self.flood(irow, icolumn, self.neutral, pixel_color);
                }
            }
        }
        result
    }

    /// Returns the set of pixel values for regions that neighbor
    /// the region of the given row, column, and color.
    /// The color of pixels in the region is changed to neutral.
    /// The caller is responsible for restoring the original color
    /// of the region by calling flood().
    fn neighbors(&mut self, row: isize, column: isize, color: Color) -> BTreeSet<Color> {
        let urow = row as usize;
        let ucolumn = column as usize;
        let mut result = BTreeSet::new();
        if (0..self.rows).contains(&urow) && (0..self.columns).contains(&ucolumn) {
            let pixel_color = self.pixels[urow][ucolumn];
            if pixel_color == color {
                self.pixels[urow][ucolumn] = self.neutral;
                result.append(&mut self.neighbors(row + 1, column, color));
                result.append(&mut self.neighbors(row - 1, column, color));
                result.append(&mut self.neighbors(row, column + 1, color));
                result.append(&mut self.neighbors(row, column - 1, color));
            } else if pixel_color != self.neutral {
                result.insert(pixel_color);
            }
        }
        result
    }
}

/// Parse next argument as an integer.
fn next_usize(lines: &mut std::str::Lines) -> Result<usize> {
    Ok(lines.next().ok_or("missing argument")?.parse::<usize>()?)
}
