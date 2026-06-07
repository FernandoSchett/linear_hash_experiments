#include "ExperimentRunner.hpp"

#include "CsvWriter.hpp"
#include "LinearHashing.hpp"
#include "RandomKeyGenerator.hpp"

#include <chrono>
#include <stdexcept>
#include <vector>

namespace {

using Clock = std::chrono::steady_clock;

double elapsedMs(Clock::time_point begin, Clock::time_point end) {
    return std::chrono::duration<double, std::milli>(end - begin).count();
}

double average(uint64_t total, std::size_t count) {
    return count == 0 ? 0.0 : static_cast<double>(total) / static_cast<double>(count);
}

} // namespace

ExperimentRunner::ExperimentRunner(ExperimentConfig config)
    : config_(std::move(config)) {}

void ExperimentRunner::run() {
    RandomKeyGenerator generator(config_.seed);
    LinearHashing hash(config_.pageSize, config_.alphaMax, config_.initialBuckets);

    const auto totalBegin = Clock::now();
    std::vector<uint64_t> insertedKeys = generator.generateUniqueKeys(config_.numRecords);

    uint64_t insertAccesses = 0;
    const auto insertBegin = Clock::now();
    for (uint64_t key : insertedKeys) {
        hash.insert(key);
        insertAccesses += hash.getLastOperationPageAccesses();
    }
    const auto insertEnd = Clock::now();

    const std::vector<uint64_t> successfulKeys =
        generator.sampleExistingKeys(insertedKeys, config_.numSuccessfulSearches);

    uint64_t successfulAccesses = 0;
    const auto successfulBegin = Clock::now();
    for (uint64_t key : successfulKeys) {
        if (!hash.contains(key)) {
            throw std::runtime_error("chave existente nao encontrada durante experimento");
        }
        successfulAccesses += hash.getLastOperationPageAccesses();
    }
    const auto successfulEnd = Clock::now();

    const std::vector<uint64_t> absentKeys =
        generator.generateAbsentKeys(config_.numUnsuccessfulSearches);

    uint64_t unsuccessfulAccesses = 0;
    const auto unsuccessfulBegin = Clock::now();
    for (uint64_t key : absentKeys) {
        if (hash.contains(key)) {
            throw std::runtime_error("chave inexistente encontrada durante experimento");
        }
        unsuccessfulAccesses += hash.getLastOperationPageAccesses();
    }
    const auto unsuccessfulEnd = Clock::now();
    const auto totalEnd = Clock::now();

    const HashStats stats = hash.getStats();

    ExperimentResult result;
    result.experimentId = config_.experimentId;
    result.pageSizeP = config_.pageSize;
    result.alphaMax = config_.alphaMax;
    result.seed = config_.seed;
    result.numInsertedRecords = config_.numRecords;
    result.numSuccessfulSearches = config_.numSuccessfulSearches;
    result.numUnsuccessfulSearches = config_.numUnsuccessfulSearches;
    result.initialBuckets = config_.initialBuckets;
    result.finalPrimaryBuckets = stats.primaryBuckets;
    result.finalOverflowPages = stats.overflowPages;
    result.finalTotalPages = stats.totalPages;
    result.finalTotalRecords = stats.totalRecords;
    result.finalLoadFactorGlobal = stats.loadFactorGlobal;
    result.realSpaceUtilization = stats.realSpaceUtilization;
    result.overflowPagePercentage = stats.overflowPagePercentage;
    result.numSplits = stats.numSplits;
    result.finalLevel = stats.level;
    result.finalSplitPointer = stats.splitPointer;
    result.insertTotalPageAccesses = insertAccesses;
    result.insertAvgPageAccesses = average(insertAccesses, config_.numRecords);
    result.successfulSearchTotalPageAccesses = successfulAccesses;
    result.successfulSearchAvgPageAccesses =
        average(successfulAccesses, config_.numSuccessfulSearches);
    result.unsuccessfulSearchTotalPageAccesses = unsuccessfulAccesses;
    result.unsuccessfulSearchAvgPageAccesses =
        average(unsuccessfulAccesses, config_.numUnsuccessfulSearches);
    result.insertRuntimeMs = elapsedMs(insertBegin, insertEnd);
    result.successfulSearchRuntimeMs = elapsedMs(successfulBegin, successfulEnd);
    result.unsuccessfulSearchRuntimeMs = elapsedMs(unsuccessfulBegin, unsuccessfulEnd);
    result.totalRuntimeMs = elapsedMs(totalBegin, totalEnd);

    CsvWriter::writeSingleResult(config_.outputCsv, result);
}
