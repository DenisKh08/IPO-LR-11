import requests
from bs4 import BeautifulSoup
import json

def main():
    url = "https://www.scrapethissite.com/pages/simple/"
    
    with requests.Session() as session:
        response = session.get(url)
        
        if not response.ok:
            print(f"Failed to fetch page: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.content, 'html.parser')
        countries = soup.select('div.country')
        countries_list = []
        
        for idx, country in enumerate(countries, 1):
            name = country.select_one('h3.country-name').get_text(strip=True)
            capital = country.select_one('span.country-capital').get_text(strip=True)
            
            print(f"{idx}. Country: {name}; Capital: {capital};")
            
            country_info = {
                "id": idx,
                "name": name,
                "capital": capital
            }
            countries_list.append(country_info)
    
    
    table_rows = ''
    for country in countries_list:
        table_rows += f'''
        <tr>
            <td>{country['id']}</td>
            <td>{country['name']}</td>
            <td>{country['capital']}</td>
        </tr>
        '''
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Countries Information</title>
    <style>
        body 
        {{
            text-align: center;
            background-color: #f5f5f5;
        }}
        table 
        {{
            margin: 0 auto;
            background-color: white;
        }}
        th 
        {{
            background-color: #4CAF50;
            color: white;
        }}
        tr:nth-child(even) 
        {{
            background-color: #f2f2f2;
        }}
        tr:hover 
        {{
            background-color: #e0f7fa;
        }}
    </style>
</head>
<body>
    <h1 style="color: #2c3e50;">Countries and Their Capitals</h1>
    <table border="1" cellpadding="10" cellspacing="0">
        <tr>
            <th>№</th>
            <th>Country</th>
            <th>Capital</th>
        </tr>
        {table_rows}
    </table>
    <br>
    <p>Source: <a href="https://www.scrapethissite.com/pages/simple/">https://www.scrapethissite.com/pages/simple/</a></p>
</body>
</html>'''
    
    #сохраняем HTML файл
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    #сохраненяем JSON файл
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(countries_list, f, ensure_ascii=False, indent=2)
    
    print(f"\nHTML файл создан: 'index.html'")
    print(f"JSON файл создан: 'data.json'")

if __name__ == "__main__":
    main()
