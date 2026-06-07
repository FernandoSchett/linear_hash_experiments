#pragma once

#include "Record.hpp"

#include <cstddef>
#include <vector>

class BucketPage {
public:
    explicit BucketPage(std::size_t capacity);

    bool isFull() const;
    bool empty() const;
    bool contains(uint64_t key) const;
    void insert(uint64_t key);
    void clear();

    const std::vector<Record>& records() const;
    std::size_t size() const;
    std::size_t capacity() const;

private:
    std::size_t capacity_;
    std::vector<Record> records_;
};
