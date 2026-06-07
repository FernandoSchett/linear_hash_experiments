#pragma once

#include <cstddef>
#include <cstdint>

struct HashStats {
    std::size_t pageSize = 0;
    double alphaMax = 0.0;
    std::size_t initialBuckets = 0;
    std::size_t primaryBuckets = 0;
    std::size_t overflowPages = 0;
    std::size_t totalPages = 0;
    std::size_t totalRecords = 0;
    double loadFactorGlobal = 0.0;
    double realSpaceUtilization = 0.0;
    double overflowPagePercentage = 0.0;
    std::size_t numSplits = 0;
    std::size_t level = 0;
    std::size_t splitPointer = 0;
    uint64_t totalPageAccesses = 0;
};
