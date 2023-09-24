//
// Created by Fedorych Andriy on 24/9/23.
//

#ifndef LAB1_DICTIONARY_H
#define LAB1_DICTIONARY_H

typedef struct {
    char* key;
    int value;
} Pair;

typedef struct {
    Pair* pairs;
    int size;
    int count;  // Track the current count of elements
} Dictionary;

Dictionary* init(int initial_size);
void add_pair(Dictionary* dict, const char* key, int value);
int get_value(Dictionary* dict, const char* key);
void clear_dictionary(Dictionary* dict);

#endif //LAB1_DICTIONARY_H
