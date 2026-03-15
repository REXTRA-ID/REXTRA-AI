"""
app/models/__init__.py
----------------------
Re-export semua model agar bisa diimport dari satu tempat.

Contoh:
    from app.models import Profession, Skill, Tool
"""

from app.models.profession_main_category import ProfessionMainCategory
from app.models.profession_sub_category import ProfessionSubCategory
from app.models.profession import Profession
from app.models.profession_activity import ProfessionActivity
from app.models.profession_career_path import ProfessionCareerPath
from app.models.skill import Skill
from app.models.profession_skill_rel import ProfessionSkillRel
from app.models.tool import Tool
from app.models.profession_tool_rel import ProfessionToolRel
from app.models.profession_alias import ProfessionAlias
from app.models.profession_market_insight import ProfessionMarketInsight
from app.models.profession_study_program_rel import ProfessionStudyProgramRel

__all__ = [
    "ProfessionMainCategory",
    "ProfessionSubCategory",
    "Profession",
    "ProfessionActivity",
    "ProfessionCareerPath",
    "Skill",
    "ProfessionSkillRel",
    "Tool",
    "ProfessionToolRel",
    "ProfessionAlias",
    "ProfessionMarketInsight",
    "ProfessionStudyProgramRel",
]
