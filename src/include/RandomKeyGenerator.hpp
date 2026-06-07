#pragma once

#include <cstddef>
#include <cstdint>
#include <random>
#include <unordered_set>
#include <vector>

class RandomKeyGenerator {
public:
    explicit RandomKeyGenerator(uint64_t seed);

    uint64_t nextUniqueKey();
    std::vector<uint64_t> generateUniqueKeys(std::size_t count);
    std::vector<uint64_t> sampleExistingKeys(const std::vector<uint64_t>& keys, std::size_t count);
    std::vector<uint64_t> generateAbsentKeys(std::size_t count);

private:
    std::mt19937_64 rng_;
    std::unordered_set<uint64_t> generated_;
};
