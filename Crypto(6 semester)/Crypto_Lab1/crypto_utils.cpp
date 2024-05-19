#include "crypto_utils.h"


typedef unsigned long long ll;
using namespace std;

ll pow_mod(ll a, ll b, ll m) {
    ll res = 1;
    while (b > 0) {
        if (b & 1) res = res * a % m;
        a = a * a % m;
        b >>= 1;
    }
    return res;
}

bool is_prime_mr(ll p, int iterations) {
    if (p < 4) return p > 1;
    if (!(p & 1)) return false;

    ll d = p - 1;
    while ((d & 1) == 0) d >>= 1;

    random_device rd;
    mt19937_64 gen(rd());
    uniform_int_distribution<ll> dist(2, p - 2);

    for (int i = 0; i < iterations; ++i) {
        ll a = dist(gen);
        ll x = pow_mod(a, d, p);
        if (x == 1 || x == p - 1) continue;

        bool pass = false;
        for (; d != p - 1; d <<= 1) {
            x = x * x % p;
            if (x == 1) return false;
            if (x == p - 1) {
                pass = true;
                break;
            }
        }
        if (!pass) return false;
    }
    return true;
}

int symbol_jacobi(long long a, long long b) {
    if (b <= 0 || (b & 1) == 0) return 0;
    int s = 1;
    if (a < 0) {
        a = -a;
        if (b % 4 == 3) s = -s;
    }
    while (a != 0) {
        while ((a & 1) == 0) {
            a >>= 1;
            if (b % 8 == 3 || b % 8 == 5) s = -s;
        }
        swap(a, b);
        if (a % 4 == 3 && b % 4 == 3) s = -s;
        a %= b;
    }
    return (b == 1) ? s : 0;
}

bool lucas_test(ll n, long long D, ll P, ll Q) {
    ll d = n + 1, s = 0;
    while ((d & 1) == 0) {
        s++;
        d >>= 1;
    }

    ll U = 1, V = P, Qk = Q, Qm = Q;
    for (ll mask = 1ULL << (63 - __builtin_clzll(d)); mask; mask >>= 1) {
        U = U * V % n;
        V = (V * V + Qk * U * U) % n;
        Qk = Qk * Qk % n;

        if (d & mask) {
            U = (U * P + V) % n;
            V = (V * V + D * U * U) % n;
            Qk = Qk * Q % n;
        }
    }

    if (U == 0 || V == 0) return true;
    for (ll i = 0; i < s; ++i) {
        V = (V * V - 2 * Qk) % n;
        if (V == 0) return true;
        Qk = Qk * Qk % n;
    }

    return false;
}

bool prime_test_bpsw(ll n) {
    if (n < 2) return false;
    if (n < 4 || n % 2 == 0) return n == 2;

    if (!is_prime_mr(n, 1)) return false;

    long long D = 5, sign = 1;
    while (symbol_jacobi(D, n) != -1) {
        D = D + sign * 2;
        sign = -sign;
    }

    return lucas_test(n, D, 1, (1 - D) / 4);
}

string convert_to_base(ll num, int base) {
    if (base == 2) return bitset<64>(num).to_string();
    else if (base == 10) return to_string(num);
    else if (base == 64) {
        const char* chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
        string result;
        do {
            result = chars[num % 64] + result;
            num /= 64;
        } while (num);
        return result.empty() ? "0" : result;
    }
    return "";  // Default case for unexpected base
}

vector<ll> get_primes(int bits) {
    vector<ll> primes;
    ll start = 1ULL << (bits - 1);
    ll finish = (1ULL << bits) - 1;
    for (ll candidate = start; candidate <= finish; ++candidate) {
        if (is_prime_mr(candidate, 100)) primes.push_back(candidate);
    }
    return primes;
}
