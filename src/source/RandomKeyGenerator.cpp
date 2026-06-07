#include "RandomKeyGenerator.hpp"

#include <algorithm>
#include <stdexcept>

RandomKeyGenerator::RandomKeyGenerator(uint64_t seed)
    : rng_(seed) {}

uint64_t RandomKeyGenerator::nextUniqueKey() {
    uint64_t key = 0;
    do {
        key = rng_();
    } while (generated_.find(key) != generated_.end());

    generated_.insert(key);
    return key;
}

std::vector<uint64_t> RandomKeyGenerator::generateUniqueKeys(std::size_t count) {
    std::vector<uint64_t> keys;
    keys.reserve(count);
    for (std::size_t i = 0; i < count; ++i) {
        keys.push_back(nextUniqueKey());
    }
    return keys;
}

std::vector<uint64_t> RandomKeyGenerator::sampleExistingKeys(const std::vector<uint64_t>& keys,
                                                             std::size_t count) {
    if (count > keys.size()) {
        throw std::runtime_error("amostra maior que o conjunto de chaves existentes");
    }

    std::vector<uint64_t> sample = keys;
    std::shuffle(sample.begin(), sample.end(), rng_);
    sample.resize(count);
    return sample;
}

std::vector<uint64_t> RandomKeyGenerator::generateAbsentKeys(std::size_t count) {
    return generateUniqueKeys(count);
}
