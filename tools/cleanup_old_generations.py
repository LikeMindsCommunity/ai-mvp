#!/usr/bin/env python3
"""
Script to clean up old Flutter code generations.

This script removes directories for completed or failed Flutter code generations
that are older than a specified time threshold.
"""

import os
import shutil
import time
import argparse
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Clean up old Flutter code generations.')
    parser.add_argument(
        '--age-hours',
        type=int,
        default=24,
        help='Age threshold in hours (default: 24)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='output',
        help='Path to the output directory (default: output)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform a dry run without deleting files'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    return parser.parse_args()

def is_directory_old(directory_path, threshold_hours):
    """
    Check if a directory is older than the threshold.
    
    Args:
        directory_path (str): Path to the directory
        threshold_hours (int): Age threshold in hours
        
    Returns:
        bool: True if the directory is older than the threshold, False otherwise
    """
    try:
        # Get the directory's modification time
        mtime = os.path.getmtime(directory_path)
        # Convert to datetime
        mtime_dt = datetime.fromtimestamp(mtime)
        # Calculate the age threshold
        threshold_dt = datetime.now() - timedelta(hours=threshold_hours)
        # Return whether the directory is older than the threshold
        return mtime_dt < threshold_dt
    except Exception as e:
        logger.error(f"Error checking age of {directory_path}: {str(e)}")
        return False

def cleanup_old_generations(output_dir, threshold_hours, dry_run=False, verbose=False):
    """
    Clean up old Flutter code generations.
    
    Args:
        output_dir (str): Path to the output directory
        threshold_hours (int): Age threshold in hours
        dry_run (bool, optional): Whether to perform a dry run. Defaults to False.
        verbose (bool, optional): Whether to enable verbose logging. Defaults to False.
        
    Returns:
        int: Number of directories removed
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        logger.info(f"Output directory {output_dir} does not exist, creating it")
        os.makedirs(output_dir, exist_ok=True)
        return 0
        
    count = 0
    current_time = time.time()
    
    # Loop through all directories in the output directory
    for dirname in os.listdir(output_dir):
        dir_path = os.path.join(output_dir, dirname)
        
        # Skip if not a directory
        if not os.path.isdir(dir_path):
            continue
            
        # Skip directories that look like project IDs or other system directories
        # Note: We now use database IDs which could be integers or other formats
        if dirname.startswith('.') or dirname == 'logs' or dirname == '__pycache__':
            if verbose:
                logger.debug(f"Skipping system directory: {dirname}")
            continue
            
        # Check if the directory is older than the threshold
        if is_directory_old(dir_path, threshold_hours):
            if dry_run:
                logger.info(f"Would remove old generation directory: {dirname}")
            else:
                try:
                    shutil.rmtree(dir_path)
                    logger.info(f"Removed old generation directory: {dirname}")
                    count += 1
                except Exception as e:
                    logger.error(f"Failed to remove directory {dirname}: {str(e)}")
        elif verbose:
            logger.debug(f"Skipping directory that is not old enough: {dirname}")
    
    return count

def main():
    """Main entry point."""
    args = parse_arguments()
    
    # Set log level based on verbose flag
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    logger.info(f"Starting cleanup of Flutter code generations older than {args.age_hours} hours")
    
    if args.dry_run:
        logger.info("Performing dry run, no files will be deleted")
    
    try:
        count = cleanup_old_generations(
            args.output_dir,
            args.age_hours,
            args.dry_run,
            args.verbose
        )
        
        logger.info(f"Cleanup complete. {'Would have removed' if args.dry_run else 'Removed'} {count} generation directories")
    except Exception as e:
        logger.error(f"An error occurred during cleanup: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 