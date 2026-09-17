import sys
import re

file_path = 'd:\\Documents\\rextra\\REXTRA-AI\\scripts\\seed_digital_professions.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix imports
content = content.replace(
    'from app.models.profession import Profession as DigitalProfession',
    '''from app.models.profession import Profession as DigitalProfession
from app.models.profession_main_category import ProfessionMainCategory
from app.models.profession_sub_category import ProfessionSubCategory
from datetime import datetime'''
)

# Fix insertion logic
old_logic = '''            # Insert new profession
            new_profession = DigitalProfession(
                title=title,
                description=prof_data["description"],
                riasec_code_id=riasec_code_id,
                meta_data=prof_data["meta_data"]
            )
            db.add(new_profession)'''

new_logic = '''            # Get or create dummy categories
            main_cat = db.execute(select(ProfessionMainCategory).where(ProfessionMainCategory.code == 'TECH')).scalar_one_or_none()
            if not main_cat:
                main_cat = ProfessionMainCategory(
                    code='TECH', name='Technology', description='Tech roles',
                    created_at=datetime.now(), updated_at=datetime.now()
                )
                db.add(main_cat)
                db.flush()
            
            sub_cat = db.execute(select(ProfessionSubCategory).where(ProfessionSubCategory.code == 'GEN_TECH')).scalar_one_or_none()
            if not sub_cat:
                sub_cat = ProfessionSubCategory(
                    main_category_id=main_cat.id, code='GEN_TECH', name='General Tech', description='General tech roles',
                    created_at=datetime.now(), updated_at=datetime.now()
                )
                db.add(sub_cat)
                db.flush()

            # Insert new profession
            new_profession = DigitalProfession(
                name=title,
                slug=title.lower().replace(" ", "-").replace("/", "-"),
                about_description=prof_data["description"],
                riasec_code_id=riasec_code_id,
                main_category_id=main_cat.id,
                sub_category_id=sub_cat.id,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.add(new_profession)'''

content = content.replace(old_logic, new_logic)

# Fix existing query
content = content.replace('DigitalProfession.title == title', 'DigitalProfession.name == title')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
