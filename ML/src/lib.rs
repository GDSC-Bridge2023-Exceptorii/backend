use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn ML(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    Ok(())
}

use discorec::{Dataset, Recommender};

let mut data = Dataset::new();
// using synthetic data

// combine both koreans and japanese
// most elderly want to learn banking and payment first, then others.

data.push("user_a", "banking", 5.0);
data.push("user_a", "google", 3.5);
data.push("user_a", "maps", 3.2);
data.push("user_b", "banking", 4.8);

data.push("user_b", "google", 4.0);
data.push("user_b", "maps", 3.5);

data.push("user_c", "banking", 5.0);
data.push("user_c", "google", 4.6);
data.push("user_c", "maps", 2.8);

data.push("user_d", "banking", 4.5);
data.push("user_d", "google", 3.2);
data.push("user_d", "maps", 5.0);

data.push("user_e", "banking", 4.0);
data.push("user_e", "google", 3.5);
data.push("user_e", "maps", 4.2);

data.push("user_f", "banking", 4.6);
data.push("user_f", "google", 2.8);
data.push("user_f", "maps", 4.0);

data.push("user_g", "banking", 5.0);
data.push("user_g", "google", 3.2);
data.push("user_g", "maps", 4.5);

data.push("user_h", "banking", 4.0);
data.push("user_h", "google", 5.0);
data.push("user_h", "maps", 3.5);

data.push("user_i", "banking", 4.2);
data.push("user_i", "google", 4.0);
data.push("user_i", "maps", 4.8);

data.push("user_j", "banking", 3.8);
data.push("user_j", "google", 4.6);
data.push("user_j", "maps", 5.0);

struct Recommendation {
    item_rec: String,
    predicted_rating: f32,
}


// make a function to get a new user and recommend them item
#[pyfunction]
fn get_recommendation(user: &str, item: &str, ranking: f32) -> PyResult<Recommendation> {
    data = data;
    data.push(user, item, ranking);
    let recommender = Recommender::fit_explicit(&data);
    let mut Recommendation::item_rec = recommender.item_recs(&item_id, 1);
    let mut Recommendation::predicted_rating = recommender.predict(&user, Recommendation::item_rec);
    return Recommendation
}

fn main() {
    get_recommendation("user_k", "banking", 5.0)
}

