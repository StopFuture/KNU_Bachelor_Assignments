//
// Created by Fedorych Andriy
//

#ifndef BMS_DATABASE_BANKS_H
#define BMS_DATABASE_BANKS_H
# define file_m "banks_file_m.bin"

struct Bank {
    int id;
    char name[20];
    char country[20];
    int first_filial;
};

#endif //BMS_DATABASE_BANKS_H
