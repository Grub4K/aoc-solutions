use crate::result::RunResult;
use std::convert::TryFrom;
use std::error::Error;
use std::fmt::Display;
use std::fs::File;
use std::io::BufReader;

pub type Lines = std::io::Lines<BufReader<File>>;
pub type RunReturn = Result<RunResult, Box<dyn Error>>;
pub type RunnerFunctionType = fn(Lines, Part) -> Result<RunResult, Box<dyn Error>>;

#[derive(Debug)]
pub enum Part {
    A = 1,
    B = 2,
    Both = 3,
}

impl TryFrom<String> for Part {
    type Error = String;

    fn try_from(v: String) -> Result<Self, Self::Error> {
        if v.len() != 1 {
            return Err("Part specifier must be 1 character long".to_string());
        }

        match v.as_bytes()[0] {
            b'a' | b'A' => Ok(Part::A),
            b'b' | b'B' => Ok(Part::B),
            b'*' => Ok(Part::Both),
            _ => Err("Invalid part specifier".to_string()),
        }
    }
}

#[derive(Debug)]
pub struct RuntimeError<'a> {
    message: &'a str,
}

impl<'a> RuntimeError<'a> {
    pub fn new(message: &'a str) -> Self {
        RuntimeError { message }
    }
}

impl Display for RuntimeError<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        self.message.fmt(f)
    }
}

impl Error for RuntimeError<'_> {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        None
    }

    fn description(&self) -> &str {
        "description() is deprecated; use Display"
    }

    fn cause(&self) -> Option<&dyn Error> {
        self.source()
    }
}

pub struct Run {
    pub id: String,
    pub part: Part,
    pub filename: String,
}

pub struct Runs {
    args: std::env::Args,
}

impl Runs {
    pub fn new() -> Runs {
        let mut args = std::env::args();
        args.next();
        Runs { args }
    }
}

impl Iterator for Runs {
    type Item = Result<Run, String>;

    fn next(&mut self) -> Option<Self::Item> {
        let (Some(id), Some(part), Some(filename)) =
            (self.args.next(), self.args.next(), self.args.next())
        else {
            return None;
        };
        Some(match part.try_into() {
            Ok(part) => Ok(Run { id, part, filename }),
            Err(err) => Err(err),
        })
    }
}
