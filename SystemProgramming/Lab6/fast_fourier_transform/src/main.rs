
use battery::{Manager, State};
use num_complex::Complex;
use std::f64::consts::PI;

fn fft(input: &[Complex<f64>]) -> Vec<Complex<f64>> {
    let n = input.len();
    if n <= 1 {
        return input.to_vec();
    }

    // Перевірка, чи є n степенем двійки
    assert!(n.is_power_of_two(), "Кількість точок повинна бути степенем двійки.");

    let even: Vec<_> = input.iter().step_by(2).cloned().collect();
    let odd: Vec<_> = input.iter().skip(1).step_by(2).cloned().collect();

    let even_fft = fft(&even);
    let odd_fft = fft(&odd);

    let mut result = vec![Complex::new(0.0, 0.0); n];
    for k in 0..n / 2 {
        let t = Complex::new(0.0, -2.0 * PI * k as f64 / n as f64).exp() * odd_fft[k];
        result[k] = even_fft[k] + t;
        result[k + n / 2] = even_fft[k] - t;
    }

    result
}

fn main() {
    /*
    let manager = Manager::new().expect("Unable to create battery manager");
    println!("Before Execution:\n------------------");
    for (i, maybe_battery) in manager.batteries().unwrap().enumerate() {
        let battery = maybe_battery.expect("Unable to access battery information");
        println!("Battery {}:", i + 1);
        println!("State: {:?}", battery.state());
        println!("Energy: {:.10} Wh", battery.energy().get::<battery::units::energy::watt_hour>());
        println!("Energy Full: {:.10} Wh", battery.energy_full().get::<battery::units::energy::watt_hour>());
        println!("Percentage: {:.10} %", battery.state_of_charge().get::<battery::units::ratio::percent>());
    }
     */
    let n = 2048*2048; // Кількість точок, степінь двійки 2^11
    let mut points = Vec::new();

    // Генеруємо вхідні точки
    for t in 0..n {
        points.push(Complex::new((2.0 * PI * t as f64 / n as f64).sin(), 0.0));
    }

    let fft_result = fft(&points);

    let mut sum_re = 0.0;
    let mut sum_im = 0.0;
    for value in fft_result {
        sum_re += value.re;
        sum_im += value.im;
    }
    println!("Code Output:\n");
    println!("Real: {}", sum_re);
    println!("Imaginary: {}", sum_im);
    /*
    println!("After Execution:\n------------------");
    for (i, maybe_battery) in manager.batteries().unwrap().enumerate() {
        let battery = maybe_battery.expect("Unable to access battery information");
        println!("Battery {}:", i + 1);
        println!("State: {:?}", battery.state());
        println!("Energy: {:.10} Wh", battery.energy().get::<battery::units::energy::watt_hour>());
        println!("Energy Full: {:.10} Wh", battery.energy_full().get::<battery::units::energy::watt_hour>());
        println!("Percentage: {:.10} %", battery.state_of_charge().get::<battery::units::ratio::percent>());
    }
     */
}
