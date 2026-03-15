#!/usr/bin/env python3
"""
Digital Professions Seeder Script

Seeds the digital_professions table with sample data for testing
the career recommendation feature.

Usage:
    python -m scripts.seed_digital_professions

Naming Convention (PRD):
    [Specialization] + [Platform/Domain] + [Core Role]
    Example: "Web Frontend Developer", "Cloud Infrastructure Engineer"
"""
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.api.v1.categories.career_profile.models.riasec import RIASECCode
from app.api.v1.categories.career_profile.models.digital_profession import DigitalProfession


# =============================================================================
# PROFESSION DATA
# =============================================================================
# Format: (riasec_code, title, description, meta_data)

PROFESSIONS_DATA = [
    # Investigative (I) - Research & Analysis oriented
    {
        "riasec_code": "I",
        "title": "Data Analytics Engineer",
        "description": "Analyzes complex datasets to extract insights and build data pipelines for business intelligence",
        "meta_data": {
            "tech_stack": ["Python", "SQL", "Pandas", "NumPy", "Jupyter"],
            "frameworks": ["Apache Spark", "Airflow", "dbt"],
            "seniority_level": ["Junior", "Mid-Level", "Senior"],
            "work_mode": ["Remote", "Hybrid"],
            "industry_focus": ["FinTech", "E-Commerce", "HealthTech"]
        }
    },
    {
        "riasec_code": "I",
        "title": "Machine Learning Engineer",
        "description": "Develops and deploys machine learning models for production systems",
        "meta_data": {
            "tech_stack": ["Python", "TensorFlow", "PyTorch", "Scikit-learn"],
            "frameworks": ["MLflow", "Kubeflow", "Ray"],
            "seniority_level": ["Mid-Level", "Senior", "Lead"],
            "work_mode": ["Remote", "Hybrid", "Onsite"],
            "industry_focus": ["AI/ML", "FinTech", "HealthTech"]
        }
    },
    {
        "riasec_code": "IR",
        "title": "Backend Systems Architect",
        "description": "Designs scalable backend architectures and distributed systems",
        "meta_data": {
            "tech_stack": ["Go", "Python", "Rust", "PostgreSQL", "Redis"],
            "frameworks": ["Kubernetes", "gRPC", "Kafka"],
            "seniority_level": ["Senior", "Lead", "Principal"],
            "work_mode": ["Remote", "Hybrid"],
            "industry_focus": ["Enterprise", "FinTech", "SaaS"]
        }
    },
    
    # Realistic (R) - Hands-on technical work
    {
        "riasec_code": "R",
        "title": "Cloud Infrastructure Engineer",
        "description": "Manages and optimizes cloud infrastructure using Infrastructure as Code",
        "meta_data": {
            "tech_stack": ["AWS", "GCP", "Terraform", "Docker", "Kubernetes"],
            "frameworks": ["Ansible", "Pulumi", "CloudFormation"],
            "seniority_level": ["Junior", "Mid-Level", "Senior"],
            "work_mode": ["Remote", "Hybrid"],
            "industry_focus": ["Cloud Services", "Enterprise", "Startup"]
        }
    },
    {
        "riasec_code": "R",
        "title": "Mobile Android Developer",
        "description": "Develops native Android applications using modern Kotlin and Jetpack",
        "meta_data": {
            "tech_stack": ["Kotlin", "Java", "SQLite", "Firebase"],
            "frameworks": ["Jetpack Compose", "Coroutines", "Hilt"],
            "seniority_level": ["Junior", "Mid-Level", "Senior"],
            "work_mode": ["Remote", "Hybrid", "Onsite"],
            "industry_focus": ["Mobile Apps", "FinTech", "E-Commerce"]
        }
    },
    {
        "riasec_code": "RI",
        "title": "Web Backend Developer",
        "description": "Builds robust backend APIs and services for web applications",
        "meta_data": {
            "tech_stack": ["Go", "Python", "Node.js", "PostgreSQL", "MongoDB"],
            "frameworks": ["Gin", "FastAPI", "Express", "NestJS"],
            "seniority_level": ["Junior", "Mid-Level", "Senior"],
            "work_mode": ["Remote", "Hybrid"],
            "industry_focus": ["SaaS", "E-Commerce", "FinTech"]
        }
    },
    {
        "riasec_code": "RC",
        "title": "DevOps Platform Engineer",
        "description": "Builds and maintains CI/CD pipelines and developer platforms",
        "meta_data": {
            "tech_stack": ["Linux", "Docker", "Kubernetes", "GitHub Actions", "Jenkins"],
            "frameworks": ["ArgoCD", "Backstage", "Crossplane"],
            "seniority_level": ["Mid-Level", "Senior", "Lead"],
            "work_mode": ["Remote", "Hybrid"],
            "industry_focus": ["Enterprise", "Cloud Services", "FinTech"]
        }
    },
    
    # Artistic (A) - Creative & Design focused
    {
        "riasec_code": "A",
        "title": "Product UI/UX Designer",
        "description": "Creates user-centered designs and interactive prototypes for digital products",
        "meta_data": {
            "tech_stack": ["Figma", "Adobe XD", "Sketch", "Framer"],
            "frameworks": ["Design Systems", "Atomic Design", "Material Design"],
            "seniority_level": ["Junior", "Mid-Level", "Senior"],
            "work_mode": ["Remote", "Hybrid", "Onsite"],
            "industry_focus": ["Product Design", "SaaS", "Agency"]
        }
    },
    {
        "riasec_code": "AR",
        "title": "Creative Frontend Developer",
        "description": "Builds visually stunning and interactive web experiences",
        "meta_data": {
            "tech_stack": ["JavaScript", "TypeScript", "Three.js", "GSAP", "CSS"],
            "frameworks": ["React", "Next.js", "Framer Motion", "WebGL"],
            "seniority_level": ["Junior", "Mid-Level", "Senior"],
            "work_mode": ["Remote", "Hybrid"],
            "industry_focus": ["Agency", "Gaming", "Entertainment"]
        }
    },
    {
        "riasec_code": "AI",
        "title": "Digital Motion Designer",
        "description": "Creates motion graphics and animations for digital platforms",
        "meta_data": {
            "tech_stack": ["After Effects", "Premiere Pro", "Lottie", "Rive"],
            "frameworks": ["Animation Principles", "Motion Design Systems"],
            "seniority_level": ["Junior", "Mid-Level", "Senior"],
            "work_mode": ["Remote", "Hybrid"],
            "industry_focus": ["Agency", "Entertainment", "Marketing"]
        }
    },
    
    # Social (S) - People & Communication focused
    {
        "riasec_code": "S",
        "title": "Technical Developer Advocate",
        "description": "Bridges the gap between developers and products through education and community building",
        "meta_data": {
            "tech_stack": ["Public Speaking", "Technical Writing", "Video Production"],
            "frameworks": ["Developer Relations", "Community Building", "Content Strategy"],
            "seniority_level": ["Mid-Level", "Senior", "Lead"],
            "work_mode": ["Remote", "Hybrid"],
            "industry_focus": ["Developer Tools", "Cloud Services", "Open Source"]
        }
    },
    {
        "riasec_code": "SE",
        "title": "Technical Project Manager",
        "description": "Leads technical projects and coordinates cross-functional teams",
        "meta_data": {
            "tech_stack": ["Jira", "Confluence", "Linear", "Notion"],
            "frameworks": ["Agile", "Scrum", "Kanban", "SAFe"],
            "seniority_level": ["Mid-Level", "Senior", "Lead"],
            "work_mode": ["Remote", "Hybrid", "Onsite"],
            "industry_focus": ["Enterprise", "Startup", "Consulting"]
        }
    },
    {
        "riasec_code": "SA",
        "title": "EdTech Learning Designer",
        "description": "Designs educational technology products and learning experiences",
        "meta_data": {
            "tech_stack": ["LMS Platforms", "Articulate", "Instructional Design"],
            "frameworks": ["ADDIE", "SAM", "Gamification"],
            "seniority_level": ["Junior", "Mid-Level", "Senior"],
            "work_mode": ["Remote", "Hybrid"],
            "industry_focus": ["EdTech", "Corporate Training", "Higher Education"]
        }
    },
    
    # Enterprising (E) - Leadership & Business focused
    {
        "riasec_code": "E",
        "title": "Digital Product Manager",
        "description": "Defines product strategy and roadmap for digital products",
        "meta_data": {
            "tech_stack": ["Product Analytics", "A/B Testing", "User Research"],
            "frameworks": ["Lean Startup", "Jobs-to-be-Done", "OKRs"],
            "seniority_level": ["Mid-Level", "Senior", "Lead"],
            "work_mode": ["Remote", "Hybrid", "Onsite"],
            "industry_focus": ["SaaS", "FinTech", "E-Commerce"]
        }
    },
    {
        "riasec_code": "ES",
        "title": "Tech Startup Founder",
        "description": "Leads technology startups from ideation to scale",
        "meta_data": {
            "tech_stack": ["Business Strategy", "Fundraising", "Product Vision"],
            "frameworks": ["Lean Canvas", "Customer Development", "Growth Hacking"],
            "seniority_level": ["Lead", "Executive"],
            "work_mode": ["Hybrid", "Onsite"],
            "industry_focus": ["Startup", "Venture Capital", "Innovation"]
        }
    },
    {
        "riasec_code": "EC",
        "title": "Technology Sales Engineer",
        "description": "Provides technical expertise to support enterprise sales processes",
        "meta_data": {
            "tech_stack": ["Demo Skills", "Solution Architecture", "CRM"],
            "frameworks": ["MEDDIC", "Solution Selling", "Value Engineering"],
            "seniority_level": ["Mid-Level", "Senior", "Lead"],
            "work_mode": ["Remote", "Hybrid"],
            "industry_focus": ["Enterprise Software", "Cloud Services", "SaaS"]
        }
    },
    
    # Conventional (C) - Detail & Process oriented
    {
        "riasec_code": "C",
        "title": "Software QA Engineer",
        "description": "Ensures software quality through comprehensive testing strategies",
        "meta_data": {
            "tech_stack": ["Selenium", "Cypress", "PyTest", "Postman"],
            "frameworks": ["Test-Driven Development", "BDD", "CI/CD Testing"],
            "seniority_level": ["Junior", "Mid-Level", "Senior"],
            "work_mode": ["Remote", "Hybrid"],
            "industry_focus": ["Enterprise", "FinTech", "HealthTech"]
        }
    },
    {
        "riasec_code": "CI",
        "title": "Database Reliability Engineer",
        "description": "Maintains database performance, availability, and disaster recovery",
        "meta_data": {
            "tech_stack": ["PostgreSQL", "MySQL", "Oracle", "MongoDB", "Redis"],
            "frameworks": ["High Availability", "Replication", "Backup Strategies"],
            "seniority_level": ["Mid-Level", "Senior", "Lead"],
            "work_mode": ["Remote", "Hybrid"],
            "industry_focus": ["Enterprise", "FinTech", "Cloud Services"]
        }
    },
    {
        "riasec_code": "CR",
        "title": "Security Operations Analyst",
        "description": "Monitors and responds to security threats and incidents",
        "meta_data": {
            "tech_stack": ["SIEM", "Splunk", "Security Tools", "Python"],
            "frameworks": ["NIST", "ISO 27001", "Incident Response"],
            "seniority_level": ["Junior", "Mid-Level", "Senior"],
            "work_mode": ["Remote", "Hybrid", "Onsite"],
            "industry_focus": ["Cybersecurity", "FinTech", "Enterprise"]
        }
    },
    {
        "riasec_code": "CE",
        "title": "Technical Documentation Engineer",
        "description": "Creates and maintains technical documentation for software products",
        "meta_data": {
            "tech_stack": ["Markdown", "Docs as Code", "API Documentation"],
            "frameworks": ["Diátaxis", "Information Architecture", "Style Guides"],
            "seniority_level": ["Junior", "Mid-Level", "Senior"],
            "work_mode": ["Remote", "Hybrid"],
            "industry_focus": ["Developer Tools", "Enterprise", "Open Source"]
        }
    },
]


def get_riasec_code_map(db: Session) -> dict:
    """
    Fetch RIASEC codes from database and return as {code: id} mapping
    """
    result = db.execute(select(RIASECCode.id, RIASECCode.riasec_code))
    code_map = {row.riasec_code: row.id for row in result}
    return code_map


def seed_digital_professions():
    """
    Seed digital_professions table with sample data
    """
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("🚀 Starting Digital Professions Seeding...")
        print("=" * 60)
        
        # Step 1: Get RIASEC code mapping
        riasec_map = get_riasec_code_map(db)
        
        if not riasec_map:
            print("❌ ERROR: No RIASEC codes found in database!")
            print("   Please run riasec_codes seeder first.")
            return False
        
        print(f"\n📋 Found {len(riasec_map)} RIASEC codes:")
        for code, id_ in riasec_map.items():
            print(f"   - {code}: ID {id_}")
        
        # Step 2: Seed professions
        inserted = 0
        skipped = 0
        missing_codes = []
        
        print(f"\n📦 Processing {len(PROFESSIONS_DATA)} professions...")
        print("-" * 60)
        
        for prof_data in PROFESSIONS_DATA:
            riasec_code = prof_data["riasec_code"]
            title = prof_data["title"]
            
            # Check if RIASEC code exists
            if riasec_code not in riasec_map:
                missing_codes.append((title, riasec_code))
                print(f"⚠️  SKIPPED: '{title}' - RIASEC code '{riasec_code}' not found")
                skipped += 1
                continue
            
            riasec_code_id = riasec_map[riasec_code]
            
            # Check if profession already exists
            existing = db.execute(
                select(DigitalProfession).where(DigitalProfession.title == title)
            ).scalar_one_or_none()
            
            if existing:
                print(f"⏭️  SKIPPED: '{title}' - already exists (ID: {existing.id})")
                skipped += 1
                continue
            
            # Insert new profession
            new_profession = DigitalProfession(
                title=title,
                description=prof_data["description"],
                riasec_code_id=riasec_code_id,
                meta_data=prof_data["meta_data"]
            )
            db.add(new_profession)
            db.flush()  # Get the ID
            
            print(f"✅ INSERTED: '{title}' (ID: {new_profession.id}, RIASEC: {riasec_code})")
            inserted += 1
        
        db.commit()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 SEEDING SUMMARY")
        print("=" * 60)
        print(f"   ✅ Inserted: {inserted}")
        print(f"   ⏭️  Skipped:  {skipped}")
        print(f"   📦 Total:    {len(PROFESSIONS_DATA)}")
        
        if missing_codes:
            print(f"\n⚠️  Warning: The following RIASEC codes need to be added:")
            for title, code in missing_codes:
                print(f"   - '{code}' (required by: {title})")
        
        print("\n✅ Digital Professions seeding completed successfully!\n")
        return True
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ ERROR: {str(e)}")
        raise e
    
    finally:
        db.close()


if __name__ == "__main__":
    seed_digital_professions()
