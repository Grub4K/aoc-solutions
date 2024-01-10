use std::fmt::Display;

macro_rules! map_numeric {
    ($macro_name:ident $($params:tt)* ) => {
        $macro_name!(u8 $($params)*);
        $macro_name!(u16 $($params)*);
        $macro_name!(u32 $($params)*);
        $macro_name!(u64 $($params)*);
        $macro_name!(u128 $($params)*);
        $macro_name!(usize $($params)*);
        $macro_name!(i8 $($params)*);
        $macro_name!(i16 $($params)*);
        $macro_name!(i32 $($params)*);
        $macro_name!(i64 $($params)*);
        $macro_name!(i128 $($params)*);
        $macro_name!(isize $($params)*);
    };
}

#[derive(Debug)]
pub enum PartResult {
    Int(u128),
    Str(String),
}

impl Display for PartResult {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            PartResult::Int(value) => value.fmt(f),
            PartResult::Str(value) => value.fmt(f),
        }
    }
}

macro_rules! impl_part_result {
    () => {
        map_numeric!(impl_part_result);
    };
    ($t:ty) => {
        impl From<$t> for PartResult {
            fn from(item: $t) -> Self {
                PartResult::Int(item as u128)
            }
        }
    };
}
impl_part_result!();

impl From<String> for PartResult {
    fn from(item: String) -> Self {
        PartResult::Str(item)
    }
}

pub struct RunResult {
    pub a: PartResult,
    pub b: PartResult,
}

macro_rules! impl_run_result {
    () => {
        map_numeric!(impl_run_result);
        impl_run_result!(String);
    };
    ($t:ty) => {
        map_numeric!(impl_run_result, $t);
        impl_run_result!(String, $t);
    };
    ($t:ty, $u: ty) => {
        impl From<($t, $u)> for RunResult {
            fn from((a, b): ($t, $u)) -> Self {
                RunResult {
                    a: a.into(),
                    b: b.into(),
                }
            }
        }
    };
}
impl_run_result!();
