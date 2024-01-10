use crate::types::RunnerFunctionType;
use std::collections::HashMap;

pub fn build_lookup() -> HashMap<&'static str, RunnerFunctionType> {
    let years = HashMap::<&str, RunnerFunctionType>::new();

    years
}
