#!/bin/bash

prettier --write 'todoapp/**/*.{js,jsx,ts,tsx,html,css}'

find todoapp -type f -exec grep -l '^#![[:blank:]]*/bin/\(bash\|sh\)' {} \; | xargs shfmt -l -w
