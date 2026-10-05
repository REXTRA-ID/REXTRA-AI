import re

path = 'app/models/profession.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'(?ms)^\s*from app\.models\.profession_study_program_rel import ProfessionStudyProgramRel.*?$', '', content)
content = re.sub(r'(?ms)^\s*study_program_rels: Mapped\[list\["ProfessionStudyProgramRel"\]\] = relationship\(.*?lazy="select",\s*\)\s*$', '', content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
