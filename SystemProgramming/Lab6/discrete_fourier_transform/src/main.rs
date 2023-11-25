use std::f64::consts::PI;
use num_complex::Complex;
use battery::{Manager, State};

fn dft(points: &[Complex<f64>]) -> Vec<Complex<f64>> {
    let n = points.len();
    let mut result = Vec::with_capacity(n);


    for k in 0..n {
        let mut sum = Complex::new(0.0, 0.0);
        for (t, &x) in points.iter().enumerate() {
            let angle = 2.0 * PI * k as f64 * t as f64 / n as f64;

            sum = sum + x * Complex::new(angle.cos(), -angle.sin());

        }
        result.push(sum);
    }



    result
}


fn main() {

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
    let n = 2048 * 2048; // Кількість точок 2^33
    let mut points = Vec::new();



    // Генеруємо вхідні точки
    for t in 0..n {
        // Можна згенерувати будь-які дані, наприклад, синусоїду
        points.push(Complex::new((2.0 * PI * t as f64 / n as f64).sin(), 0.0));
    }


    let dft_result = dft(&points);


    let mut sum_re = 0.0;
    let mut sum_im = 0.0;
    for value in dft_result {
        sum_re += value.re;
        sum_im += value.im;
    }
    println!("Code Output:\n");
    println!("Real: {}", sum_re);
    println!("Imaginary: {}", sum_im);
    println!("After Execution:\n------------------");
    for (i, maybe_battery) in manager.batteries().unwrap().enumerate() {
        let battery = maybe_battery.expect("Unable to access battery information");
        println!("Battery {}:", i + 1);
        println!("State: {:?}", battery.state());
        println!("Energy: {:.10} Wh", battery.energy().get::<battery::units::energy::watt_hour>());
        println!("Energy Full: {:.10} Wh", battery.energy_full().get::<battery::units::energy::watt_hour>());
        println!("Percentage: {:.10} %", battery.state_of_charge().get::<battery::units::ratio::percent>());
    }
}
