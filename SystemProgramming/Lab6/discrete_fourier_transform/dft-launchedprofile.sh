#!/bin/bash

cargo build --release

./target/release/discrete_fourier_transform & APP_PID=$!

sample $APP_PID -file dft-output.prof

