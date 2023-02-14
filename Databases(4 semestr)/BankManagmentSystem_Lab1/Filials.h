//
// Created by Fedorych Andriy
//

#ifndef BMS_DATABASE_FILIALS_H
#define BMS_DATABASE_FILIALS_H

# define file_s "filials_file_s.bin"

struct Filial{
    int id;
    int bank_id;
    char filial_name[20];
    char filial_address[20];
    int next_address;
    int deleted;
};
#endif //BMS_DATABASE_FILIALS_H
