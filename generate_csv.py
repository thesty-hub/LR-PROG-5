#!/usr/bin/env python3
import csv
import random
import sys

BRANDS = ['Toyota','Honda','Ford','Chevrolet','BMW','Mercedes','Audi','Nissan','Hyundai','Kia',
          'Volkswagen','Subaru','Mazda','Volvo','Tesla','Lexus','Jeep','Ram','GMC','Acura']

MODELS = ['Civic','Accord','Corolla','Camry','F-150','Mustang','3 Series','X5','A4','Q5',
          'Model S','Model 3','CX-5','Outback','Wrangler','Silverado','Fusion','Focus','Sentra','Altima']

VEHICLE_TYPES = ['passenger','truck']

def generate_csv(filename, num_rows=25_000_000):
    # Генерация CSV-файла размера >1 ГБ при 25 млн строк

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        # Открытие файла для записи с кодировкой UTF-8
        # newline='' - отключает преобразование символов перевода строки
        
        writer = csv.writer(f)
        # Создание объекта для записи CSV
        
        batch_size = 50000
        # Размер пакета строк для записи (по 50000 строк за раз)
        
        for start in range(0, num_rows, batch_size):
            # Цикл по пакетам от 0 до общего количества строк с шагом batch_size
            
            batch = []
            # Создание пустого списка для текущего пакета строк
            
            end = min(start + batch_size, num_rows)
            # Вычисление конечного индекса пакета (не больше общего количества строк)
            
            for i in range(start, end):                
                car_id = i + 1                
                brand = random.choice(BRANDS)
                model = random.choice(MODELS)
                price = round(random.uniform(10000, 100000), 2)
                horsepower = random.randint(80, 800)
                stock = random.randint(0, 500)
                vehicle_type = random.choice(VEHICLE_TYPES)
                
                batch.append([car_id, brand, model, price, horsepower, stock, vehicle_type])
                # Добавление сгенерированной строки в пакет
                
            writer.writerows(batch)
            # Запись всех строк пакета в файл одной операцией (для производительности)
            print(f"Прогресс: {end}/{num_rows} строк", end='\r')
            
    print(f"\nФайл {filename} создан, строк: {num_rows}")

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'data.csv'
    rows = int(sys.argv[2]) if len(sys.argv) > 2 else 25_000_000
    generate_csv(out, rows)
