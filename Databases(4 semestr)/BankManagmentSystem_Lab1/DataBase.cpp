//
// Created by Fedorych Andriy
//
#include <cstdio>
#include <algorithm>


#include "DataBase.h"
#include "Banks.h"
#include "Filials.h"
#include "GarbageCollector.h"

void DataBase::init_files(){
    FILE* banks_file_m = fopen(file_m, "wb+");
    fclose(banks_file_m);
    FILE* filials_file_s = fopen(file_s, "wb+");
    fclose(filials_file_s);
    FILE* indexes_file_i = fopen(file_i, "wb+");
    fclose(indexes_file_i);

}

void DataBase::init_collector(){
    for(int i = 0; i < MAX_SIZE; i += 1)
    {
        collector[i].key = -1;
        collector[i].address = -1;
        collector[i].deleted = 0;
    }
}

void  DataBase::load_collector(bool mode){ // load if mode == True else rewrite collector
    FILE * collector_file = fopen(file_i,mode ? "rb+" : "wb+");

    for (int i = 0; i < cnt_banks; i += 1) {
        mode ? fread(&collector[i].key, sizeof(int), 1, collector_file):fwrite(&collector[i].key, sizeof(int), 1, collector_file);
        mode ? fread(&collector[i].address, sizeof(int), 1, collector_file):fwrite(&collector[i].address, sizeof(int), 1, collector_file);
        mode ? fread(&collector[i].deleted, sizeof(int), 1, collector_file):fwrite(&collector[i].deleted, sizeof(int), 1, collector_file);
    }
    fclose(collector_file);
}

void DataBase::sort_collector(){
   std::qsort(collector,
              cnt_banks, sizeof(collectorElement),
              [](const void * a, const void * b)
              { return (((collectorElement *)a)->key  - ((collectorElement *)b)->key);}
    );
}

int DataBase::get_collector_address(int key) {

        for(int i = 0; i < cnt_banks + del_banks; i += 1){ // can be faster --> log(cnt_banks)
            if (collector[i].key == key && collector[i].deleted == 0) {
                    return collector[i].address;
            }
        }

        return -1;

}

int DataBase::get_collector_index(int key) {
    for(int i = 0; i < cnt_banks + del_banks; i += 1){ // can be faster --> log(cnt_banks)
        if (collector[i].key == key && collector[i].deleted == 0) {
            return i;
        }
    }
    return -1;
}

void DataBase::insert_m(Bank* bank)
{
    for (int i = 0; i < cnt_banks; i+=1) {
        if (collector[i].key == bank->id) {
            printf("Reserved\n");
            return;
        }
    }

    FILE* banks_file_m = fopen(file_m, "rb+");

    load_collector(true);
    collector[cnt_banks + del_banks].key= bank -> id;
    collector[cnt_banks + del_banks].address = (cnt_banks + del_banks) * (int) sizeof(Bank);
    cnt_banks++;

    fseek(banks_file_m, 0, SEEK_END);

    fwrite(&bank->id, sizeof(int), 1, banks_file_m);
    fwrite(&bank->name, sizeof(bank->name), 1, banks_file_m);
    fwrite(&bank->country, sizeof(bank->country), 1, banks_file_m);
    fwrite(&bank->first_filial, sizeof(int), 1, banks_file_m);
    sort_collector();
    load_collector(false);
    fclose(banks_file_m);

}

void DataBase::insert_s(Filial* filial)
{
    int flag = 0;
    for (int i = 0; i < cnt_banks + del_banks; i++) {
        if (collector[i].deleted != 1 && collector[i].key == filial->bank_id ) {
            flag = 1;
        }
    }
    if(flag == 0){
        printf("ERROR\n");
        return;
    }

    FILE* filials_file_s = fopen(file_s, "rb+");
    fseek(filials_file_s, 0, SEEK_END);
    fwrite(&filial->id, sizeof(int), 1, filials_file_s);
    fwrite(&filial->bank_id, sizeof (int), 1, filials_file_s);
    fwrite(&filial->filial_name, sizeof(filial->filial_name), 1, filials_file_s);
    fwrite(&filial->filial_address, sizeof(filial->filial_address), 1, filials_file_s);
    fwrite(&filial->next_address, sizeof(int), 1, filials_file_s);
    fwrite(&filial->deleted, sizeof(int), 1, filials_file_s);

    FILE* banks_file_m = fopen(file_m, "rb+");
    int to_first_filial_address = get_collector_address(filial->bank_id) + 44;
    fseek(banks_file_m, to_first_filial_address, SEEK_SET);

    int first_filial_address;
    fread(&first_filial_address, sizeof(int), 1, banks_file_m);

    int address = (cnt_filial + del_filial) * (int) sizeof(Filial);
    if (first_filial_address == -1) {
        fseek(banks_file_m, -4, SEEK_CUR);
        fwrite(&address, sizeof(int), 1, banks_file_m);
    } else {
        int next_filial = first_filial_address;
        while (next_filial != -1) {
            fseek(filials_file_s, next_filial + 48, SEEK_SET);
            fread(&next_filial, sizeof(int), 1, filials_file_s);
        }
        fseek(filials_file_s, -4, SEEK_CUR);
        fwrite(&address, sizeof(int), 1, filials_file_s);
    }
    cnt_filial += 1;
    fclose(filials_file_s);
    fclose(banks_file_m);
}


void DataBase::ut_m()
{
    FILE* banks_file_m = fopen(file_m, "rb+");
    printf("ut_m:\n");

    int id;
    char name[20];
    char country[20];
    int first_filial;



    for(int i = 0; i < cnt_banks + del_banks; i+=1)
    {
        if(collector[i].deleted == 0)
        {

            fseek(banks_file_m, get_collector_address(collector[i].key), SEEK_SET);
            fread(&id, sizeof(int), 1, banks_file_m);
            fread(&name, sizeof(name), 1, banks_file_m);
            fread(&country, sizeof(country), 1, banks_file_m);
            fread(&first_filial, sizeof(int), 1, banks_file_m);
            printf("Id: %d, Name: %s, Country: %s, Filial1 address: %d\n",id, name, country, first_filial);
        }

    }

    fclose(banks_file_m);


}

void DataBase::ut_s() const{
    FILE* filials_file_s = fopen(file_s, "rb+");

    printf("ut_s:\n");

    int id;
    int bank_id;
    char filial_name[20];
    char filial_address[20];
    int next_address;
    int deleted;
    // printf("cnt filial: %d \n", cnt_filial);
    for (int i = 0; i < cnt_filial + del_filial; i += 1) {
        fseek(filials_file_s, 52, SEEK_CUR);
        fread(&deleted, sizeof(int), 1, filials_file_s);

        if(deleted == 0) {
            fseek(filials_file_s, -56, SEEK_CUR);
            fread(&id, sizeof(int), 1, filials_file_s);
            fread(&bank_id, sizeof(int), 1, filials_file_s);
            fread(&filial_name, sizeof(filial_name), 1, filials_file_s);
            fread(&filial_address, sizeof(filial_address), 1, filials_file_s);
            fread(&next_address, sizeof(int), 1, filials_file_s);
            fread(&deleted, sizeof (int), 1, filials_file_s);
            printf("Id: %d, Bank id %d: Filial name: %s,  Filial address(location) : %s, Next  address: %d, deleted:%d \n",
                   id, bank_id, filial_name, filial_address, next_address, deleted);
        }
    }

    fclose(filials_file_s);
}

void DataBase::delete_m(int id)
{
    int tmp = get_collector_index(id);
    if (tmp == -1) {
        printf("Error, not presented id %d\n", id);
        return;
    }
    collector[tmp].deleted = 1;

    int offset = collector[tmp].address;
    FILE* banks_file_m = fopen(file_m, "rb+");
    int first_filial;
    fseek(banks_file_m, offset + 44 ,SEEK_SET);
    fread(&first_filial, sizeof(int), 1, banks_file_m);
    fclose(banks_file_m);
    if(first_filial != -1)
    {
        FILE* filials_file_s = fopen(file_s, "rb+");
        int new_del = 1;
        fseek(filials_file_s, first_filial, SEEK_SET);
        int next_filial = first_filial; 
        int current_address;
        while(next_filial != -1)
        {
            current_address = next_filial;
            fseek(filials_file_s, current_address + 52, SEEK_SET);
            fwrite(&new_del, sizeof(int), 1, filials_file_s);
            del_filial += 1;
            cnt_filial -= 1;
            fseek(filials_file_s, next_filial + 48, SEEK_SET);
            fread(&next_filial, sizeof(int), 1, filials_file_s);
        }

        fclose(filials_file_s);

    }
    cnt_banks -= 1;
    del_banks += 1;
    sort_collector();
    load_collector(false);
    fclose(banks_file_m);
}

void DataBase :: delete_s(int key_id_m, int key_id_s) {
    int skip_m = get_collector_address(key_id_m);
    if (skip_m == -1) {
        printf("Error, key id %d\n", key_id_m);
        return;
    }

    FILE *banks_file_m = fopen(file_m, "rb+");
    fseek(banks_file_m, skip_m, SEEK_SET);
    int first_filial;
    fseek(banks_file_m, skip_m + 44, SEEK_SET);
    fread(&first_filial, sizeof(int), 1, banks_file_m);


    if (first_filial == -1) {
        printf("Bank without filials\n");
        return;
    } else {
        FILE *filials_file_s = fopen(file_s, "rb+");


        int new_key_id_s;
        int next_filial_new = -1;

        int new_del = 1;

        int new_next_filial_address = -1;
        int next_filial_address = first_filial;
        int current_address = first_filial;


        fseek(filials_file_s, first_filial, SEEK_SET);
        fread(&new_key_id_s, sizeof(int), 1, filials_file_s);

        fseek(filials_file_s, first_filial + 48, SEEK_SET);
        fread(&next_filial_address, sizeof(int), 1, filials_file_s);

        if (new_key_id_s == key_id_s) {

            fseek(banks_file_m, skip_m + 44, SEEK_SET);
            fwrite(&next_filial_address, sizeof(int), 1, banks_file_m);

            fseek(filials_file_s, first_filial + 48, SEEK_SET);
            fwrite(&next_filial_new, sizeof(int), 1, filials_file_s);
            fwrite(&new_del, sizeof(int), 1, filials_file_s);

            cnt_filial -= 1;
            del_filial += 1;

            return;
        }else{
            while(next_filial_address != -1){
                fseek(filials_file_s, next_filial_address, SEEK_SET);
                fread(&new_key_id_s, sizeof (int), 1, filials_file_s);
                if (new_key_id_s == key_id_s)
                {
                    fseek(filials_file_s, next_filial_address + 48, SEEK_SET);      //finding new nextAddress
                    fread(&new_next_filial_address, sizeof(int), 1, filials_file_s);

                    fseek(filials_file_s, current_address + 48, SEEK_SET);         // writing new nextAddress
                    fwrite(&new_next_filial_address, sizeof(int), 1, filials_file_s);

                    fseek(filials_file_s, next_filial_address + 48, SEEK_SET);
                    fwrite(&next_filial_new, 4,1, filials_file_s);
                    fwrite(&new_del, 4,1,filials_file_s);

                    fflush(filials_file_s);

                    cnt_filial -= 1;
                    del_filial += 1;
                    return;
                }

                current_address = next_filial_address;
                fseek(filials_file_s, next_filial_address+48, SEEK_SET);
                fread(&next_filial_address, sizeof (int), 1, filials_file_s);

            }
        }
        fclose(filials_file_s);
    }
    fclose(banks_file_m);
}

void DataBase::update_m(int id, char name[20], char country[20]){
    int skip = get_collector_address(id);
    if (skip == -1){
        printf("Error update_m, key id %d\n", id);
        return;
    }

    FILE* banks_file_m = fopen(file_m, "rb+");
    fseek(banks_file_m, skip + 4, SEEK_SET);
    fwrite(name, 20, 1, banks_file_m);
    fwrite(country, 20, 1, banks_file_m);
    fclose(banks_file_m);
}

void DataBase::update_s(int key_id_m, int key_id_s, char filial_name[20], char filial_address[20]) {
    int skip_m = get_collector_address(key_id_m);
    if (skip_m == -1) {
        printf("ERROR update_s, key id %d\n", key_id_m);
        return;
    }

    FILE *banks_file_m = fopen(file_m, "rb+");
    fseek(banks_file_m, skip_m, SEEK_SET);

    int first_filial;
    fseek(banks_file_m, skip_m + 44, SEEK_SET);
    fread(&first_filial, sizeof(int), 1, banks_file_m);

    fclose(banks_file_m);

    if (first_filial == -1) {
        printf("ERROR, bank without filials\n");
        return;
    } else {
        FILE *filials_file_s = fopen(file_s, "rb+");
        fseek(filials_file_s, first_filial, SEEK_SET);
        int new_key_id_s;
        int next_filial = first_filial;
        int current_address = first_filial;
        fread(&new_key_id_s, sizeof(int), 1, filials_file_s);
        while (new_key_id_s != key_id_s) {
            if (next_filial == -1) {
                printf("ERROR, update_s");
                return;
            }
            fseek(filials_file_s, next_filial, SEEK_SET);
            fread(&new_key_id_s, sizeof(int), 1, filials_file_s);
            current_address = next_filial;
            fseek(filials_file_s, next_filial + 48, SEEK_SET);
            fread(&next_filial, sizeof(int), 1, filials_file_s);
        }


        fseek(filials_file_s, current_address + 8, SEEK_SET);
        fwrite(filial_name, 20, 1, filials_file_s);
        fwrite(filial_address, 20, 1, filials_file_s);
        fclose(filials_file_s);
    }
}

void DataBase::get_m(int key_id){
    int skip = get_collector_address(key_id);
    if (skip == -1) {
        printf("Error, key_id %d \n", key_id);
        return;
    }

    FILE* banks_file_m = fopen(file_m, "rb+");
    fseek(banks_file_m, skip+4, SEEK_SET);
    char name[20], country[20];
    int  first_filial;
    fread(&name, sizeof(name), 1, banks_file_m);
    fread(&country, sizeof(country), 1, banks_file_m);
    fread(&first_filial, sizeof(int), 1, banks_file_m);
    printf("Bank id = %d, Bank name= %s, Bank country= %s\n",
           key_id, name, country);
    fclose(banks_file_m);
}

void DataBase:: get_s(int key_id_m, int key_id_s){
    int skip_m = get_collector_address(key_id_m);
    if (skip_m == -1) {
        printf("Error, key_id %d \n", key_id_m);
        return;
    }

    FILE* banks_file_m = fopen(file_m, "rb+");
    fseek(banks_file_m, skip_m, SEEK_SET);
    int  first_filial;
    fseek(banks_file_m, skip_m + 44 ,SEEK_SET);
    fread(&first_filial, sizeof(int), 1, banks_file_m);
    fclose(banks_file_m);


    if(first_filial == -1){
        printf("Bank without filials\n");
        return;
    }
    else {
        FILE *filial_file_s = fopen(file_s, "rb+");
        fseek(filial_file_s, first_filial, SEEK_SET);
        char filial_name[20], filial_address[20];
        int new_key_id_s;
        int next_filial = first_filial;
        int current_address = first_filial;
        fread(&new_key_id_s, sizeof(int), 1, filial_file_s);
        while (new_key_id_s != key_id_s) {
            if (next_filial == -1) {
                printf("Bank %d doesn't have filial %d\n", key_id_m, key_id_s);
                return;
            }
            fseek(filial_file_s, next_filial, SEEK_SET);
            fread(&new_key_id_s, sizeof(int), 1, filial_file_s);
            current_address = next_filial;
            fseek(filial_file_s, next_filial + 48, SEEK_SET);
            fread(&next_filial, sizeof(int), 1, filial_file_s);
        }
        int deleted = -1;
        fseek(filial_file_s, current_address + 8, SEEK_SET);
        fread(filial_name, sizeof(filial_name), 1, filial_file_s);
        fread(filial_address, sizeof(filial_address), 1, filial_file_s);
        fseek(filial_file_s, sizeof(int), SEEK_CUR);
        fread(&deleted, sizeof(int), 1, filial_file_s);

        if (deleted == 0) {
            printf("Bank id: %d Filial id: %d Filial name: %s Filial address: %s\n", key_id_m, key_id_s, filial_name,
                   filial_address);
        } else {
            printf("Bank %d doesn't have filial %d(prev_deleted)\n", key_id_m, key_id_s);
        }

        fclose(banks_file_m);

    }
    }

