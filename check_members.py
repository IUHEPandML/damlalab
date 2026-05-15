import sqlite3
import sys
sys.path.insert(0, 'damlalab')
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'damlalab.settings')

import django
django.setup()

from sayfalar.models import Person, ThesisParticipation, ProjectParticipation

print("=== TOPLAM PERSON KAYITLARI ===")
all_persons = Person.objects.all().order_by('name')
print(f"Toplam: {all_persons.count()}")
for person in all_persons:
    print(f"  ID: {person.id}, İsim: {person.name}")

print("\n=== TEZ KATILIMCıLARI (ThesisParticipation) ===")
thesis_persons = Person.objects.filter(thesisparticipation__isnull=False).distinct().order_by('name')
print(f"Toplam: {thesis_persons.count()}")
for person in thesis_persons:
    print(f"  ID: {person.id}, İsim: {person.name}")

print("\n=== PROJE KATILIMCıLARI (ProjectParticipation) ===")
project_persons = Person.objects.filter(projectparticipation__isnull=False).distinct().order_by('name')
print(f"Toplam: {project_persons.count()}")
for person in project_persons:
    print(f"  ID: {person.id}, İsim: {person.name}")

print("\n=== MEMBERS SAYFASINDA GÖRÜLECEK KİŞİLER (Tez VEYA Proje) ===")
from django.db.models import Q
active_persons = Person.objects.filter(
    Q(thesisparticipation__isnull=False) | Q(projectparticipation__isnull=False)
).distinct().order_by('name')
print(f"Toplam: {active_persons.count()}")
for person in active_persons:
    print(f"  ID: {person.id}, İsim: {person.name}")

print("\n=== KAYITLARDA ANCAK MEMBERS'DA GÖRÜLMEYECEK KİŞİLER ===")
orphan_persons = Person.objects.exclude(
    Q(thesisparticipation__isnull=False) | Q(projectparticipation__isnull=False)
).order_by('name')
if orphan_persons.exists():
    print(f"Toplam: {orphan_persons.count()}")
    for person in orphan_persons:
        print(f"  ID: {person.id}, İsim: {person.name}")
else:
    print("Yok - Tüm kişiler bir tez veya proje ile ilişkili!")
