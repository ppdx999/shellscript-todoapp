#!/bin/bash -vx

######################################################################
# Initialize

# Setup the environment
homd="$(
	d=${0%/*}/
	[ "_$d" = "_$0/" ] && d='./'
	cd "$d../.."
	pwd
)"
. $homd/config/common.shlib
timestamp=$(date '+%Y%m%d%H%M%S')
cmdname=$(basename $0)
# Set the umask
umask 022
# Create a name prefix for temporary file
tmp=/tmp/$cmdname.$timestamp.$$

# Define util functions
ERROR_CHECK() {
	[ $(plus ${PIPESTATUS[@]}) -gt 0 ] && ERROR_EXIT "$@"
}

ERROR_EXIT() {
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
exec 2>$logd/LOG.$cmdname.$timestamp.$$

######################################################################
# Handle POST data
if [ ! -z "$CONTENT_LENGTH" -a "$CONTENT_LENGTH" -gt 0 ]; then
	dd bs=${CONTENT_LENGTH:-0} count=1 2>/dev/null |
		cgi-name >$tmp-name
	ERROR_CHECK
else
	false
	ERROR_CHECK
fi

cat <<FIN >$tmp-check
title x30
expiredat n14
FIN
ERROR_CHECK

check_attr_name $tmp-check $tmp-name >$tmp-result
if [ -s $tmp-result ]; then
	cat <<-__HTTP_HEADER
		Status: 400 Bad Request
		Content-Type: text/plain

		400 Bad Request
	__HTTP_HEADER
	cat $tmp-result

	exit 1
fi
title=$(cat $tmp-name | nameread title)
[ -z "$title" ] && ERROR_EXIT "title is empty"
expiredat=$(cat $tmp-name | nameread expiredat)
[ -z "$expiredat" ] && expiredat=0

######################################################################
# Save

# If the data to be appended is under 4096 bytes, it is atomic.
# 1: id, 2: title, 3: is_completed, 4: createdat, 5: expiredat
printf "$timestamp.$$ $title 0 $timestamp $expiredat\n" >>$datad/tasks
ERROR_CHECK "Failed to save task"

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
