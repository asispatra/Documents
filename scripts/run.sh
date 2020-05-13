#!/bin/bash

#
# File Name: run.sh
#
# Date: April 14, 2020
# Author: Asis Kumar Patra
# Purpose:
#
#

# Write your shell script here.

source helper.sh

MODE=1 # 0: RUN, 1: TEST, 2: DATA COLLECT
SLEEP=5
#JUST_RAN=0 # 1: TRUE, 0: FALSE

iterations=1
LOGDIR="logs"
mkdir -p "${LOGDIR}"

iterations=$(expr ${iterations} - 1)
# Here `s` in `<VAR>s` stand for plural
# ++++++++----------++++++++++----------#
                                        ########################################
vars=(
***+SMT="8 4 1"
-r="30"
-t="1 2 4 8 16 24"
-m="1 2 4 8 16 24"
"=$(seq 0 ${iterations})" # This should be the second last list for number of iterations
#"***+cat /proc/schedstat \>\> \${LOG_FILENAME}.schedstat.before" # This should be some command you want to run before or after run
#"***-cat /proc/schedstat \>\> \${LOG_FILENAME}.schedstat.after" # This should be some command you want to run before or after run
### DUMMY POSITION for COMMAND - for understanding
)

ext=$(date +%d%b%Y_%H%M%S) # Add timestamp extension to file name to identify uniqly

# Spefify your workload command
PROGRAM="${PWD}/schbench"

function startRun() {
(
  if [ ${#vars[@]} -gt $2 ] ; then
    elm="${vars[$2]}"
    if echo "${elm}" | grep "^\*\*\*" > /dev/null  ; then
      option=$(echo ${elm} | cut -d'=' -f 1)
      values=$(echo ${elm} | cut -d'=' -f 2)
      OPTION=$(echo ${option} | sed 's/^\*\*\*[+-][+-]*//')
      if [ "${values}" == "${option}" ] ; then
        if echo "${option}" | grep -e "^...+" -e "^...-+" > /dev/null ; then
          EXEC "$(eval "echo ${OPTION}")"
          #EXEC "${OPTION}"
        fi
        startRun "${1}" $(expr $2 + 1) "${3}" "${4}"
        JUST_RAN=$?
        if echo "${option}" | grep -e "^...-" -e "^...+-" > /dev/null ; then
          EXEC "$(eval "echo ${OPTION}")"
          #EXEC "${OPTION}"
        fi
        if [ ${JUST_RAN} -eq 1 ] ; then
          sleep ${SLEEP}
          head -c 80 /dev/zero | tr '\0' '=' ; echo
        fi
      else
        for value in ${values} ; do
          if echo "${option}" | grep -e "^...+" -e "^...-+" > /dev/null ; then
            EXEC "$(eval "echo ${OPTION} ${value}")"
            #EXEC "${OPTION} ${value}"
          fi
          startRun "${1}" $(expr $2 + 1) "${3}" "${OPTION}-${value}_${4}"
        JUST_RAN=$?
          if echo "${option}" | grep -e "^...-" -e "^...+-" > /dev/null ; then
            EXEC "$(eval "echo ${OPTION} ${value}")"
            #EXEC "${OPTION} ${value}"
          fi
          if [ ${JUST_RAN} -eq 1 ] ; then
            sleep ${SLEEP}
            head -c 80 /dev/zero | tr '\0' '=' ; echo
          fi
        done
      fi
    elif echo "${elm}" | grep "^=" > /dev/null ; then
      option=$(echo ${elm} | cut -d'=' -f 1)
      values=$(echo ${elm} | cut -d'=' -f 2)
      for value in ${values} ; do
        PROGRAM_NAME=$(echo "${PROGRAM}"  | sed 's/.*\///')
        DETAILS=$(echo "${4}" | sed 's/_*\._*/\./')
        LOG_FILENAME="${LOGDIR}/${PROGRAM_NAME}.${DETAILS}.${ext}.${value}"
        startRun "${1}" $(expr $2 + 1) "${3}" "${LOG_FILENAME}"
      done
    else
      option=$(echo ${elm} | cut -d'=' -f 1)
      values=$(echo ${elm} | cut -d'=' -f 2)
      if [ "${values}" == "${option}" ] ; then
        startRun "${1}" $(expr $2 + 1) "${3}${option} " "${4}_$(echo ${option} | tr -d '_-')"
      else
        for value in ${values} ; do
          if echo "${option} ${value}" | grep "/" > /dev/null ; then
            startRun "${1}" $(expr $2 + 1) "${3}${option} ${value} " "${4}"
          else
            startRun "${1}" $(expr $2 + 1) "${3}${option} ${value} " "${4}_$(echo ${option} | tr -d '_-')-$(echo ${value} | tr -d '_-')"
          fi
        done
      fi
    fi
  else
    #PROGRAM_NAME=$(echo "${PROGRAM}"  | sed 's/.*\///')
    #DETAILS=$(echo "${4}" | sed 's/_*\._*/\./' | sed 's/'$(echo -e '\033')'/'${ext}'/')
    #LOG_FILENAME="${PROGRAM_NAME}.${DETAILS}"

    CMD="${PROGRAM} ${3}"
    LOGFILE="${4}".log
    if [ ${MODE} -eq 1 ] ; then
      echo "${LOGFILE}"
      EXEC "$CMD"
    elif [ ${MODE} -eq 0 ] ; then
      EXEC "$CMD" 2>&1 >> "${LOGFILE}"
      cat "${LOGFILE}"
      #sleep ${SLEEP}
      JUST_RAN=1
      return ${JUST_RAN}
    elif [ ${MODE} -eq 2 ] ; then
      #echo "${LOGFILE}"
      ls "${LOGFILE}"
    fi
  fi
)
}
if [ ${MODE} -eq 0 ] ; then
  head -c 80 /dev/zero | tr '\0' '=' ; echo
fi
# startRun <PROGRAM> <OPTION_INDEX> <PROGRAM-ARGS> <FILENAME>
startRun "${PROGRAM}" 0 "" "."
