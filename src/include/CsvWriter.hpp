#pragma once

#include <cstdint>
#include <string>

struct ExperimentResult {
    std::string experimentId;
    std::size_t pageSizeP = 0;
    double alphaMax = 0.0;
    uint64_t seed = 0;
    std::size_t numInsertedRecords = 0;
    std::size_t numSuccessfulSearches = 0;
    std::size_t numUnsuccessfulSearches = 0;
    std::size_t initialBuckets = 0;
    std::size_t finalPrimaryBuckets = 0;
    std::size_t finalOverflowPages = 0;
    std::size_t finalTotalPages = 0;
    std::size_t finalTotalRecords = 0;
    double finalLoadFactorGlobal = 0.0;
    double realSpaceUtilization = 0.0;
    double overflowPagePercentage = 0.0;
    std::size_t numSplits = 0;
    std::size_t finalLevel = 0;
    std::size_t finalSplitPointer = 0;
    uint64_t insertTotalPageAccesses = 0;
    double insertAvgPageAccesses = 0.0;
    uint64_t successfulSearchTotalPageAccesses = 0;
    double successfulSearchAvgPageAccesses = 0.0;
    uint64_t unsuccessfulSearchTotalPageAccesses = 0;
    double unsuccessfulSearchAvgPageAccesses = 0.0;
    double insertRuntimeMs = 0.0;
    double successfulSearchRuntimeMs = 0.0;
    double unsuccessfulSearchRuntimeMs = 0.0;
    double totalRuntimeMs = 0.0;
};

class CsvWriter {
public:
    static void writeSingleResult(const std::string& path, const ExperimentResult& result);
};
