//
// Created by Fedorych Andriy on 22/10/23.
//

#include "tokenizer.h"
#include <regex>
#include <iostream>
#include <vector>

using namespace std;

string tokenize(string program) {
        vector<Token> tokens = {
            {regex("/\\*[^*]*\\*+(?:[^/*][^*]*\\*+)*/"), "Comment"},  // Multiline
            {regex("//.*"), "Comment"},  // Inline
            {regex("\"(?:\\\\\"|[^\"])*?\""), "String"},
            {regex("(\"([^\"\\\\]|\\\\.)*\"|'(\\\\['\"tvrnafb\\\\]|[^'\\\\])')"), "Char"},
            {regex("#[ ]*(define|import|include|elif|else|ifndef|error|if|ifdef|pragma|line|undef|using|endif)"), "Directive"},
            {regex("[ ]+<(assert|complex|ctype|errno|fenv|float|inttypes|iso646|limits|locale|math|setjmp|signal|stdalign|stdarg|stdatomic|stdbool|stddef|stdint|stdio|stdlib|stdnoreturn|string|tgmath|threads|time|uchar|wchar|wctype)\\.h>"), "Library"},
            {regex("\\b(break|case|catch|const_cast|continue|delete|do|dynamic_cast|new|sizeof|volatile|goto|static|explicit|export|else|try|this|throw|typeid|switch|if|operator|mutable|namespace|extern|inline|return|using|virtual|while|for)\\b"), "Reserved"},
            {regex("\\b(bool|auto|char|class|double|struct|enum|typedef|template|int|union|long|float|unsigned|void)\\b"), "DataType"},
            {regex("\\b(false|true)\\b"), "Bool"},
            {regex("0x[0-9A-Fa-f]+"), "HexNumber"},
            {regex("0b[01]+"), "BinNumber"},
            {regex("[+-]?([0-9]*[.])?[0-9]+([eE][+-]?[0-9]+)?"), "Number"},
            {regex("\\bmain\\s*"), "Function"},
            {regex("[_A-Za-z][0-9A-Za-z_]*(?=\\([A-Za-z_][A-Za-z_0-9]*[*]*[\\s]+[A-Za-z_][A-Za-z_0-9]*)"), "Function"},
            {regex("[_A-Za-z][0-9A-Za-z_]*(?=\\()"), "FunctionCall"},
            {regex("[_A-Za-z][0-9A-Za-z_]*(?!\\()"), "Variable"},
            {regex("([\\(\\)\\{\\}\\[\\]\"'\\;\\,\\<\\>\\.\\/]|->)"), "Delimiter"},
            {regex("([==|!=|<=|>=|&&|\\+\\+|--|\\+|-|\\*|/|%|&|\\|\\^|~|<<|>>|<|>|!|=])"), "Operator"},
            {regex("([\\s]+)"), " "},

    };
//    for (const auto& token : tokens) {
//        cout<<token.name<<endl;
//    }
    string result = "";
    while (!program.empty()) {
        smatch match;
        bool flag = true;
        for (const auto& token : tokens) {
            if (regex_search(program, match, token.pattern)) {
                if (match.position() == 0) {
                    if (token.name != " ") {
                        string new_token =  token.name + ":   " + match.str() + "\n" ;
                        cout << new_token;
                        result += new_token;
                    }
                    program = match.suffix();
                    flag = false;
                    break;
                }
            }
        }


        if (flag) {
            size_t newline_pos = program.find('\n');
            if (newline_pos == string::npos) {
                result += "Uncategorized: " + program + "\n";
                cout <<"Uncategorized: " + program + "\n";
                break;
            } else {
                string uncategorized_text = program.substr(0, newline_pos);
                result += "Uncategorized: " + uncategorized_text + "\n";
                cout << "Uncategorized: " + uncategorized_text + "\n";
                program = program.substr(newline_pos + 1);
            }
        }
    }
    return result;
}

