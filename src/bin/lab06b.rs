//! Programming Assignment 6: N queens

/// Demonstrate N queens solution.
fn main() {
    for size in 1..9 {
        let board = solve(size);
        println!("placed {} queens on {size} x {size} board", board.len());
        println!("{board:?}");
    }
}

/// A board is a collection of positions as (row, column) tuples.
type Board = Vec<(i32, i32)>;

/// Attempt to place N queens on an NxN board.
/// Return a collection of N positions upon success.
/// Return an empty collection upon failure.
fn solve(size: i32) -> Board {
    let mut board = Board::new();
    solve_recursively(&mut board, size, 0);
    return board;
}

/// Attempt to place a queen in the given row of an NxN board
/// taking into account the positions occupied by other queens.
/// Recursively attempt to place a queen in the next row
/// and backtrack when necessary.
/// Return true upon success.
fn solve_recursively(board: &mut Board, size: i32, row: i32) -> bool {
    for col in 0..size {
        let position = (row, col);
        if is_safe(board, position) {
            board.push(position); // tentatively place queen
            if row + 1 < size {
                if solve_recursively(board, size, row + 1) {
                    return true;
                } else {
                    board.pop(); // backtrack
                }
            } else {
                return true;
            }
        }
    }
    return false;
}

/// Test the safety of placing a queen in the given position
/// taking into account the positions occupied by other queens.
fn is_safe(board: &Board, position: (i32, i32)) -> bool {
    for occupied in board {
        if position.0 == occupied.0
            || position.1 == occupied.1
            || (position.0 - occupied.0).abs() == (position.1 - occupied.1).abs()
        {
            return false;
        }
    }
    return true;
}
