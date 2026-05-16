#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <ctime>
#include <vector>
#include <algorithm>
#include <string>
using namespace std;

const int MAX = 200000;

struct Car {
    int id, hp, stock;
    char brand[50], model[50], type[20];
    double price;
};

// Сортировка по возрастанию
bool cmpByIdAsc(const Car& a, const Car& b) { return a.id < b.id; } 
bool cmpByBrandAsc(const Car& a, const Car& b) { return strcmp(a.brand, b.brand) < 0; } 
bool cmpByModelAsc(const Car& a, const Car& b) { return strcmp(a.model, b.model) < 0; } 
bool cmpByPriceAsc(const Car& a, const Car& b) { return a.price < b.price; } 
bool cmpByHpAsc(const Car& a, const Car& b) { return a.hp < b.hp; }         
bool cmpByStockAsc(const Car& a, const Car& b) { return a.stock < b.stock; } 
bool cmpByTypeAsc(const Car& a, const Car& b) { return strcmp(a.type, b.type) < 0; }

// Сортировка по убыванию
bool cmpByIdDesc(const Car& a, const Car& b) { return a.id > b.id; }   
bool cmpByBrandDesc(const Car& a, const Car& b) { return strcmp(a.brand, b.brand) > 0; } 
bool cmpByModelDesc(const Car& a, const Car& b) { return strcmp(a.model, b.model) > 0; } 
bool cmpByPriceDesc(const Car& a, const Car& b) { return a.price > b.price; }
bool cmpByHpDesc(const Car& a, const Car& b) { return a.hp > b.hp; }   
bool cmpByStockDesc(const Car& a, const Car& b) { return a.stock > b.stock; } 
bool cmpByTypeDesc(const Car& a, const Car& b) { return strcmp(a.type, b.type) > 0; }

int main(int argc, char* argv[]) {
    if(argc!=5) return 1; // 5 аргументов вместо 4
    char* infile=argv[1], *outfile=argv[2], *key=argv[3], *order=argv[4];
    
    bool (*cmp)(const Car&,const Car&);
    
    if(strcmp(key,"id")==0) {
        if(strcmp(order,"asc")==0) cmp = cmpByIdAsc;    
        else cmp = cmpByIdDesc;                         
    }
    else if(strcmp(key,"brand")==0) {
        if(strcmp(order,"asc")==0) cmp = cmpByBrandAsc; 
        else cmp = cmpByBrandDesc;                     
    }
    else if(strcmp(key,"model")==0) {
        if(strcmp(order,"asc")==0) cmp = cmpByModelAsc; 
        else cmp = cmpByModelDesc;                     
    }
    else if(strcmp(key,"price")==0) {
        if(strcmp(order,"asc")==0) cmp = cmpByPriceAsc;
        else cmp = cmpByPriceDesc;                    
    }
    else if(strcmp(key,"horsepower")==0) {
        if(strcmp(order,"asc")==0) cmp = cmpByHpAsc; 
        else cmp = cmpByHpDesc;                          
    }
    else if(strcmp(key,"stock")==0) {
        if(strcmp(order,"asc")==0) cmp = cmpByStockAsc;  
        else cmp = cmpByStockDesc;                       
    }
    else {
        if(strcmp(order,"asc")==0) cmp = cmpByTypeAsc;  
        else cmp = cmpByTypeDesc;                    
    }
    
    printf("============================================================\n");
    printf("НАЧАЛО ВНЕШНЕЙ СОРТИРОВКИ (C++)\n");
    printf("Порядок: %s\n", strcmp(order,"asc")==0 ? "по возрастанию" : "по убыванию"); 
    printf("============================================================\n");
    
    FILE* in=fopen(infile,"r");
    vector<string> tmp;
    vector<Car> chunk;
    char line[500];
    
    int n=0;
    int total_lines = 0; 
    
    printf("\n[ЭТАП 1] РАЗБИЕНИЕ ФАЙЛА НА БЛОКИ\n");
    
    while(fgets(line,sizeof(line),in)){
        Car c;
        char* p=strtok(line,",");
        c.id=atoi(p);
        p=strtok(NULL,","); strcpy(c.brand,p?p:"");
        p=strtok(NULL,","); strcpy(c.model,p?p:"");
        p=strtok(NULL,","); c.price=p?atof(p):0;
        p=strtok(NULL,","); c.hp=p?atoi(p):0;
        p=strtok(NULL,","); c.stock=p?atoi(p):0;
        p=strtok(NULL,"\n\r"); strcpy(c.type,p?p:"");
        chunk.push_back(c);
        total_lines++;
        
        if(chunk.size()>=MAX){
            sort(chunk.begin(),chunk.end(),cmp);  // = функция сравнения
            char name[100]; sprintf(name,"tmp%d.txt",n++);
            FILE* f=fopen(name,"w");
            for(auto& cc:chunk) fprintf(f,"%d,%s,%s,%.2f,%d,%d,%s\n",cc.id,cc.brand,cc.model,cc.price,cc.hp,cc.stock,cc.type);
            fclose(f);
            tmp.push_back(name);
            chunk.clear();
            printf("  Блок %d: %d строк\n", n, MAX); 
        }
    }
    
    if(!chunk.empty()){
        sort(chunk.begin(),chunk.end(),cmp);  // = функция сравнения
        char name[100]; sprintf(name,"tmp%d.txt",n++);
        FILE* f=fopen(name,"w");
        for(auto& cc:chunk) fprintf(f,"%d,%s,%s,%.2f,%d,%d,%s\n",cc.id,cc.brand,cc.model,cc.price,cc.hp,cc.stock,cc.type);
        fclose(f);
        tmp.push_back(name);
        printf("  Блок %d: %zu строк\n", n, chunk.size()); 
    }
    fclose(in);
    
    printf("\n  ИТОГО: %d блоков, %d строк обработано\n", n, total_lines); 
    
    vector<FILE*> files;
    for(auto& fname:tmp) files.push_back(fopen(fname.c_str(),"r"));
    
    vector<string> lines(files.size());
    vector<Car> cars(files.size());
    vector<bool> active(files.size(),false);
    
    printf("\n[ЭТАП 2] СЛИЯНИЕ БЛОКОВ\n");
    
    for(size_t i=0;i<files.size();i++){
        if(fgets(line,sizeof(line),files[i])){
            lines[i]=line;
            char* p=strtok(line,",");
            cars[i].id=p?atoi(p):0;
            p=strtok(NULL,","); if(p) strcpy(cars[i].brand,p);
            p=strtok(NULL,","); if(p) strcpy(cars[i].model,p);
            p=strtok(NULL,","); cars[i].price=p?atof(p):0;
            p=strtok(NULL,","); cars[i].hp=p?atoi(p):0;
            p=strtok(NULL,","); cars[i].stock=p?atoi(p):0;
            p=strtok(NULL,"\n\r"); if(p) strcpy(cars[i].type,p);
            active[i]=true;
        }
    }
    
    FILE* out=fopen(outfile,"w");
    int total=0;
    
    while(1){
        int best=-1;
        for(size_t i=0;i<files.size();i++)
            if(active[i] && (best==-1 || cmp(cars[i],cars[best]))) best=i; 
        if(best==-1) break;
        
        fprintf(out,"%s",lines[best].c_str());
        total++;
        
        if(total % 1000000 == 0) { 
            printf("  Записано %d строк\r", total);
            fflush(stdout);
        }
        
        if(fgets(line,sizeof(line),files[best])){
            lines[best]=line;
            char* p=strtok(line,",");
            cars[best].id=p?atoi(p):0;
            p=strtok(NULL,","); if(p) strcpy(cars[best].brand,p);
            p=strtok(NULL,","); if(p) strcpy(cars[best].model,p);
            p=strtok(NULL,","); cars[best].price=p?atof(p):0;
            p=strtok(NULL,","); cars[best].hp=p?atoi(p):0;
            p=strtok(NULL,","); cars[best].stock=p?atoi(p):0;
            p=strtok(NULL,"\n\r"); if(p) strcpy(cars[best].type,p);
        } else active[best]=false;
    }
    
    printf("\n  Записано %d строк\n", total);
    
    fclose(out);
    for(auto f:files) fclose(f);
    for(auto& fname:tmp) remove(fname.c_str());
    
    printf("\n[ЭТАП 3] ОЧИСТКА\n");
    printf("  Временные файлы удалены: %d шт.\n", (int)tmp.size());
    printf("\n============================================================\n");
    printf("СОРТИРОВКА ЗАВЕРШЕНА УСПЕШНО!\n");
    printf("============================================================\n");
    
    return 0;
}
