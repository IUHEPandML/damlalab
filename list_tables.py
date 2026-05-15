import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'damlalab.settings')

sys.path.insert(0, 'damlalab')

import django
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    print('=== VERITABANINDAKI TÜM TABLOLAR ===\n')
    for table in tables:
        table_name = table[0]
        print(f'• {table_name}')
        
        # Her tablo için sütunları göster
        cursor.execute(f'PRAGMA table_info({table_name})')
        columns = cursor.fetchall()
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            print(f'    - {col_name} ({col_type})')
        print()
