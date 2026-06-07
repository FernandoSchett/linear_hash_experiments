#include "CsvWriter.hpp"

#include <filesystem>
#include <fstream>
#include <iomanip>
#include <stdexcept>

void CsvWriter::writeSingleResult(const std::string& path, const ExperimentResult& result) {
    const std::filesystem::path csvPath(path);
    if (csvPath.has_parent_path()) {
        std::filesystem::create_directories(csvPath.parent_path());
    }

    std::ofstream output(path);
    if (!output) {
        throw std::runtime_error("nao foi possivel criar CSV: " + path);
    }

    output << "experiment_id,page_size_P,alpha_max,seed,num_inserted_records,"
           << "num_successful_searches,num_unsuccessful_searches,initial_buckets,"
           << "final_primary_buckets,final_overflow_pages,final_total_pages,"
           << "final_total_records,final_load_factor_global,real_space_utilization,"
           << "overflow_page_percentage,num_splits,final_level,final_split_pointer,"
           << "insert_total_page_accesses,insert_avg_page_accesses,"
           << "successful_search_total_page_accesses,successful_search_avg_page_accesses,"
           << "unsuccessful_search_total_page_accesses,unsuccessful_search_avg_page_accesses,"
           << "insert_runtime_ms,successful_search_runtime_ms,unsuccessful_search_runtime_ms,"
           << "total_runtime_ms\n";

    output << std::fixed << std::setprecision(6)
           << result.experimentId << ','
           << result.pageSizeP << ','
           << result.alphaMax << ','
           << result.seed << ','
           << result.numInsertedRecords << ','
           << result.numSuccessfulSearches << ','
           << result.numUnsuccessfulSearches << ','
           << result.initialBuckets << ','
           << result.finalPrimaryBuckets << ','
           << result.finalOverflowPages << ','
           << result.finalTotalPages << ','
           << result.finalTotalRecords << ','
           << result.finalLoadFactorGlobal << ','
           << result.realSpaceUtilization << ','
           << result.overflowPagePercentage << ','
           << result.numSplits << ','
           << result.finalLevel << ','
           << result.finalSplitPointer << ','
           << result.insertTotalPageAccesses << ','
           << result.insertAvgPageAccesses << ','
           << result.successfulSearchTotalPageAccesses << ','
           << result.successfulSearchAvgPageAccesses << ','
           << result.unsuccessfulSearchTotalPageAccesses << ','
           << result.unsuccessfulSearchAvgPageAccesses << ','
           << result.insertRuntimeMs << ','
           << result.successfulSearchRuntimeMs << ','
           << result.unsuccessfulSearchRuntimeMs << ','
           << result.totalRuntimeMs << '\n';
}
