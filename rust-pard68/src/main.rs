#![feature(vec_remove_item)]
use std::env;
use std::fs::File;
use std::io::{prelude::*, BufReader};
use std::time;


fn value_of(word: &String) -> isize {
    let VALUES: Vec<isize> = vec![1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3,
                    1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10];
    let mut value: isize = 0;
    for c in word.chars() {
        value += VALUES[c as usize - 97];
    }
    value
}

fn contains(word: &String, tiles: &String) -> bool {
    let mut word_bytes = word.clone().into_bytes();
    let tiles_bytes = tiles.clone().into_bytes();
    for byte in tiles_bytes {
        word_bytes.remove_item(&byte);
    }
    word_bytes.is_empty()
}


fn find_best(path: String, tiles: String) -> String {
    let mut best = "a".to_string();
    let mut best_score = 0;
    let max = value_of(&tiles);
    let file = File::open(path).unwrap();
    let reader = BufReader::new(file);
    for line in reader.lines() {
        let word = line.unwrap();
        if word.len() <= tiles.len() {
            if value_of(&word) > best_score {
                if contains(&word, &tiles) {
                    best = word;
                    best_score = value_of(&best);
                }
            }
        }
        if best_score == max {
            return best
        }
    }
    best
}

fn main() {
    let start = time::Instant::now();
    let best = find_best("../data/dictionary.txt".to_string(), env::args().nth(1).unwrap().to_string());
    let elapsed = start.elapsed();
    let ms = ((elapsed.as_secs() as f64) + (elapsed.subsec_nanos() as f64 / 1_000_000_000.0)) * 1000.0;
    println!("pard68, Rust, {}, {}, {}, Give me `iter()` or give me death", &best, value_of(&best), ms)
}

