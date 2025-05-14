//! Programming Assignment 3: A simulation of a predator prey system

fn main() {
    let mut rabbits = 10.0; // Ten rabbits excape in month 0
    let mut coyotes = 0.0;
    let mut last_month = 300;
    let mut stop = false;

    for month in 0..last_month {
        if stop {
            last_month = month;
            break;
        }
        if month == 50 {
            coyotes += 10.0; // Ten coyotes are released in month 50
        }
        print_line(month, rabbits, coyotes);
        (stop, rabbits, coyotes) = update(rabbits, coyotes);
    }
    print_line(last_month, rabbits, coyotes);
    println!(
        "In month {} there are {} rabbits and {} coyotes",
        last_month, rabbits, coyotes
    );
}

/// Print one line of a graphical display of rabbit and coyote populations.
fn print_line(month: i32, rabbits: f64, coyotes: f64) {
    if month % 3 != 0 {
        return;
    }
    let rabbit_column = (1e-2 * rabbits).round() as usize;
    let coyote_column = (2.0 * coyotes).round() as usize;
    if rabbit_column < coyote_column {
        println!(
            "{0:>1$}|{2:>3$}{4:>5$}",
            month,
            3,
            "r",
            rabbit_column + 1,
            "c",
            coyote_column - rabbit_column
        );
    } else if coyote_column < rabbit_column {
        println!(
            "{0:>1$}|{2:>3$}{4:>5$}",
            month,
            3,
            "c",
            coyote_column + 1,
            "r",
            rabbit_column - coyote_column
        );
    } else {
        println!("{0:>1$}|{2:>3$}", month, 3, "r", rabbit_column + 1);
    }
}

/// Update rabbit and coyote populations.
fn update(old_rabbits: f64, old_coyotes: f64) -> (bool, f64, f64) {
    let rabbits = new_rabbits(old_rabbits, old_coyotes);
    let coyotes = new_coyotes(old_rabbits, old_coyotes);
    let stop = small_change(old_rabbits, rabbits) && small_change(old_coyotes, coyotes);
    (stop, rabbits, coyotes)
}

/// Number of rabbits alive in a new month
/// given the number of rabbits and coyotes alive in the previous month.
fn new_rabbits(old_rabbits: f64, old_coyotes: f64) -> f64 {
    let births = 2e-1 * old_rabbits;
    let starvation_deaths = 2e-5 * old_rabbits * old_rabbits;
    let other_deaths = 4.5e-3 * old_coyotes * old_rabbits;
    old_rabbits + births - starvation_deaths - other_deaths
}

/// Number of coyotes alive in a new month
/// given the number of rabbits and coyotes alive in the previous month.
fn new_coyotes(old_rabbits: f64, old_coyotes: f64) -> f64 {
    let births = 8e-2 * old_coyotes;
    let starvation_deaths = 2.5e2 * old_coyotes / old_rabbits;
    old_coyotes + births - starvation_deaths
}

/// Determine if a change is smaller than 1%
fn small_change(old: f64, new: f64) -> bool {
    (new - old).abs() < 1e-2 * old.abs()
}
