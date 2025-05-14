//! Programming Assignment 3: A simple interactive game

use std::cmp;
use std::io;
use std::io::Write;

/// Play the game.
fn main() {
    let start = 21;
    let mut stones = start;
    while stones > 0 {
        stones -= them(stones, start);
        if stones == 0 {
            println!("You took the last stone. You lose.");
        } else {
            stones -= us(stones);
            if stones == 0 {
                println!("I took the last stone. I lose.");
            }
        }
    }
}

/// Human takes a turn.
fn them(stones: i32, start: i32) -> i32 {
    println!("There are {stones} stones");
    let mut buffer = String::new();
    loop {
        buffer.clear();
        print!("How many do you take? ");
        io::stdout().flush().ok();
        io::stdin().read_line(&mut buffer).ok();
        if let Ok(take) = buffer.trim().parse::<i32>() {
            if take == 0 && stones == start {
                println!("In that case I will go first");
                return take;
            } else if take < 1 {
                println!("You must take a stone");
            } else if take > 3 {
                println!("You cannot take more than 3 stones");
            } else if take > stones {
                println!("There are only {stones} stones");
            } else {
                return take;
            }
        } else {
            println!("I do not understand \"{}\"", buffer.trim());
        }
    }
}

/// Computer takes a turn.
fn us(stones: i32) -> i32 {
    let take = cmp::max(1, (stones - 1) % 4);
    println!("I take {take} stones");
    take
}
