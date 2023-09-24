//
// Created by Fedorych Andriy on 24/9/23.
//

#include <stdlib.h>
#include <string.h>
#include "dictionary.h"

Dictionary* init(int initial_size) {
    Dictionary* dict = malloc(sizeof(Dictionary));
    dict->pairs = malloc(initial_size * sizeof(Pair));
    dict->size = initial_size;
    dict->count = 0;
    return dict;
}

void add_pair(Dictionary* dict, const char* key, int value) {
    for (int i = 0; i < dict->count; i++) {
        if (strcmp(dict->pairs[i].key, key) == 0) {
            dict->pairs[i].value = value;  // Updating if key exists
            return;
        }
    }

    if (dict->count == dict->size) {
        dict->size *= 2;
        dict->pairs = realloc(dict->pairs, dict->size * sizeof(Pair));
    }

    dict->pairs[dict->count].key = malloc(strlen(key) + 1);
    strcpy(dict->pairs[dict->count].key, key);

    dict->pairs[dict->count].value = value;
    dict->count++;
}

int get_value(Dictionary* dict, const char* key) {
    for (int i = 0; i < dict->count; i++) {
        if (strcmp(dict->pairs[i].key, key) == 0) {
            return dict->pairs[i].value;
        }
    }
    return -1;  // if key not found
}

void clear_dictionary(Dictionary* dict) {
    for (int i = 0; i < dict->count; i++) {
        free(dict->pairs[i].key);
    }
    free(dict->pairs);
    free(dict);
}
