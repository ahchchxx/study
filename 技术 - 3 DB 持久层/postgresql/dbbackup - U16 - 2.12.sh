#!/bin/bash
dblist=`psql -U odoo -c '\l' |grep UTF | grep -v postgres | grep -v hrone | awk '{print $1}'`
for i in $dblist
do

DB_NAME=$i

BACKUP_DIR=/mnt/db_backup

#prepare directory
FINIAL_BACKUP_DIR=$BACKUP_DIR"/"$DB_NAME

mkdir -p $FINIAL_BACKUP_DIR
          
#find $FINIAL_BACKUP_DIR -name "$i*" -type f -mtime +10 -exec rm {} \;
find $FINIAL_BACKUP_DIR -name "$i*" -type f -mtime +10 -delete;

DB_FILENAME="$i-`date +\%Y\%m\%d-\%H%M%S`.dump"
        
pg_dump -Fc -U odoo -d $DB_NAME>$FINIAL_BACKUP_DIR"/"$DB_FILENAME
             
DBSIZE=`du $FINIAL_BACKUP_DIR"/"$DB_FILENAME | awk -F " " '{print $1}'`

if [[ $DBSIZE -le 100 ]]
then 
 echo "db backup error" # | mail -s backuperror min.zhou
 echo "sizi error" 
else
echo "pg_dump finished"
fi  
done