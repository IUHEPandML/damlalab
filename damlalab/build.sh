#!/usr/bin/env bash
# Herhangi bir hata oluşursa betiği durdur
set -o errexit

# Bağımlılıkları yükle
pip install -r requirements.txt

# Statik dosyaları topla
python manage.py collectstatic --no-input

# Veritabanı tablolarını Render üzerinde oluştur/güncelle
python manage.py migrate