#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include "dictionary.h"

#define MAX_WORD_LENGTH 30
#define MAX_FILENAME_LENGTH 100
const char* test_directory = "Tests/";
const char* result_directory = "Results/output";


char *read_one_word(FILE *file) {
    char *word = (char *)malloc((MAX_WORD_LENGTH + 1) * sizeof(char));  // + 1 for null terminal
    int pointer = 0;
    char c;

    while ((c = fgetc(file)) != EOF && pointer < MAX_WORD_LENGTH) {
        if (isalpha(c)) {
            word[pointer++] = c;
        }
        else if (pointer > 0) break;
        if (pointer == 30) break;
    }

    word[pointer] = '\0';
    return word;
}


int main() {
    char input_file_path[MAX_FILENAME_LENGTH];
    strcpy(input_file_path, test_directory);
    strcat(input_file_path, "input_3.txt");

    FILE* input_file = fopen(input_file_path, "r");
    if (input_file == NULL) {
        printf("Couldn't open the input_file: %s\n", input_file_path);
        return 1;
    }


    Dictionary* dict = init(1);
    int word_count = 0;

    while (!feof(input_file)) {
        char *word = read_one_word(input_file);
        if (word[0] == '\0') {
            free(word);
            break;
        }
        if (get_value(dict, word) == -1) {
            add_pair(dict, word, 1);
        }
        else{
            add_pair(dict, word, get_value(dict, word) + 1);
        }

        // printf("Word %d: %s\n", word_count + 1, word);
        word_count++;
        free(word);
    }

    printf("Total words: %d\n", word_count);
    printf("Unique words: %d\n", dict->count);

    char output_file_path[MAX_FILENAME_LENGTH];
    strcpy(output_file_path, result_directory);
    strcat(output_file_path, input_file_path + strlen(test_directory) + 5);

    FILE *output_file;
    output_file = fopen(output_file_path, "w");
    if (output_file == NULL) {
        printf("Couldn't open the output_file: %s\n", output_file_path);
        return 1;
    }

    for (int i = 0; i < dict->count; i++) {
        printf("%s  %d\n", dict->pairs[i].key, dict->pairs[i].value);
        fprintf(output_file, "%s  %d\n", dict->pairs[i].key, dict->pairs[i].value);
    }


    fclose(input_file);
    fclose(output_file);
    clear_dictionary(dict);

    return 0;
}
