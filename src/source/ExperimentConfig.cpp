#include "ExperimentConfig.hpp"

#include <cctype>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>

namespace {

class SimpleJsonObject {
public:
    explicit SimpleJsonObject(const std::string& text)
        : text_(text), pos_(0) {
        parse();
    }

    std::string getString(const std::string& key) const {
        const auto it = values_.find(key);
        if (it == values_.end() || it->second.isString == false) {
            throw std::runtime_error("campo string ausente ou invalido: " + key);
        }
        return it->second.value;
    }

    std::size_t getSize(const std::string& key) const {
        return static_cast<std::size_t>(std::stoull(getNumberToken(key)));
    }

    uint64_t getUint64(const std::string& key) const {
        return static_cast<uint64_t>(std::stoull(getNumberToken(key)));
    }

    double getDouble(const std::string& key) const {
        return std::stod(getNumberToken(key));
    }

private:
    struct Value {
        std::string value;
        bool isString = false;
    };

    void parse() {
        skipSpaces();
        expect('{');
        skipSpaces();
        while (!peek('}')) {
            const std::string key = parseString();
            skipSpaces();
            expect(':');
            skipSpaces();
            Value value;
            if (peek('"')) {
                value.value = parseString();
                value.isString = true;
            } else {
                value.value = parseNumber();
                value.isString = false;
            }
            values_[key] = value;
            skipSpaces();
            if (peek(',')) {
                ++pos_;
                skipSpaces();
            } else {
                break;
            }
        }
        expect('}');
        skipSpaces();
        if (pos_ != text_.size()) {
            throw std::runtime_error("conteudo inesperado apos fim do JSON");
        }
    }

    std::string parseString() {
        expect('"');
        std::string result;
        while (pos_ < text_.size() && text_[pos_] != '"') {
            if (text_[pos_] == '\\') {
                throw std::runtime_error("escapes em strings JSON nao sao suportados");
            }
            result.push_back(text_[pos_++]);
        }
        expect('"');
        return result;
    }

    std::string parseNumber() {
        const std::size_t start = pos_;
        while (pos_ < text_.size() &&
               (std::isdigit(static_cast<unsigned char>(text_[pos_])) ||
                text_[pos_] == '.' || text_[pos_] == '-')) {
            ++pos_;
        }
        if (start == pos_) {
            throw std::runtime_error("numero JSON esperado");
        }
        return text_.substr(start, pos_ - start);
    }

    std::string getNumberToken(const std::string& key) const {
        const auto it = values_.find(key);
        if (it == values_.end() || it->second.isString) {
            throw std::runtime_error("campo numerico ausente ou invalido: " + key);
        }
        return it->second.value;
    }

    void skipSpaces() {
        while (pos_ < text_.size() &&
               std::isspace(static_cast<unsigned char>(text_[pos_]))) {
            ++pos_;
        }
    }

    bool peek(char expected) const {
        return pos_ < text_.size() && text_[pos_] == expected;
    }

    void expect(char expected) {
        if (!peek(expected)) {
            throw std::runtime_error(std::string("caractere JSON esperado: ") + expected);
        }
        ++pos_;
    }

    std::string text_;
    std::size_t pos_;
    std::unordered_map<std::string, Value> values_;
};

std::string readWholeFile(const std::string& path) {
    std::ifstream input(path);
    if (!input) {
        throw std::runtime_error("nao foi possivel abrir o JSON: " + path);
    }
    std::ostringstream buffer;
    buffer << input.rdbuf();
    return buffer.str();
}

} // namespace

ExperimentConfig ExperimentConfig::loadFromFile(const std::string& path) {
    const SimpleJsonObject json(readWholeFile(path));

    ExperimentConfig config;
    config.experimentId = json.getString("experiment_id");
    config.pageSize = json.getSize("page_size");
    config.alphaMax = json.getDouble("alpha_max");
    config.initialBuckets = json.getSize("initial_buckets");
    config.numRecords = json.getSize("num_records");
    config.numSuccessfulSearches = json.getSize("num_successful_searches");
    config.numUnsuccessfulSearches = json.getSize("num_unsuccessful_searches");
    config.seed = json.getUint64("seed");
    config.outputCsv = json.getString("output_csv");

    if (config.numSuccessfulSearches > config.numRecords) {
        throw std::runtime_error("buscas com sucesso nao podem exceder num_records");
    }

    return config;
}
