#!/usr/bin/env python3
"""
RIASEC Codes Seeder Script

Seeds the riasec_codes table with Holland's RIASEC personality types.
This is a prerequisite for seeding digital_professions.

Usage:
    python -m scripts.seed_riasec_codes

RIASEC Types:
    R - Realistic: Hands-on, practical
    I - Investigative: Analytical, intellectual
    A - Artistic: Creative, expressive
    S - Social: Helping, interpersonal
    E - Enterprising: Persuading, leading
    C - Conventional: Organizing, detail-oriented
"""
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select, text
from app.db.session import SessionLocal
from app.api.v1.categories.career_profile.models.riasec import RIASECCode


# =============================================================================
# RIASEC CODES DATA
# =============================================================================
# Single letter codes (primary types)
# Dual letter codes (combination types)

RIASEC_CODES_DATA = [
    # =========================================================================
    # PRIMARY SINGLE TYPES (6 codes)
    # =========================================================================
    {
        "riasec_code": "R",
        "riasec_title": "Realistic",
        "riasec_description": "Realistic types prefer working with things, tools, machines, and physical activities. They enjoy practical, hands-on problem solving.",
        "strengths": ["Practical skills", "Mechanical ability", "Physical coordination", "Working with tools"],
        "challenges": ["Social interaction", "Abstract thinking", "Expressing emotions"],
        "strategies": ["Focus on hands-on learning", "Seek technical roles", "Build tangible projects"],
        "work_environments": ["Outdoors", "Workshops", "Laboratories", "Construction sites"],
        "interaction_styles": ["Direct", "Task-focused", "Practical"],
        "congruent_code_ids": []  # Will be updated after all codes exist
    },
    {
        "riasec_code": "I",
        "riasec_title": "Investigative",
        "riasec_description": "Investigative types enjoy research, analysis, and understanding complex problems. They prefer intellectual challenges over routine tasks.",
        "strengths": ["Analytical thinking", "Research skills", "Problem solving", "Critical thinking"],
        "challenges": ["Leadership roles", "Persuasion", "Repetitive tasks"],
        "strategies": ["Pursue continuous learning", "Seek research opportunities", "Ask deep questions"],
        "work_environments": ["Research labs", "Universities", "Think tanks", "Tech companies"],
        "interaction_styles": ["Thoughtful", "Reserved", "Curious"],
        "congruent_code_ids": []
    },
    {
        "riasec_code": "A",
        "riasec_title": "Artistic",
        "riasec_description": "Artistic types value creativity, self-expression, and aesthetic pursuits. They prefer unstructured environments that allow innovation.",
        "strengths": ["Creativity", "Imagination", "Self-expression", "Design sense"],
        "challenges": ["Routine work", "Following strict rules", "Detailed procedures"],
        "strategies": ["Seek creative outlets", "Embrace experimentation", "Build portfolio"],
        "work_environments": ["Studios", "Theaters", "Design agencies", "Media companies"],
        "interaction_styles": ["Expressive", "Independent", "Unconventional"],
        "congruent_code_ids": []
    },
    {
        "riasec_code": "S",
        "riasec_title": "Social",
        "riasec_description": "Social types enjoy helping, teaching, and working with others. They value interpersonal relationships and community service.",
        "strengths": ["Communication", "Empathy", "Teaching", "Counseling"],
        "challenges": ["Working alone", "Technical tasks", "Competition"],
        "strategies": ["Develop listening skills", "Seek mentorship roles", "Build communities"],
        "work_environments": ["Schools", "Hospitals", "Community centers", "HR departments"],
        "interaction_styles": ["Friendly", "Supportive", "Collaborative"],
        "congruent_code_ids": []
    },
    {
        "riasec_code": "E",
        "riasec_title": "Enterprising",
        "riasec_description": "Enterprising types enjoy leading, influencing, and persuading others. They value achievement, status, and competitive environments.",
        "strengths": ["Leadership", "Persuasion", "Risk-taking", "Decision making"],
        "challenges": ["Detailed analysis", "Following others", "Patience"],
        "strategies": ["Seek leadership roles", "Develop negotiation skills", "Take calculated risks"],
        "work_environments": ["Corporate offices", "Sales floors", "Startups", "Politics"],
        "interaction_styles": ["Confident", "Persuasive", "Ambitious"],
        "congruent_code_ids": []
    },
    {
        "riasec_code": "C",
        "riasec_title": "Conventional",
        "riasec_description": "Conventional types prefer organized, systematic work with clear rules and procedures. They value accuracy, efficiency, and stability.",
        "strengths": ["Organization", "Attention to detail", "Following procedures", "Data management"],
        "challenges": ["Ambiguity", "Creative tasks", "Unstructured situations"],
        "strategies": ["Create systems", "Document processes", "Seek stable environments"],
        "work_environments": ["Offices", "Banks", "Government agencies", "Accounting firms"],
        "interaction_styles": ["Methodical", "Reliable", "Precise"],
        "congruent_code_ids": []
    },
    
    # =========================================================================
    # DUAL COMBINATION TYPES (15 codes - all possible pairs)
    # =========================================================================
    # R combinations
    {"riasec_code": "RI", "riasec_title": "Realistic-Investigative", 
     "riasec_description": "Combines hands-on skills with analytical thinking. Enjoys technical research and engineering.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "RA", "riasec_title": "Realistic-Artistic", 
     "riasec_description": "Combines craftsmanship with creativity. Enjoys building artistic or design objects.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "RS", "riasec_title": "Realistic-Social", 
     "riasec_description": "Combines practical skills with people orientation. Enjoys teaching trades or physical therapy.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "RE", "riasec_title": "Realistic-Enterprising", 
     "riasec_description": "Combines technical work with leadership. Enjoys managing technical operations.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "RC", "riasec_title": "Realistic-Conventional", 
     "riasec_description": "Combines hands-on work with systematic organization. Enjoys quality control and operations.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    
    # I combinations (excluding IR which equals RI)
    {"riasec_code": "IA", "riasec_title": "Investigative-Artistic", 
     "riasec_description": "Combines research with creativity. Enjoys design research and innovative solutions.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "IS", "riasec_title": "Investigative-Social", 
     "riasec_description": "Combines analysis with helping others. Enjoys psychology, medical research.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "IE", "riasec_title": "Investigative-Enterprising", 
     "riasec_description": "Combines analysis with business acumen. Enjoys consulting and strategy.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "IC", "riasec_title": "Investigative-Conventional", 
     "riasec_description": "Combines research with systematic approaches. Enjoys data science and statistics.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    
    # A combinations
    {"riasec_code": "AS", "riasec_title": "Artistic-Social", 
     "riasec_description": "Combines creativity with helping others. Enjoys art therapy and teaching arts.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "AE", "riasec_title": "Artistic-Enterprising", 
     "riasec_description": "Combines creativity with business skills. Enjoys marketing and creative direction.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "AC", "riasec_title": "Artistic-Conventional", 
     "riasec_description": "Combines creativity with organization. Enjoys technical art and production.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    
    # S combinations
    {"riasec_code": "SE", "riasec_title": "Social-Enterprising", 
     "riasec_description": "Combines helping with leadership. Enjoys management in service industries.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "SC", "riasec_title": "Social-Conventional", 
     "riasec_description": "Combines helping with organization. Enjoys administrative support roles.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    
    # E combinations
    {"riasec_code": "EC", "riasec_title": "Enterprising-Conventional", 
     "riasec_description": "Combines leadership with organization. Enjoys operations management.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    
    # =========================================================================
    # REVERSE PAIRS (for symmetry - some apps may use these)
    # =========================================================================
    {"riasec_code": "IR", "riasec_title": "Investigative-Realistic", 
     "riasec_description": "Combines analytical thinking with hands-on skills. Enjoys engineering and technical research.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "AR", "riasec_title": "Artistic-Realistic", 
     "riasec_description": "Combines creativity with craftsmanship. Enjoys design and fabrication.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "AI", "riasec_title": "Artistic-Investigative", 
     "riasec_description": "Combines creativity with research. Enjoys design research and innovation.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "SR", "riasec_title": "Social-Realistic", 
     "riasec_description": "Combines people skills with practical work. Enjoys healthcare and therapy.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "SI", "riasec_title": "Social-Investigative", 
     "riasec_description": "Combines helping with analysis. Enjoys counseling and social research.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "SA", "riasec_title": "Social-Artistic", 
     "riasec_description": "Combines helping with creativity. Enjoys art therapy and creative teaching.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "ER", "riasec_title": "Enterprising-Realistic", 
     "riasec_description": "Combines leadership with practical skills. Enjoys managing technical operations.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "EI", "riasec_title": "Enterprising-Investigative", 
     "riasec_description": "Combines leadership with analysis. Enjoys strategic consulting.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "EA", "riasec_title": "Enterprising-Artistic", 
     "riasec_description": "Combines leadership with creativity. Enjoys advertising and creative business.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "ES", "riasec_title": "Enterprising-Social", 
     "riasec_description": "Combines leadership with helping. Enjoys managing service organizations.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "CR", "riasec_title": "Conventional-Realistic", 
     "riasec_description": "Combines organization with hands-on work. Enjoys operations and logistics.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "CI", "riasec_title": "Conventional-Investigative", 
     "riasec_description": "Combines organization with analysis. Enjoys data management and research.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "CA", "riasec_title": "Conventional-Artistic", 
     "riasec_description": "Combines organization with creativity. Enjoys production and layout.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "CS", "riasec_title": "Conventional-Social", 
     "riasec_description": "Combines organization with helping. Enjoys administrative support.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
    {"riasec_code": "CE", "riasec_title": "Conventional-Enterprising", 
     "riasec_description": "Combines organization with leadership. Enjoys financial management.", 
     "strengths": [], "challenges": [], "strategies": [], "work_environments": [], "interaction_styles": [], "congruent_code_ids": []},
]


def seed_riasec_codes():
    """
    Seed riasec_codes table with Holland's RIASEC types
    """
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("🚀 Starting RIASEC Codes Seeding...")
        print("=" * 60)
        
        inserted = 0
        skipped = 0
        
        for code_data in RIASEC_CODES_DATA:
            riasec_code = code_data["riasec_code"]
            
            # Check if code already exists
            existing = db.execute(
                select(RIASECCode).where(RIASECCode.riasec_code == riasec_code)
            ).scalar_one_or_none()
            
            if existing:
                print(f"⏭️  SKIPPED: '{riasec_code}' - already exists (ID: {existing.id})")
                skipped += 1
                continue
            
            # Insert new code
            new_code = RIASECCode(
                riasec_code=riasec_code,
                riasec_title=code_data["riasec_title"],
                riasec_description=code_data["riasec_description"],
                strengths=code_data["strengths"],
                challenges=code_data["challenges"],
                strategies=code_data["strategies"],
                work_environments=code_data["work_environments"],
                interaction_styles=code_data["interaction_styles"],
                congruent_code_ids=code_data["congruent_code_ids"]
            )
            db.add(new_code)
            db.flush()
            
            print(f"✅ INSERTED: '{riasec_code}' - {code_data['riasec_title']} (ID: {new_code.id})")
            inserted += 1
        
        db.commit()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 SEEDING SUMMARY")
        print("=" * 60)
        print(f"   ✅ Inserted: {inserted}")
        print(f"   ⏭️  Skipped:  {skipped}")
        print(f"   📦 Total:    {len(RIASEC_CODES_DATA)}")
        print("\n✅ RIASEC Codes seeding completed successfully!\n")
        return True
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ ERROR: {str(e)}")
        raise e
    
    finally:
        db.close()


if __name__ == "__main__":
    seed_riasec_codes()
