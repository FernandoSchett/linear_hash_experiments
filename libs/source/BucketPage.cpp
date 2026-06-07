#include "BucketPage.hpp"

#include <algorithm>
#include <stdexcept>

BucketPage::BucketPage(std::size_t capacity)
    : capacity_(capacity) {
    records_.reserve(capacity);
}

bool BucketPage::isFull() const {
    return records_.size() >= capacity_;
}

bool BucketPage::empty() const {
    return records_.empty();
}

bool BucketPage::contains(uint64_t key) const {
    return std::any_of(records_.begin(), records_.end(),
                       [key](const Record& record) { return record.key == key; });
}

void BucketPage::insert(uint64_t key) {
    if (isFull()) {
        throw std::runtime_error("tentativa de inserir em pagina cheia");
    }
    records_.push_back(Record{key});
}

void BucketPage::clear() {
    records_.clear();
}

const std::vector<Record>& BucketPage::records() const {
    return records_;
}

std::size_t BucketPage::size() const {
    return records_.size();
}

std::size_t BucketPage::capacity() const {
    return capacity_;
}
