#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <cstdint>

using namespace std;

// Simple sieve to generate primes up to limit
vector<int> sieve_primes(int limit) {
    vector<bool> is_prime(limit + 1, true);
    is_prime[0] = is_prime[1] = false;
    
    for (int p = 2; p * p <= limit; p++) {
        if (is_prime[p]) {
            for (int mult = p * p; mult <= limit; mult += p) {
                is_prime[mult] = false;
            }
        }
    }
    
    vector<int> primes;
    for (int p = 2; p <= limit; p++) {
        if (is_prime[p]) {
            primes.push_back(p);
        }
    }
    return primes;
}

// Check if all prime factors of i are greater than k
// Strategy: divide out all primes <= k, if remainder > k then we're good
bool largest_prime_gt_k(int64_t i, int k, const vector<int>& primes) {
    for (int p : primes) {
        if (p > k) {
            return true;
        }
        while (i % p == 0) {
            i /= p;
            if (i <= k) {
                return false;
            }
        }
    }
    // If we've exhausted all primes and i > k, then i > k is a prime or
    // product of primes all > k
    return i > k;
}

int main() {
    const int MAX_K = 1000;
    
    cout << "Generating primes up to " << MAX_K << "..." << endl;
    vector<int> primes = sieve_primes(MAX_K);
    cout << "Generated " << primes.size() << " primes" << endl;
    
    int64_t m = 1;
    vector<int> k_seq;
    vector<int64_t> m_seq;
    vector<double> logm_k_seq;
    
    for (int k = 1; k < MAX_K; k++) {
        while (true) {
            bool working = true;
            
            // Check from highest to lowest to improve skip-ahead
            for (int64_t i = m + k; i > m; i--) {
                if (!largest_prime_gt_k(i, k, primes)) {
                    working = false;
                    m = i - 1;  // Skip ahead
                    break;
                }
            }
            
            if (working) {
                k_seq.push_back(k);
                m_seq.push_back(m);
                
                cout << "k=" << k << ": m=" << m << endl;
                
                if (k > 1) {
                    logm_k_seq.push_back(log(m) / log(k));
                }
                break;
            }
            m++;
        }
    }
    
    // Write results to file for plotting
    ofstream outfile("erdos_962_results.csv");
    outfile << "k,m,logm_k" << endl;
    for (size_t i = 0; i < k_seq.size(); i++) {
        outfile << k_seq[i] << "," << m_seq[i];
        if (i > 0) {  // logm_k starts from k=2
            outfile << "," << logm_k_seq[i-1];
        }
        outfile << endl;
    }
    outfile.close();
    
    // Print sequence
    cout << "\nSequence (first 50 terms):" << endl;
    for (size_t i = 0; i < min(size_t(50), m_seq.size()); i++) {
        if (i > 0) cout << ",";
        cout << m_seq[i];
    }
    cout << endl;
    
    cout << "\nComputed " << k_seq.size() << " terms" << endl;
    cout << "Results written to erdos_962_results.csv" << endl;
    
    return 0;
}