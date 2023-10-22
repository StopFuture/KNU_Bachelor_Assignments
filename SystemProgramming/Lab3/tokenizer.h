//
// Created by Fedorych Andriy on 22/10/23.
//

#ifndef LAB3_TOKENIZER_H
#define LAB3_TOKENIZER_H

#include <string>
#include <vector>
#include <regex>

struct Token {
    std::regex pattern;
    std::string name;
};

std::string tokenize(std::string program);

#endif //LAB3_TOKENIZER_H
