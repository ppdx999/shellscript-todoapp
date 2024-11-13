#!/bin/bash -vx

######################################################################
# Initialize

# Setup the environment
homd="$(d=${0%/*}/; [ "_$d" = "_$0/" ] && d='./'; cd "$d../.."; pwd)"
. $homd/config/common.shlib
timestamp=$(date '+%Y%m%d%H%M%S')
cmdname=$(basename $0)
# Set the umask
umask 022
# Create a name prefix for temporary file
tmp=/tmp/$cmdname.$timestamp.$$

# Define util functions
ERROR_CHECK () {
	[ $(plus ${PIPESTATUS[@]}) -gt 0 ] && ERROR_EXIT "$@"
}

ERROR_EXIT () {
	cat <<-__HTTP_HEADER
		Status: 500 Internal Server Error
		Content-Type: text/plain

		500 Internal Server Error
__HTTP_HEADER
	echo "$@"
	[ -n "$tmp" ] && rm -f $tmp*
	exit 1
}

# output exec error log
exec 2> $logd/LOG.$cmdname.$timestamp.$$

######################################################################
# Handle POST data
if [ ! -z "$CONTENT_LENGTH" -a "$CONTENT_LENGTH" -gt 0 ]; then
	dd bs=${CONTENT_LENGTH:-0} count=1 2>/dev/null |
	cgi-name > $tmp-name
	ERROR_CHECK
else
	false
	ERROR_CHECK
fi

id=$(cat $tmp-name | nameread task-id)
[ -z "$id" ] && ERROR_EXIT "id is empty"


######################################################################
# Delete Task

# Craete lock dir
mkdir $datad/.tasks
ERROR_CHECK

cat $datad/tasks | grep -v "^$id" > $tmp-tasks
ERROR_CHECK

mv $tmp-tasks $datad/tasks
ERROR_CHECK

# Remove lock dir
rmdir $datad/.tasks

######################################################################
# Response Task List
echo "Status: 200 OK"
echo "Content-Type: text/html"
echo ""

cat $tpld/tasks.html |
mojihame -l___TASK_ITEMS___ - $datad/tasks


######################################################################
# Finalize
rm -f $tmp*
exit 0

