#include "LinearHashing.hpp"

#include <stdexcept>

LinearHashing::Bucket::Bucket(std::size_t pageSize)
    : primary(pageSize) {}

LinearHashing::LinearHashing(std::size_t pageSize, double alphaMax, std::size_t initialBuckets)
    : pageSize_(pageSize),
      alphaMax_(alphaMax),
      initialBuckets_(initialBuckets),
      level_(0),
      splitPointer_(0),
      totalRecords_(0),
      numSplits_(0),
      totalPageAccesses_(0),
      lastOperationPageAccesses_(0) {
    if (pageSize_ == 0) {
        throw std::invalid_argument("page_size deve ser maior que zero");
    }
    if (alphaMax_ <= 0.0 || alphaMax_ >= 1.0) {
        throw std::invalid_argument("alpha_max deve estar entre 0 e 1");
    }
    if (initialBuckets_ == 0) {
        throw std::invalid_argument("initial_buckets deve ser maior que zero");
    }

    buckets_.reserve(initialBuckets_);
    for (std::size_t i = 0; i < initialBuckets_; ++i) {
        buckets_.emplace_back(pageSize_);
    }
}

void LinearHashing::insert(uint64_t key) {
    resetOperationCounters();
    const std::size_t index = bucketIndex(key);

    if (bucketContains(buckets_.at(index), key)) {
        throw std::runtime_error("chave duplicada inserida no hash linear");
    }

    insertIntoBucket(buckets_.at(index), key, true);
    ++totalRecords_;

    if (currentLoadFactor() > alphaMax_) {
        splitNextBucket();
    }
}

bool LinearHashing::contains(uint64_t key) {
    resetOperationCounters();
    const std::size_t index = bucketIndex(key);
    return bucketContains(buckets_.at(index), key);
}

HashStats LinearHashing::getStats() const {
    HashStats stats;
    stats.pageSize = pageSize_;
    stats.alphaMax = alphaMax_;
    stats.initialBuckets = initialBuckets_;
    stats.primaryBuckets = buckets_.size();
    stats.overflowPages = totalOverflowPages();
    stats.totalPages = totalPages();
    stats.totalRecords = totalRecords_;
    stats.loadFactorGlobal = currentLoadFactor();
    stats.realSpaceUtilization = stats.loadFactorGlobal;
    stats.overflowPagePercentage =
        stats.totalPages == 0 ? 0.0 : 100.0 * static_cast<double>(stats.overflowPages) /
                                      static_cast<double>(stats.totalPages);
    stats.numSplits = numSplits_;
    stats.level = level_;
    stats.splitPointer = splitPointer_;
    stats.totalPageAccesses = totalPageAccesses_;
    return stats;
}

void LinearHashing::resetOperationCounters() {
    lastOperationPageAccesses_ = 0;
}

uint64_t LinearHashing::getLastOperationPageAccesses() const {
    return lastOperationPageAccesses_;
}

uint64_t LinearHashing::getTotalPageAccesses() const {
    return totalPageAccesses_;
}

std::size_t LinearHashing::bucketIndex(uint64_t key) const {
    std::size_t index = hashAtLevel(key, level_);
    if (index < splitPointer_) {
        index = hashAtLevel(key, level_ + 1);
    }
    return index;
}

std::size_t LinearHashing::hashAtLevel(uint64_t key, std::size_t level) const {
    return static_cast<std::size_t>(key % bucketsAtLevel(level));
}

std::size_t LinearHashing::bucketsAtLevel(std::size_t level) const {
    return initialBuckets_ << level;
}

double LinearHashing::currentLoadFactor() const {
    return static_cast<double>(totalRecords_) /
           static_cast<double>(totalPages() * pageSize_);
}

std::size_t LinearHashing::totalPages() const {
    return buckets_.size() + totalOverflowPages();
}

std::size_t LinearHashing::totalOverflowPages() const {
    std::size_t total = 0;
    for (const Bucket& bucket : buckets_) {
        total += bucket.overflow.size();
    }
    return total;
}

bool LinearHashing::insertIntoBucket(Bucket& bucket, uint64_t key, bool countReadBeforeWrite) {
    if (countReadBeforeWrite) {
        countPageAccess();
    }
    if (!bucket.primary.isFull()) {
        countPageAccess();
        bucket.primary.insert(key);
        return true;
    }

    for (BucketPage& page : bucket.overflow) {
        if (countReadBeforeWrite) {
            countPageAccess();
        }
        if (!page.isFull()) {
            countPageAccess();
            page.insert(key);
            return true;
        }
    }

    bucket.overflow.emplace_back(pageSize_);
    countPageAccess();
    bucket.overflow.back().insert(key);
    return true;
}

bool LinearHashing::bucketContains(const Bucket& bucket, uint64_t key) {
    countPageAccess();
    if (bucket.primary.contains(key)) {
        return true;
    }

    for (const BucketPage& page : bucket.overflow) {
        countPageAccess();
        if (page.contains(key)) {
            return true;
        }
    }
    return false;
}

void LinearHashing::splitNextBucket() {
    const std::size_t oldIndex = splitPointer_;
    const std::size_t newIndex = splitPointer_ + bucketsAtLevel(level_);
    buckets_.emplace_back(pageSize_);

    std::vector<Record> records = collectRecordsAndClear(buckets_.at(oldIndex));
    for (const Record& record : records) {
        const std::size_t target = hashAtLevel(record.key, level_ + 1);
        reinsertDuringSplit(target == newIndex ? newIndex : oldIndex, record.key);
    }

    ++numSplits_;
    ++splitPointer_;
    if (splitPointer_ == bucketsAtLevel(level_)) {
        splitPointer_ = 0;
        ++level_;
    }
}

std::vector<Record> LinearHashing::collectRecordsAndClear(Bucket& bucket) {
    std::vector<Record> records;
    records.reserve(bucket.primary.size() + bucket.overflow.size() * pageSize_);

    countPageAccess();
    for (const Record& record : bucket.primary.records()) {
        records.push_back(record);
    }

    for (const BucketPage& page : bucket.overflow) {
        countPageAccess();
        for (const Record& record : page.records()) {
            records.push_back(record);
        }
    }

    countPageAccess();
    bucket.primary.clear();
    bucket.overflow.clear();
    return records;
}

void LinearHashing::reinsertDuringSplit(std::size_t bucketIndex, uint64_t key) {
    insertIntoBucket(buckets_.at(bucketIndex), key, false);
}

void LinearHashing::countPageAccess() {
    ++lastOperationPageAccesses_;
    ++totalPageAccesses_;
}
