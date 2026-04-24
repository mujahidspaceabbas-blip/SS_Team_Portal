#!/usr/bin/env python3
"""
Reset Database - Delete old ss_portal.db
Run this before starting the app
"""

import os
import sqlite3

DB_PATH = "ss_portal.db"

# Delete old database
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print(f"✓ Deleted old database: {DB_PATH}")
else:
    print(f"ℹ Database doesn't exist: {DB_PATH}")

# Verify deletion
if not os.path.exists(DB_PATH):
    print("✓ Database reset complete. Run app now!")
else:
    print("❌ Failed to delete database")