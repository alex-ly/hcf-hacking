#!/bin/bash
docker exec -it grading /bin/bash -c "export COLUMNS=`tput cols`; export LINES=`tput lines`; exec bash"
