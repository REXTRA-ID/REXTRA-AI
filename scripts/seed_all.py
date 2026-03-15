#!/usr/bin/env python3
"""
Master Seeder Script

Runs all database seeders in the correct order.

Usage:
    python -m scripts.seed_all

Order of execution:
    1. kenalidiri_categories (base categories)
    2. riasec_codes (RIASEC personality types)
    3. digital_professions (profession data)
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.seed_kenalidiri_categories import seed_kenalidiri_categories
from scripts.seed_users import seed_users
from scripts.seed_riasec_codes import seed_riasec_codes
from scripts.seed_digital_professions import seed_digital_professions


def seed_all():
    """
    Run all seeders in correct order
    """
    print("\n" + "=" * 70)
    print("🌱 MASTER DATABASE SEEDER")
    print("=" * 70)
    print("\nThis script will seed all required data in the correct order.\n")
    
    seeders = [
        ("Kenali Diri Categories", seed_kenalidiri_categories),
        ("Users", seed_users),
        ("RIASEC Codes", seed_riasec_codes),
        ("Digital Professions", seed_digital_professions),
    ]
    
    results = []
    
    for name, seeder_func in seeders:
        print(f"\n{'─' * 70}")
        print(f"📦 Running: {name}")
        print(f"{'─' * 70}\n")
        
        try:
            seeder_func()
            results.append((name, "✅ SUCCESS"))
        except Exception as e:
            results.append((name, f"❌ FAILED: {str(e)}"))
            print(f"\n⚠️  Seeder '{name}' failed, continuing with next...")
    
    # Final Summary
    print("\n" + "=" * 70)
    print("📊 FINAL SEEDING SUMMARY")
    print("=" * 70)
    
    for name, status in results:
        print(f"   {status}: {name}")
    
    failed = sum(1 for _, s in results if s.startswith("❌"))
    if failed == 0:
        print("\n🎉 All seeders completed successfully!")
    else:
        print(f"\n⚠️  {failed} seeder(s) failed. Check logs above.")
    
    print("")


if __name__ == "__main__":
    seed_all()
