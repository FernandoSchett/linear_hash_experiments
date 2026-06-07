#pragma once

#include "ExperimentConfig.hpp"

class ExperimentRunner {
public:
    explicit ExperimentRunner(ExperimentConfig config);

    void run();

private:
    ExperimentConfig config_;
};
