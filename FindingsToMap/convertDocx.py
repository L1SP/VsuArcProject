import csv
import base64
import sys
import os
import glob
import re
import http.client
import json
from docx import Document

# Получение сведений о местоположении
def getInfoByAddress(address):
    apiKey = "#insert API key here"
    secret = "#insert secret here" 
    connection = http.client.HTTPSConnection('cleaner.dadata.ru')
    headers = {'Content-type': 'application/json', 'Accept': 'application/json', 'Authorization': f'Token {apiKey}', 'X-Secret': secret}
    body = json.dumps([address])
    connection.request('POST', '/api/v1/clean/address', body, headers)
    response = connection.getresponse()
    return response.read().decode()

# Названия колонок
def generate_first_row(csv_writer):
    column = ["object_id", "object_card_date", "object_card_author", "object_information_year",
              "object_information_source", "object_information_receive_type", "object_origin_place",
              "object_information_act_number", "object_excavation_date", "object_name",
              "object_description", "object_count", "object_material", "object_size", "object_preservation", 
              "object_registration_number", "object_storage_place", "object_inventory_number", "object_note",
              "object_media", "object_geodata"]
    csv_writer.writerow(column)

# Конвертация документа в csv-файл
def convert_docx_to_csv(docx_path, img_path, csv_path):
	
    # Открываем файл DOCX
    doc = Document(docx_path)
    table = doc.tables[0] # Получаем таблицу из документа
    rowsRangeLength = len(table.rows) # кол-во строк (2208)

    # Открываем и заполняем csv-файл
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        generate_first_row(csv_writer) # Генерируем названия колонок
        row_num = 1
        group_num = "0"
        
        # Заполнение строк
        while row_num < rowsRangeLength: 
            row = table.rows[row_num] # Рассматриваем каждую строку
            row_elements = [] # Элементы новой строки         
            formatted = re.sub(r"[\s\n]", r"", row.cells[0].text) # Убираем лишние пробелы
            
            # Если обобщенная строка
            if re.search(r"\d+/1-\d+", formatted):
                group_num = re.sub(r"(\d+)/1-\d+", r"\1", formatted) # Номер обобщенной строки
                formatted = re.sub(r"\n", r" ", row.cells[2].text + ' . ' + row.cells[3].text)
                # object_information_year
                search = re.search(r"\d{4}\s?[–-]\s?\d{4}\sгг\.|(?<!\.)\d{4}", formatted) 
                if search:
                    information_year = re.sub(r"(\d{4})\s?[–-]\s?(\d{4}\sгг\.)", r"\1-\2", search.group(0))
                    information_year = re.sub(r"(?<!-)(\d{4})(?!-)", r"\1 г.", information_year)
                else:
                    information_year = ""
                # object_information_source
                search = re.search(r"Материалы [^А-ЯЁ]*?[А-ЯЁ]\.[А-ЯЁ]\.\s*[А-ЯЁ][а-яё]+|Материалы [^А-ЯЁ]*?[А-ЯЁ][а-яё]+\s+[А-ЯЁ]\.\s?[А-ЯЁ]\.|Случайные находки", formatted)
                if search:
                    information_source = search.group(0)
                else:
                    information_source = ""
                # object_receive_type
                search = re.search(r"Передано\s+[А-ЯЁ]\.\s?[А-ЯЁ]\.\s?[А-ЯЁ][а-яё]+", row.cells[2].text)
                if search:
                    receive_type = search.group(0)
                else:
                    receive_type = "" 
                # object_origin_place   
                search_list = re.findall(r"(\b[сc]\.[\s\n]?[А-ЯЁа-яё][а-яё]+-?\w*)|([А-ЯЁ][а-яё]+\s)(р-н[еа]?|район[еа]?\b|област[ьи]|обл\.)|(ВО)|могильника (\w+)|(пос\.\s[А-ЯЁ][а-яё]+)|поселени[ия]\s«?([А-ЯЁа-яё]+)|(г\.?\s[А-ЯЁ][а-яё]+)|(ул\.\s?[А-ЯЁ][а-яё]+)|(д\.\s?\d+)|селища\s([А-ЯЁ][а-яё]+)|группы\s([А-ЯЁ][а-яё]+)|могильника\s([А-ЯЁ][а-яё]+)", row.cells[3].text)
                if search_list != []:
                    place = ', '.join(''.join(elems) for elems in search_list)
                    place = re.sub(r"\n|\s+", r" ", place)
                    place = re.sub(r"ВО", r"Воронежская область", place)
                else:
                    place = ""
                # object_act_number 
                search = re.search(r"№[\s\n]?\d+", row.cells[2].text)
                if search:
                    act_number = search.group(0)
                else:
                    act_number = ""
                # object_excavation_date
                search = re.search(r"\d{2}\.\d{2}\.\d{4}", row.cells[2].text)
                if search:
                    date = search.group(0)
                else:
                    date = ""
                row_num += 1
                row = table.rows[row_num]
                row_elements = []
                formatted = re.sub(r"[\s\n]", r"", row.cells[0].text)
                
            # Заполнение object_id
            row_elements.append(formatted) 
            row_elements = [item.replace("/", ".") for item in row_elements]  
                     
            # Заполнение object_card_date
            search = re.search(r"\b\d{4}-\d{2}-\d{2}\b", row.cells[1].text)
            if search:
                formatted = re.sub(r"(\b\d{4})-(\d{2})-(\d{2}\b)", r"\3.\2.\1", search.group(0))
                row_elements.append(formatted.rstrip(", ").lstrip(", ")) 
            else:
                search = re.search(r"\b\d{2}\.\d{2}\.\d{4}\b", row.cells[1].text)
                if search:
                    row_elements.append(search.group(0).rstrip(", ").lstrip(", "))
                else:
                    row_elements.append("")        
                       
            # Заполнение object_card_author   
            search = re.search(r"[А-ЯЁ][а-яё]+\.?\s*[А-ЯЁ]\.\s*[А-ЯЁ]\.?", row.cells[1].text)
            if search:
                formatted = re.sub(r"(\w+)\.?\s*([А-ЯЁ])\.\s*([А-ЯЁ])\.?", r"\1 \2.\3.", search.group(0))
                row_elements.append(formatted.rstrip(", ").lstrip(", ")) 
            else:
                row_elements.append("")
                
            # Если принадлежит обобщенной строке
            if re.search(r"\d+\.\d+", row_elements[0]) and re.sub(r"(\d+)\.\d+", r"\1", re.search(r"\d+\.\d+", row_elements[0]).group(0)) == group_num:
                row_elements.append(information_year)
                row_elements.append(information_source)
                row_elements.append(receive_type)
                row_elements.append(place)
                row_elements.append(act_number)
                row_elements.append(date)
            else:  
			# Заполнение object_information_year             
                search = re.search(r"(?<!\d\.)\d{4}\s?г[,\.]|(?<!\d\.)\d{4}\s*году", row.cells[2].text)
                if search:
                    formatted = re.sub(r"(\d+).*", r"\1 г.", search.group(0))
                    row_elements.append(formatted.rstrip(", ").lstrip(", ")) 
                else:
                    search = re.search(r"\d{4}\s?[–-]\s?\d{4}\s?гг\.", row.cells[2].text)
                    if search:
                        formatted = re.sub(r"(\d{4})\s?[–-]\s?(\d{4})\s?(гг\.)", r"\1-\2 \3", search.group(0))
                        row_elements.append(formatted.rstrip(", ").lstrip(", "))
                    else:
                        row_elements.append("")
                        
            # Заполнение object_information_source
                formatted = re.sub(r"\n", r" ", row.cells[2].text)
                search = re.search(r"Материалы.*?[А-ЯЁа-яё]\.\s*[А-ЯЁ]\.?\s*[А-ЯЁ][а-яё]+|М[ае]териалы.*?[А-ЯЁ][а-яё]+\s+[А-ЯЁ]\.\s*[А-ЯЁ]\.|Раскопки [А-ЯЁ]\.\s*[А-ЯЁ]\.\s+[А-ЯЁ][а-яё]+|Случайная находка|Фонды \w+|(Музей-заповедник.*?),|Сборы(\s+[А-ЯЁ]\.\s*[А-ЯЁ]\.\s+[А-ЯЁ][а-яё]+)?|Материалы раскопок", formatted)
                if search:
                    row_elements.append(search.group().rstrip(", ").lstrip(", ")) 
                else:
                    row_elements.append("")
                    
            # Заполнение object_information_receive_type
                search = re.search(r"Дар|Передано[\n\s]*[А-ЯЁа-яё]\.\s*[А-ЯЁ]\.?\s*[А-ЯЁ][а-яё]+|Передано .*,", row.cells[2].text)
                if search:
                    row_elements.append(search.group(0).rstrip(", ").lstrip(", "))
                else:
                    row_elements.append("")  
                    
            # Заполнение object_place  
                formatted = row.cells[2].text + ' . ' + row.cells[3].text 
                formatted = re.sub(r"\n|\s+", r" ", formatted) 
                search_list = re.findall(r"(\b[сc]\.[\s\n]?[А-ЯЁа-яё][а-яё]+-?\w*(?<!на|ва|ым)\b)|\b([Пп]о?с?\.\s?[А-ЯЁа-яё][а-яё]+(?<!на|ва|ым)\b)|\b([Дд](ер)?\.\s?[А-ЯЁа-яё][а-яё]+(?<!на|ва|ым)\b)|\b([Хх]\.\s?[А-ЯЁа-яё][а-яё]+)|(\w+\.?\s?)(р-[о]?н[еа]?|район[еа]?\b|област[ьи]|обл\.|край\b)|((?<!\d{4}\s)\b[Гг]о?р?\.\s?[А-ЯЁа-яё][а-яё]+(?<!на|ва|ым|но)\b)|(\b[Вв]О\b)|\b(р|респ)(\.\s?\w+)|(\b[Сс]т\.\n?\s?\w+)|(\w+\s(кордон|городище))|Музей-заповедник\s?(.*?),|(\w+\s[Лл]ог)|([А-ЯЁ][а-яё]+\s(поселени[ея]|площадь))", formatted)
                if search_list != []:
                    formatted = ', '.join(''.join(elems) for elems in search_list)
                    formatted = re.sub(r"\n|\s+", r" ", formatted)
                    formatted = re.sub(r"[Вв]О|[Вв]ор\.\s?обл\.|[Вв]оронеж\.\s?обл|[Вв]орон\.\s?обл", r"Воронежская область", formatted)
                    row_elements.append(formatted.rstrip(", ").lstrip(", "))
                else:
                    row_elements.append("")   
                      
            # Заполнение object_information_act_number
                search = re.search(r"№[\s\n]?\d+", row.cells[2].text)
                if search:
                    row_elements.append(search.group(0).rstrip(", ").lstrip(", ")) 
                else:
                    row_elements.append("") 
                    
            # Заполнение object_excavation_date    
                search = re.search(r"\d{2}\.\d{2}\.\d{4}", row.cells[2].text)
                if search:
                    row_elements.append(search.group(0).rstrip(", ").lstrip(", ")) 
                else:
                    row_elements.append("")
                    
            # Заполнение object_name     
            formatted = re.sub(r";", r",", row.cells[3].text)
            search = re.search(r".*?[:–\(,\.]", formatted, re.DOTALL)
            if search:
                formatted = re.sub(r"[:–\(\.]", r"", search.group(0))
                row_elements.append(formatted.rstrip(", ").lstrip(", ")) 
            else:
                row_elements.append(row.cells[3].text)  
                
            # Заполнение object_description  
            formatted = re.sub(r"\n", r" ", row.cells[3].text)  
            formatted = re.sub(r";", r",", formatted) 
            index1 = formatted.find(",") 
            index2 = formatted.find(".")
            if index1 != -1:
                if index2 == -1:
                    row_elements.append(formatted[index1 + 2:].rstrip(", ").lstrip(", "))
                else:
                    if index1 < index2:
                        row_elements.append(formatted[index1 + 2:].rstrip(", ").lstrip(", "))
                    else:
                        row_elements.append(formatted[index2 + 2:].rstrip(", ").lstrip(", "))
            else:
                if index2 != -1:
                    row_elements.append(formatted[index2 + 2:].rstrip(", ").lstrip(", "))
                else:
                    row_elements.append("") 
            if re.search(r"^[а-яё]", row_elements[10]):
                row_elements[10] = re.sub(r"^[а-яё]", lambda match: match.group(0).upper(), row_elements[10])  
                     
            # Заполнение object_count
            row_elements.append(row.cells[4].text)   
                    
            # Заполнение object_material
            formatted = re.sub(r"[,\.]\s*$", "", row.cells[5].text)
            row_elements.append(formatted.rstrip(", ").lstrip(", ")) 
            
            # Заполнение object_size
            formatted = re.sub(r"\s?[\*хХ]\s?", r" x ", row.cells[6].text)
            formatted = re.sub(r";", r"", formatted)
            row_elements.append(formatted.rstrip(", ").lstrip(", "))
            
            # Заполнение object_preservation
            formatted = re.sub(r"\.\s*$|\t", "", row.cells[7].text)
            row_elements.append(formatted.rstrip(", ").lstrip(", "))  
                      
            # Заполнение object_registration_number
            formatted = re.sub(r"\n|\t", "", row.cells[8].text)
            row_elements.append(formatted.rstrip(", ").lstrip(", ")) 
            
            # Заполнение object_storage_place
            row_elements.append(row.cells[9].text) 
                       
            # Заполнение object_inventory_number
            row_elements.append(row.cells[10].text) 
            
            # Заполнение object_note
            row_elements.append(row.cells[11].text) 
            
            # Заполнение object_media 
            files = os.listdir(img_path)
            formatted = ""
            pattern = re.compile(fr"{row_elements[0]}\..*|{row_elements[0]}\s?-\d+\..*|{row_elements[0]}\s?[('].*")
            for file in files:
                if re.match(pattern, file):
                    formatted += file + ", "
            row_elements.append(formatted)
            
            # Заполнение object_geodata
            if row_elements[6] != "":
                row_elements.append(getInfoByAddress(row_elements[6])) 
            else:
                row_elements.append("")  
            csv_writer.writerow(row_elements)
            row_num += 1
            
csv_path = 'finds.csv'

if len(sys.argv) == 3:
    convert_docx_to_csv(sys.argv[1], sys.argv[2], csv_path)
elif len(sys.argv) == 4:
    convert_docx_to_csv(sys.argv[1], sys.argv[2], sys.argv[3])
elif len(sys.argv) > 4:
    convert_docx_to_csv(sys.argv[1], sys.argv[2], sys.argv[3], False)
else:
    print("python3 convertDocx.py имя_исходного_docx имя_папки_с_изображениями [имя конечного csv знак заголовка]")
