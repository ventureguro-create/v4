#!/usr/bin/env python3
"""
Data Migration Script
Loads all default data into MongoDB
"""

import asyncio
import sys
import os
from datetime import datetime, timezone
from uuid import uuid4

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(MONGO_URL)
db = client.fomo_db

async def migrate_roadmap_tasks():
    """Migrate roadmap tasks"""
    print("📋 Migrating roadmap tasks...")
    
    # Check if tasks already exist
    existing = await db.roadmap_tasks.count_documents({})
    if existing > 0:
        print(f"  ℹ️  Found {existing} existing tasks, skipping...")
        return
    
    default_tasks = [
        {"id": str(uuid4()), "name": "Platform Architecture", "status": "done", "category": "Development", "order": 1},
        {"id": str(uuid4()), "name": "Core Team Formation", "status": "done", "category": "Team", "order": 2},
        {"id": str(uuid4()), "name": "Alpha Version Launch", "status": "done", "category": "Development", "order": 3},
        {"id": str(uuid4()), "name": "Community Building", "status": "done", "category": "Marketing", "order": 4},
        {"id": str(uuid4()), "name": "Beta Version v1.0", "status": "done", "category": "Development", "order": 5},
        {"id": str(uuid4()), "name": "NFT Box 666 Mint", "status": "done", "category": "NFT", "order": 6},
        {"id": str(uuid4()), "name": "Wallet Integration", "status": "done", "category": "Development", "order": 7},
        {"id": str(uuid4()), "name": "Analytics Dashboard", "status": "done", "category": "Development", "order": 8},
        {"id": str(uuid4()), "name": "Beta Version v1.1", "status": "progress", "category": "Development", "order": 9},
        {"id": str(uuid4()), "name": "OTC Marketplace", "status": "progress", "category": "Development", "order": 10},
        {"id": str(uuid4()), "name": "Mobile App Development", "status": "progress", "category": "Development", "order": 11},
        {"id": str(uuid4()), "name": "Partnership Programs", "status": "progress", "category": "Business", "order": 12},
    ]
    
    for task in default_tasks:
        task["created_at"] = datetime.now(timezone.utc).isoformat()
        task["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    await db.roadmap_tasks.insert_many(default_tasks)
    print(f"  ✅ Migrated {len(default_tasks)} roadmap tasks")

async def migrate_team_members():
    """Migrate team members"""
    print("👥 Migrating team members...")
    
    # Check if members already exist
    existing = await db.team_members.count_documents({})
    if existing > 0:
        print(f"  ℹ️  Found {existing} existing team members, skipping...")
        return
    
    default_members = [
        {
            "id": str(uuid4()),
            "name": "Alex Morgan",
            "name_ru": "Алекс Морган",
            "position": "CEO & Founder",
            "position_ru": "CEO и Основатель",
            "bio": "10+ years in blockchain and crypto trading",
            "bio_ru": "10+ лет опыта в блокчейне и крипто-трейдинге",
            "avatar": None,
            "social_links": {
                "twitter": "https://twitter.com/alexmorgan",
                "linkedin": "https://linkedin.com/in/alexmorgan"
            },
            "order": 1,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid4()),
            "name": "Sarah Chen",
            "name_ru": "Сара Чен",
            "position": "CTO",
            "position_ru": "Технический директор",
            "bio": "Former Google engineer, blockchain expert",
            "bio_ru": "Бывший инженер Google, эксперт по блокчейну",
            "avatar": None,
            "social_links": {
                "twitter": "https://twitter.com/sarahchen",
                "linkedin": "https://linkedin.com/in/sarahchen"
            },
            "order": 2,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid4()),
            "name": "Michael Ross",
            "name_ru": "Майкл Росс",
            "position": "Head of Product",
            "position_ru": "Руководитель продукта",
            "bio": "Ex-Binance, product strategy specialist",
            "bio_ru": "Экс-Binance, специалист по продуктовой стратегии",
            "avatar": None,
            "social_links": {
                "twitter": "https://twitter.com/michaelross",
                "linkedin": "https://linkedin.com/in/michaelross"
            },
            "order": 3,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    await db.team_members.insert_many(default_members)
    print(f"  ✅ Migrated {len(default_members)} team members")

async def check_platform_settings():
    """Check if platform settings exist"""
    print("⚙️  Checking platform settings...")
    
    settings = await db.platform_settings.find_one({"id": "platform_settings"})
    if settings:
        modules_count = len(settings.get('service_modules', []))
        print(f"  ℹ️  Platform settings exist with {modules_count} modules")
    else:
        print("  ⚠️  Platform settings not found")

async def main():
    """Run all migrations"""
    print("\n🚀 Starting data migration...\n")
    
    try:
        await migrate_roadmap_tasks()
        await migrate_team_members()
        await check_platform_settings()
        
        print("\n✅ Migration completed successfully!\n")
    except Exception as e:
        print(f"\n❌ Migration failed: {e}\n")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())
