#include "ExperimentConfig.hpp"
#include "ExperimentRunner.hpp"

#include <exception>
#include <iostream>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Uso: " << argv[0] << " experiments/p10_a060.json\n";
        return 1;
    }

    try {
        const ExperimentConfig config = ExperimentConfig::loadFromFile(argv[1]);
        ExperimentRunner runner(config);
        runner.run();
        std::cout << "Experimento concluido: " << config.experimentId << "\n";
        std::cout << "CSV gerado em: " << config.outputCsv << "\n";
    } catch (const std::exception& ex) {
        std::cerr << "Erro: " << ex.what() << "\n";
        return 1;
    }

    return 0;
}
