//
// Created by Fedorych Andriy
//
#include <iostream>
#include "DataBase.h"


int main() {
    printf("Database Lab1\n");
    printf("Author: Fedorych Andriy\n");
    DataBase data_base;
    DataBase::init_files();
    data_base.init_collector();


    int id[6] = {1,2,3,4,5, 6};
    char bank_name[6][20] = {"MonoBank","NBU","LHV","Swedbank", "Nordea", "Fester"};
    char country[6][20] = {"Ukraine", "Ukraine", "Estonia", "Estonia", "Finland", "France"};
    int first_filial[6] = {-1,-1,-1,-1,-1, -1};

    for(int i = 0; i < 5; i += 1){
        Bank bank = {.id = id[i], .name = "" , .country = "", .first_filial = first_filial[i]};
        strcpy(bank.name, bank_name[i]);
        strcpy(bank.country, country[i]);
        data_base.insert_m(&bank);
    }

    int filial_id[7] = {1,2,3,4,5, 6, 8};
    int bank_id[7] = {5,5,5,2,2,4, 6};
    char filial_name[7][20] = {"Nord1","Nord2","Nord3","NBU6", "NBU11", "Swed4", "NY"};
    char filial_address[7][20] = {"Helsinki 12913", "Helsinki 12142", "Espoo 64312", "Dolyna 77550", "Kyiv 45312", "Tallinn 77432", "Brooklyn 123"};

    for(int i = 0; i < 6; i += 1){
        Filial filial = {.id = filial_id[i],.bank_id = bank_id[i] ,.filial_name = "", .filial_address = "", .next_address = -1, .deleted = 0};
        strcpy(filial.filial_name, filial_name[i]);
        strcpy(filial.filial_address, filial_address[i]);
        data_base.insert_s(&filial);
    }

    data_base.ut_m();
    data_base.ut_s();

    std::cout<<"------------------------\n";
    data_base.delete_m(2);
    data_base.ut_m();
    data_base.ut_s();

    std::cout<<"------------------------\n";
    data_base.delete_s(5,2);

    data_base.ut_m();
    data_base.ut_s();

    Bank bank = {.id = id[5], .name = "" , .country = "", .first_filial = -1};
    strcpy(bank.name, bank_name[5]);
    strcpy(bank.country, country[5]);
    data_base.insert_m(&bank);

    Filial filial = {.id = 8,.bank_id = 6 ,.filial_name = "", .filial_address = "", .next_address = -1, .deleted = 0};
    strcpy(filial.filial_name, filial_name[6]);
    strcpy(filial.filial_address, filial_address[6]);
    data_base.insert_s(&filial);

    std::cout<<"------------------------\n";
    data_base.ut_m();
    data_base.ut_s();

    char new_name[20] = {"OTF"};
    char new_country[20] = {"Germany"};

    data_base.update_m(6, new_name, new_country);

    char new_filial_name[20] = "Munich2";
    char new_filial_address[20] = "Munich 12437";
    data_base.update_s(6, 8, new_filial_name, new_filial_address);

    std::cout<<"------------------------\n";
    data_base.ut_m();
    data_base.ut_s();

    data_base.get_m(4);
    data_base.get_s(5, 3);


    return 0;
}

