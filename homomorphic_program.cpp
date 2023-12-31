#include <iostream>
#include "./SEAL/seal/bigpoly.h"

int main() {
    // Initialize SEAL context and keys
    seal::EncryptionParameters parms(seal::scheme_type::BFV);
    parms.set_poly_modulus_degree(4096);
    parms.set_coeff_modulus(seal::coeff_modulus_128(4096));
    parms.set_plain_modulus(40961);
    auto context = seal::SEALContext::Create(parms);
    auto secret_key = seal::SecretKey::Create(context);
    auto public_key = seal::PublicKey::Create(context);

    // Create encryptor and evaluator
    auto encryptor = std::make_shared<seal::Encryptor>(context, public_key);
    auto evaluator = std::make_shared<seal::Evaluator>(context);

    // Step 1: Homomorphic Hiding
    int a, b;
    std::cout << "Enter the value of 'a': ";
    std::cin >> a;

    std::cout << "Enter the value of 'b': ";
    std::cin >> b;

    int c = a + b;

    // Encrypt values a and b
    seal::Plaintext plain_a(std::to_string(a));
    seal::Plaintext plain_b(std::to_string(b));
    seal::Ciphertext encrypted_a, encrypted_b;
    encryptor->encrypt(plain_a, encrypted_a);
    encryptor->encrypt(plain_b, encrypted_b);

    // Perform homomorphic addition
    seal::Ciphertext encrypted_sum;
    evaluator->add(encrypted_a, encrypted_b, encrypted_sum);

    // Encrypt value c for comparison
    seal::Plaintext plain_c(std::to_string(c));
    seal::Ciphertext encrypted_c;
    encryptor->encrypt(plain_c, encrypted_c);

    // Compare encrypted sum and encrypted c
    bool proof_accepted = encrypted_sum == encrypted_c;

    if (proof_accepted) {
        std::cout << "Receiver accepts sender's proof." << std::endl;
    } else {
        std::cout << "Receiver rejects sender's proof." << std::endl;
    }

    return 0;
}
