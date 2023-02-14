// DB LAB 1
// Created by Fedorych Andriy
//

#ifndef BMS_DATABASE_DATABASE_H
#define BMS_DATABASE_DATABASE_H
#include "GarbageCollector.h"
#include "Banks.h"
#include "Filials.h"
class DataBase {
public:
    // as a result, the file is always empty
    static void init_files();
    void init_collector();
    void load_collector(bool mode);
    void sort_collector();
    int get_collector_address(int key);
    int get_collector_index(int key);

    void insert_m(Bank* bank);
    void insert_s(Filial* filial);

    void delete_m(int id);
    void delete_s(int key_id_m, int key_id_s);

    void get_m(int key_id);
    void get_s(int key_id_m, int key_id_s);

    void update_m(int id, char name[20], char country[20]);
    void update_s(int key_id_m, int key_id_s, char filial_name[20], char filial_address[20]);

    void ut_m();
    void ut_s() const;

private:
    collectorElement collector[MAX_SIZE]{};

    int cnt_banks = 0;
    int del_banks = 0;

    int cnt_filial = 0;
    int del_filial = 0;

};
#endif //BMS_DATABASE_DATABASE_H
