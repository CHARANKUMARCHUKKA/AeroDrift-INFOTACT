#!/bin/bash
# AeroDrift Database Backup Script
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
cp aerodrift.db backups/aerodrift_$TIMESTAMP.db
echo "Backup successful: aerodrift_$TIMESTAMP.db"
