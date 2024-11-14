#!/bin/bash -vx

######################################################################
# Initialize

# Setup the environment
homd="$(
	d=${0%/*}/
	[ "_$d" = "_$0/" ] && d='./'
	cd "$d.."
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
# Response Main Page
echo "Status: 200 OK"
echo "Content-Type: text/html"
echo ""

# Create Task List
cat $tpld/tasks.html |
	mojihame -l___TASK_ITEMS___ - $datad/tasks >$tmp-tasks
ERROR_CHECK

# Output Main Page
cat $tpld/main.html |
	filehame -l___TASK_CREATE_FORM___ - $tpld/task-create-form.html |
	filehame -l___TASKS___ - $tmp-tasks

######################################################################
# Finalize
rm -f $tmp*
exit 0
