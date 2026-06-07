#pragma once

#include <cstddef>
#include <cstdint>
#include <string>

struct ExperimentConfig {
    std::string experimentId;
    std::size_t pageSize = 0;
    double alphaMax = 0.0;
    std::size_t initialBuckets = 0;
    std::size_t numRecords = 0;
    std::size_t numSuccessfulSearches = 0;
    std::size_t numUnsuccessfulSearches = 0;
    uint64_t seed = 0;
    std::string outputCsv;

    static ExperimentConfig loadFromFile(const std::string& path);
};
