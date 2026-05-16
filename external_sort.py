import os, tempfile, heapq, time

MAX_ROWS = 150000

def external_sort(infile, outfile, key, order="asc"): # ===

    idx = {'id':0,'brand':1,'model':2,'price':3,'horsepower':4,'stock':5,'vehicle_type':6}[key]
    num = key in ['id','price','horsepower','stock']
    
    # === Определяем reverse для сортировки
    reverse = (order == "desc")
    
    print("=" * 60)
    print(f"НАЧАЛО ВНЕШНЕЙ СОРТИРОВКИ (Python)")
    print(f"Порядок: {'по убыванию' if reverse else 'по возрастанию'}")  # ===
    print("=" * 60)
    
    # Разбиение
    tmp = []
    chunk = []
    n = 0
    total_lines = 0
    
    print("\n[ЭТАП 1] РАЗБИЕНИЕ ФАЙЛА НА БЛОКИ")
    
    with open(infile) as f:
        for line in f:
            chunk.append(line.strip())
            total_lines += 1
            if len(chunk) >= MAX_ROWS:
                # === Добавление reverse в сортировку
                chunk.sort(key=lambda x: float(x.split(',')[idx]) if key=='price' else int(x.split(',')[idx]) if num else x.split(',')[idx], reverse=reverse)  # ==
                t = tempfile.NamedTemporaryFile(mode='w', delete=False)
                t.write('\n'.join(chunk))
                t.close()
                tmp.append(t.name)
                chunk = []
                n += 1
                print(f"  Блок {n}: {MAX_ROWS:,} строк")
                
    if chunk:
        # === Добавление reverse в сортировку
        chunk.sort(key=lambda x: float(x.split(',')[idx]) if key=='price' else int(x.split(',')[idx]) if num else x.split(',')[idx], reverse=reverse)  # ==
        t = tempfile.NamedTemporaryFile(mode='w', delete=False)
        t.write('\n'.join(chunk))
        t.close()
        tmp.append(t.name)
        n += 1
        print(f"  Блок {n}: {len(chunk):,} строк")
    
    print(f"\n  ИТОГО: {n} блоков, {total_lines:,} строк")
    
    # Слияние
    print("\n[ЭТАП 2] СЛИЯНИЕ БЛОКОВ")
    
    files = [open(f) for f in tmp]
    heap = []
    
    for i,f in enumerate(files):
        line = f.readline()
        if line:
            val = float(line.split(',')[idx]) if key=='price' else int(line.split(',')[idx]) if num else line.split(',')[idx]
            if reverse and num: 
                val = -val     # === Инвертируем числовые значения для обратного порядка
            heap.append((val, i, line.strip()))
    
    heapq.heapify(heap)
    
    with open(outfile, 'w') as out:
        written = 0
        while heap:
            val,i,line = heapq.heappop(heap)
            out.write(line+'\n')
            written += 1
            
            if written % 1000000 == 0:
                print(f"  Записано {written:,} строк", end='\r')
            
            line = files[i].readline()
            if line:
                new_val = float(line.split(',')[idx]) if key=='price' else int(line.split(',')[idx]) if num else line.split(',')[idx]

                # === Инверсия для порядка убывания
                if reverse and num:    
                    new_val = -new_val
                heapq.heappush(heap, (new_val, i, line.strip()))
    
    print(f"\n  Записано {written:,} строк")
    
    for f in files:
        f.close()
    for f in tmp:
        os.remove(f)
    
    print(f"\nВРЕМЕННЫЕ ФАЙЛЫ УДАЛЕНЫ: {len(tmp)} шт.")
