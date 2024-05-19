//
// Created by Fedorych Andriy on 19/5/24.
//

#ifndef CRYPTO_UTILS_H
#define CRYPTO_UTILS_H

#include <iostream>
#include <string>
#include <vector>
#include <bitset>
#include <sstream>
#include <iomanip>
#include <random>

typedef unsigned long long ll;
using namespace std;

string convert_to_base(ll num, int base);

int symbol_jacobi(long long a, long long b);
ll pow_mod(ll a, ll b, ll m);
vector<ll> get_primes(int bits);



bool is_prime_mr(ll n, int iterations);
bool prime_test_bpsw(ll n);
bool lucas_test(ll n, long long D, ll P, ll Q);

#endif // CRYPTO_UTILS_H
