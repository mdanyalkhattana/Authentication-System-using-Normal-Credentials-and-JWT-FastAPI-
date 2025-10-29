"""Safe migration script to add missing columns to email_verification table.

Run from project root in the same Python environment as the app (activate venv first).
This script will:
 - add `email` column if missing
 - modify `verification_code` length to 64
 - add `is_used` column if missing
 - add `expires_at` column if missing

It uses SQL `IF NOT EXISTS` where supported (MySQL 8+). For older MySQL, errors are caught and printed.
"""
import os
import sys

# Ensure project root is on sys.path so imports like `database` resolve when running this script directly
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

from database import engine
from sqlalchemy import text

statements = [
    # Ensure all columns exist with correct types
    "ALTER TABLE email_verification ADD COLUMN IF NOT EXISTS email VARCHAR(255) NOT NULL AFTER user_id;",
    "ALTER TABLE email_verification MODIFY COLUMN verification_code VARCHAR(64) NOT NULL;",
    "ALTER TABLE email_verification ADD COLUMN IF NOT EXISTS is_used TINYINT(1) NOT NULL DEFAULT 0 AFTER verification_code;",
    "ALTER TABLE email_verification ADD COLUMN IF NOT EXISTS expires_at DATETIME NULL AFTER is_used;",
        "ALTER TABLE email_verification ADD COLUMN IF NOT EXISTS is_used TINYINT(1) NOT NULL DEFAULT 0 AFTER verification_code;",
        "ALTER TABLE email_verification ADD COLUMN IF NOT EXISTS expires_at DATETIME NULL AFTER is_used;",
        # Add created_at with CURRENT_TIMESTAMP default so model/server_default works
        "ALTER TABLE email_verification ADD COLUMN IF NOT EXISTS created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP AFTER expires_at;",
    
    # Ensure correct types for existing columns
    "ALTER TABLE email_verification MODIFY COLUMN id BIGINT AUTO_INCREMENT;",
    "ALTER TABLE email_verification MODIFY COLUMN user_id BIGINT NOT NULL;",
    "ALTER TABLE email_verification MODIFY COLUMN is_used TINYINT(1) NOT NULL DEFAULT 0;",
    "ALTER TABLE email_verification MODIFY COLUMN expires_at DATETIME NULL;"
]

print("Starting migration for email_verification table...")
with engine.begin() as conn:
    for stmt in statements:
        try:
            print("Executing:", stmt)
            conn.execute(text(stmt))
            print("OK")
        except Exception as e:
            # Print and continue (many errors are safe if column already exists or server version lacks IF NOT EXISTS)
            print("Warning executing statement:", stmt)
            print(type(e).__name__, e)

print("Migration finished. Verify the table schema in your database.")
