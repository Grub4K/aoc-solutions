mod result;
mod types;
mod years;

use std::error::Error;
use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;

use crate::result::RunResult;
use crate::types::{Run, Runs, RuntimeError};
use years::build_lookup;

fn execute(run: Result<Run, String>) -> Result<RunResult, Box<dyn Error>> {
    let run = run?;

    let file = File::open(run.filename)?;

    let lookup = build_lookup();
    let runner = lookup
        .get(run.id.as_str())
        .ok_or_else(|| RuntimeError::new("Invalid identifier"))?;
    runner(BufReader::new(file).lines(), run.part)
}

fn main() {
    for run in Runs::new() {
        match execute(run) {
            Ok(result) => {
                println!("res, {}, {}", result.a, result.b);
            }
            Err(message) => {
                println!("err, {}", message);
                continue;
            }
        }
    }
}
