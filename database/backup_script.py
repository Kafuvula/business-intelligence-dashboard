#!/usr/bin/env python3
"""
Database Backup Script for Business Intelligence Dashboard
Automated backup of MySQL database with compression and rotation
"""

import os
import sys
import subprocess
import datetime
import shutil
import gzip
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BACKUP_DIR = Path("backups")
LOG_FILE = "backup.log"
KEEP_DAYS = 30  # Keep backups for 30 days

# Database configuration from environment
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "business_dashboard")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def create_backup_dir():
    """Create backup directory if it doesn't exist"""
    try:
        BACKUP_DIR.mkdir(exist_ok=True)
        logger.info(f"Backup directory: {BACKUP_DIR.absolute()}")
    except Exception as e:
        logger.error(f"Failed to create backup directory: {e}")
        raise

def backup_database():
    """Create a backup of the database"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"{DB_NAME}_backup_{timestamp}.sql"
    compressed_file = BACKUP_DIR / f"{DB_NAME}_backup_{timestamp}.sql.gz"
    
    # Build mysqldump command
    cmd = [
        "mysqldump",
        f"--host={DB_HOST}",
        f"--user={DB_USER}",
        f"--password={DB_PASSWORD}",
        "--single-transaction",
        "--routines",
        "--triggers",
        "--events",
        DB_NAME
    ]
    
    try:
        logger.info(f"Starting backup of database: {DB_NAME}")
        
        # Execute mysqldump
        with open(backup_file, 'w') as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            logger.error(f"mysqldump failed: {result.stderr}")
            return False
        
        logger.info(f"Database backup created: {backup_file}")
        
        # Compress the backup file
        with open(backup_file, 'rb') as f_in:
            with gzip.open(compressed_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # Remove uncompressed file
        backup_file.unlink()
        
        file_size = compressed_file.stat().st_size / (1024 * 1024)  # Size in MB
        logger.info(f"Backup compressed: {compressed_file} ({file_size:.2f} MB)")
        
        return str(compressed_file)
        
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        # Clean up failed backup files
        if backup_file.exists():
            backup_file.unlink()
        if compressed_file.exists():
            compressed_file.unlink()
        return False

def rotate_backups():
    """Remove backups older than KEEP_DAYS days"""
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=KEEP_DAYS)
    deleted_count = 0
    
    try:
        for backup_file in BACKUP_DIR.glob("*.sql.gz"):
            # Extract timestamp from filename
            try:
                # Format: business_dashboard_backup_YYYYMMDD_HHMMSS.sql.gz
                parts = backup_file.stem.replace('.sql', '').split('_')
                date_str = parts[-2]  # YYYYMMDD
                time_str = parts[-1]  # HHMMSS
                
                file_date = datetime.datetime.strptime(
                    f"{date_str}_{time_str}", "%Y%m%d_%H%M%S"
                )
                
                if file_date < cutoff_date:
                    backup_file.unlink()
                    deleted_count += 1
                    logger.info(f"Deleted old backup: {backup_file.name}")
                    
            except (ValueError, IndexError) as e:
                logger.warning(f"Could not parse date from {backup_file.name}: {e}")
                continue
        
        logger.info(f"Deleted {deleted_count} old backup(s)")
        
    except Exception as e:
        logger.error(f"Backup rotation failed: {e}")

def backup_specific_tables(tables=None):
    """Backup specific tables only"""
    if tables is None:
        tables = ["sales", "customers", "products"]
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"{DB_NAME}_tables_{timestamp}.sql.gz"
    
    cmd = [
        "mysqldump",
        f"--host={DB_HOST}",
        f"--user={DB_USER}",
        f"--password={DB_PASSWORD}",
        "--single-transaction",
        DB_NAME
    ] + tables
    
    try:
        logger.info(f"Backing up tables: {', '.join(tables)}")
        
        # Execute and compress in one step
        with gzip.open(backup_file, 'wb') as f_out:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if result.returncode != 0:
                logger.error(f"Table backup failed: {result.stderr.decode()}")
                return False
            
            f_out.write(result.stdout)
        
        file_size = backup_file.stat().st_size / (1024 * 1024)
        logger.info(f"Tables backup created: {backup_file} ({file_size:.2f} MB)")
        
        return str(backup_file)
        
    except Exception as e:
        logger.error(f"Table backup failed: {e}")
        if backup_file.exists():
            backup_file.unlink()
        return False

def backup_schema_only():
    """Backup only database schema (no data)"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"{DB_NAME}_schema_{timestamp}.sql.gz"
    
    cmd = [
        "mysqldump",
        f"--host={DB_HOST}",
        f"--user={DB_USER}",
        f"--password={DB_PASSWORD}",
        "--no-data",
        DB_NAME
    ]
    
    try:
        logger.info("Backing up database schema only")
        
        with gzip.open(backup_file, 'wb') as f_out:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if result.returncode != 0:
                logger.error(f"Schema backup failed: {result.stderr.decode()}")
                return False
            
            f_out.write(result.stdout)
        
        file_size = backup_file.stat().st_size / 1024  # Size in KB
        logger.info(f"Schema backup created: {backup_file} ({file_size:.2f} KB)")
        
        return str(backup_file)
        
    except Exception as e:
        logger.error(f"Schema backup failed: {e}")
        if backup_file.exists():
            backup_file.unlink()
        return False

def list_backups():
    """List all available backups"""
    try:
        backups = list(BACKUP_DIR.glob("*.sql.gz"))
        
        if not backups:
            logger.info("No backups found")
            return []
        
        logger.info(f"Found {len(backups)} backup(s):")
        
        backup_list = []
        for backup in sorted(backups, key=lambda x: x.stat().st_mtime, reverse=True):
            size_mb = backup.stat().st_size / (1024 * 1024)
            modified = datetime.datetime.fromtimestamp(backup.stat().st_mtime)
            age_days = (datetime.datetime.now() - modified).days
            
            backup_info = {
                'filename': backup.name,
                'size_mb': round(size_mb, 2),
                'modified': modified.strftime("%Y-%m-%d %H:%M:%S"),
                'age_days': age_days,
                'path': str(backup)
            }
            
            backup_list.append(backup_info)
            logger.info(
                f"  {backup.name} - {size_mb:.2f} MB - {age_days} days old"
            )
        
        return backup_list
        
    except Exception as e:
        logger.error(f"Failed to list backups: {e}")
        return []

def restore_backup(backup_file, drop_existing=False):
    """Restore database from backup file"""
    if not Path(backup_file).exists():
        logger.error(f"Backup file not found: {backup_file}")
        return False
    
    # Check if file is compressed
    is_compressed = backup_file.endswith('.gz')
    
    # Build mysql command
    mysql_cmd = [
        "mysql",
        f"--host={DB_HOST}",
        f"--user={DB_USER}",
        f"--password={DB_PASSWORD}"
    ]
    
    try:
        logger.info(f"Starting restore from: {backup_file}")
        
        if drop_existing:
            # Drop and recreate database
            drop_cmd = mysql_cmd + ["-e", f"DROP DATABASE IF EXISTS {DB_NAME}; CREATE DATABASE {DB_NAME};"]
            subprocess.run(drop_cmd, check=True)
            logger.info(f"Dropped and recreated database: {DB_NAME}")
        
        # Restore backup
        if is_compressed:
            # For compressed backups
            gunzip_cmd = ["gunzip", "-c", backup_file]
            gunzip_proc = subprocess.Popen(gunzip_cmd, stdout=subprocess.PIPE)
            restore_proc = subprocess.Popen(
                mysql_cmd + [DB_NAME],
                stdin=gunzip_proc.stdout,
                stderr=subprocess.PIPE,
                text=True
            )
            gunzip_proc.stdout.close()
            stdout, stderr = restore_proc.communicate()
        else:
            # For uncompressed backups
            with open(backup_file, 'r') as f:
                restore_proc = subprocess.Popen(
                    mysql_cmd + [DB_NAME],
                    stdin=f,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = restore_proc.communicate()
        
        if restore_proc.returncode != 0:
            logger.error(f"Restore failed: {stderr}")
            return False
        
        logger.info("Database restored successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Restore failed: {e}")
        return False

def send_backup_notification(success=True, backup_file=None, error=None):
    """Send backup notification (placeholder for email/SMS integration)"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if success:
        message = f"✅ Backup successful at {timestamp}\n"
        if backup_file:
            size_mb = Path(backup_file).stat().st_size / (1024 * 1024)
            message += f"File: {Path(backup_file).name}\n"
            message += f"Size: {size_mb:.2f} MB"
    else:
        message = f"❌ Backup failed at {timestamp}\n"
        if error:
            message += f"Error: {error}"
    
    logger.info(f"Backup notification: {message}")
    
    # Placeholder for actual notification (email, SMS, etc.)
    # In production, integrate with email service or notification system
    
    return message

def main():
    """Main backup routine"""
    logger.info("=" * 50)
    logger.info("Starting database backup process")
    logger.info(f"Database: {DB_NAME}")
    logger.info(f"Backup directory: {BACKUP_DIR}")
    logger.info("=" * 50)
    
    try:
        # Create backup directory
        create_backup_dir()
        
        # Create full backup
        backup_file = backup_database()
        
        if backup_file:
            # Rotate old backups
            rotate_backups()
            
            # List available backups
            list_backups()
            
            # Send success notification
            send_backup_notification(success=True, backup_file=backup_file)
            
            logger.info("Backup process completed successfully!")
            return True
        else:
            error_msg = "Backup creation failed"
            send_backup_notification(success=False, error=error_msg)
            logger.error(error_msg)
            return False
            
    except Exception as e:
        error_msg = f"Backup process failed: {e}"
        send_backup_notification(success=False, error=error_msg)
        logger.error(error_msg)
        return False

if __name__ == "__main__":
    # Check if mysqldump is available
    try:
        subprocess.run(["mysqldump", "--version"], check=True, capture_output=True)
    except FileNotFoundError:
        logger.error("mysqldump not found. Please install MySQL client tools.")
        sys.exit(1)
    
    # Run main backup
    success = main()
    sys.exit(0 if success else 1)