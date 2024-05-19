#include "crypto_utils.h"

int main() {
    while (true) {
        cout << "-----------------------------------------------\n";
        cout << "Enter number: 1 - start interaction, 0 - exit: ";
        int choice;
        cin >> choice;
        if (choice == 0) {
            break; // Exit the loop and the program
        }
        ll base, exponent, modulus, n;
        int k, bits;
        vector<ll> primes;

        cout << "Enter base for modular exponentiation: ";
        cin >> base;
        cout << "Enter exponent: ";
        cin >> exponent;
        cout << "Enter modulus: ";
        cin >> modulus;
        cout << "Modular Exponentiation Result: " << pow_mod(base, exponent, modulus) << endl;

        cout << "Enter number to test for primality: ";
        cin >> n;
        cout << "Enter number of iterations for Miller-Rabin Test: ";
        cin >> k;
        if (is_prime_mr(n, k))
            cout << n << " is prime." << endl;
        else
            cout << n << " is not prime." << endl;

        if (prime_test_bpsw(n))
            cout << n << " is definitely prime." << endl;
        else
            cout << n << " is not prime." << endl;

        cout << "Base2: " << convert_to_base(n, 2) << endl;
        cout << "Base10: " << convert_to_base(n, 10) << endl;
        cout << "Base64: " << convert_to_base(n, 64) << endl;

        cout << "Enter number of bits for prime generation: ";
        cin >> bits;
        primes = get_primes(bits);
        cout << "Primes with " << bits << " bits:" << endl;
        for (ll prime : primes) {
            cout << prime << endl;
        }
    }

    return 0;
}
