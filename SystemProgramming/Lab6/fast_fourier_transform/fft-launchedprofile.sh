#!/bin/bash

cargo build --release
sleep 1
./target/release/fast_fourier_transform & APP_PID=$!

sample $APP_PID -file fft-output.prof
