
#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include "tokenizer.h"

using namespace std;

const int MAX_FILENAME_LENGTH = 100;
const string test_directory = "Tests/";
const string result_directory = "Results/output";

int main() {
    char input_file_path[MAX_FILENAME_LENGTH];
    string file_name;

    ifstream input_file;
    while (!input_file.is_open()) {
        cout << "Enter a file name: ";
        cin >> file_name;
        string file_path = test_directory + file_name;
        input_file.open(file_path.c_str());

        if (!input_file.is_open()) {
            cout << "Couldn't open the input file: " << file_path << endl;
        } else {
            strcpy(input_file_path, file_path.c_str());
        }
    }

    string c_program(istreambuf_iterator<char>(input_file), {});
    string tokenized = tokenize(c_program);

    char output_file_path[MAX_FILENAME_LENGTH];
    strcpy(output_file_path, result_directory.c_str());
    strcat(output_file_path, input_file_path + strlen(test_directory.c_str()) + 5);

    ofstream output_file(output_file_path);
    output_file << tokenized;
    cout << "Tokenized C program written to the output file: " << output_file_path << endl;

    return 0;
}
