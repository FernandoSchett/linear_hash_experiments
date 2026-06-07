#pragma once

#include "BucketPage.hpp"
#include "HashStats.hpp"

#include <cstddef>
#include <cstdint>
#include <vector>

class LinearHashing {
public:
    LinearHashing(std::size_t pageSize, double alphaMax, std::size_t initialBuckets);

    void insert(uint64_t key);
    bool contains(uint64_t key);

    HashStats getStats() const;
    void resetOperationCounters();
    uint64_t getLastOperationPageAccesses() const;
    uint64_t getTotalPageAccesses() const;

private:
    struct Bucket {
        explicit Bucket(std::size_t pageSize);

        BucketPage primary;
        std::vector<BucketPage> overflow;
    };

    std::size_t bucketIndex(uint64_t key) const;
    std::size_t hashAtLevel(uint64_t key, std::size_t level) const;
    std::size_t bucketsAtLevel(std::size_t level) const;
    double currentLoadFactor() const;
    std::size_t totalPages() const;
    std::size_t totalOverflowPages() const;

    bool insertIntoBucket(Bucket& bucket, uint64_t key, bool countReadBeforeWrite);
    bool bucketContains(const Bucket& bucket, uint64_t key);
    void splitNextBucket();
    std::vector<Record> collectRecordsAndClear(Bucket& bucket);
    void reinsertDuringSplit(std::size_t bucketIndex, uint64_t key);
    void countPageAccess();

    std::size_t pageSize_;
    double alphaMax_;
    std::size_t initialBuckets_;
    std::size_t level_;
    std::size_t splitPointer_;
    std::size_t totalRecords_;
    std::size_t numSplits_;
    uint64_t totalPageAccesses_;
    uint64_t lastOperationPageAccesses_;
    std::vector<Bucket> buckets_;
};
