#!/bin/bash

#
# File Name: getdata_fromFiles.sh
#
# Date: April 15, 2020
# Author: Asis Kumar Patra
# Purpose:
#
#

# Write your shell script here.

function grabdata {
  cat ${1} | grep "${2}" | sed 's/.*'${2}':\s\(.*\)$/\1/g'
}

DATAPATTERNS=(
"99.0th"="grabdata"
"99.5th"="grabdata"
"99.9th"="grabdata"
)

# SMT,r,t,m
DATA_FIELDS=(
"SMT"
"runtime(R)"
"threads(T)"
"message-threads(M)"
)
DATA_FIELD_ORDERS=(
"0 1 2 3" # Default
"0 2 3 1"
"1 2 3 0"
"1 3 2 0"
)

BASE_REPORT="perfp9zz_schbench"
LOGDIR="logs"
LOGFILE_PATTERN="*.log"

cat /dev/null > "${BASE_REPORT}.list"
for ORDER in "${DATA_FIELD_ORDERS[@]}" ; do
  #echo "${ORDER}"

  LOGFILE=$(ls ${LOGDIR}/${LOGFILE_PATTERN} | tail -1)
  #echo "${LOGFILE}"
  if [ -z ${DATA_FIELDS+x} ]; then
    DATA_FIELDS=($(echo "${LOGFILE}" | cut -d'.' -f2,3,5 | tr '_.' ' ' | sed 's/-[^ ]* / /g' | sed 's/ [^ ]*$//'))
  fi
  FINAL_DATA_FIELDS=()
  for FIELD_INDEX in ${ORDER} ; do
    FINAL_DATA_FIELDS+=("${DATA_FIELDS[${FIELD_INDEX}]}")
  done
  SIZE="${#FINAL_DATA_FIELDS[@]}"
  EXT="$(echo ${FINAL_DATA_FIELDS[$(expr ${SIZE} - 2)]} | tr 'a-z' 'A-Z')vs$(echo ${FINAL_DATA_FIELDS[$(expr ${SIZE} - 1)]} | tr 'a-z' 'A-Z')"
  REPORT="$(echo ${BASE_REPORT}_${EXT} | sed 's/([^)]*)//g' | tr -d '-')"
  EXT=$(echo ${EXT} | sed 's/([^)]*)//g' | tr -d '-')
  #echo "${REPORT}"

  FINAL_DATA_FIELDS+=("iteration")

  for elm in "${DATAPATTERNS[@]}" ; do
    METRIC=$(echo ${elm} | cut -d'=' -f 1)
    GRABBER=$(echo ${elm} | cut -d'=' -f 2)
    FINAL_DATA_FIELDS+=("${METRIC}")
  done
  HEADER=""
  for FIELD in "${FINAL_DATA_FIELDS[@]}" ; do
    HEADER="${HEADER},${FIELD}"
  done
  HEADER="${HEADER:1}"
  HEADER_CSV="${REPORT}.header.csv"
  echo "${HEADER}" > "${HEADER_CSV}"

  #DATA_CSV="${REPORT}.data.csv"
  #echo "python csv2xlsx.py \"${BASE_REPORT}\" \"${EXT}\" \"${HEADER_CSV}\" \"${DATA_CSV}\""
  #exit

  DATA_CSV="${REPORT}.data.csv"
  cat /dev/null > "${DATA_CSV}"
  #for LOGFILE in $(ls ${LOGDIR}/${LOGFILE_PATTERN} | head -20) ; do
  for LOGFILE in $(ls ${LOGDIR}/${LOGFILE_PATTERN}) ; do
    #echo "${LOGFILE}"
    DATA_VALUES=($(echo "${LOGFILE}" | cut -d'.' -f2,3,5 | tr '_.' ' ' | sed 's/[^ ]*-//g'))
    FINAL_DATA_VALUES=()
    for FIELD_INDEX in ${ORDER} ; do
      FINAL_DATA_VALUES+=("${DATA_VALUES[${FIELD_INDEX}]}")
    done
    FINAL_DATA_VALUES+=("${DATA_VALUES[${#FINAL_DATA_VALUES[@]}]}")
    for elm in "${DATAPATTERNS[@]}" ; do
      METRIC=$(echo ${elm} | cut -d'=' -f 1)
      GRABBER=$(echo ${elm} | cut -d'=' -f 2)
      DATA=$(eval "${GRABBER} ${LOGFILE} \"${METRIC}\"")
      FINAL_DATA_VALUES+=("${DATA}")
    done
    DATA_ROW=""
    for VALUE in "${FINAL_DATA_VALUES[@]}" ; do
      DATA_ROW="${DATA_ROW},${VALUE}"
    done
    DATA_ROW="${DATA_ROW:1}"
    echo "${DATA_ROW}" >> "${DATA_CSV}"
  done

  ### DATA GENERATED: Let's put the data in
   #echo "python csv2xlsx.py \"${BASE_REPORT}\" \"${EXT}\" \"$(echo ${EXT} | sed 's/([^)]*)//g')\" \"${HEADER_CSV}\" \"${DATA_CSV}\""
   #python csv2xlsx.py "${BASE_REPORT}" "${EXT}" "$(echo ${EXT} | sed 's/([^)]*)//g')" "${HEADER_CSV}" "${DATA_CSV}"
   #echo "python csv2xlsx.py \"${BASE_REPORT}\" \"${EXT}\" \"${HEADER_CSV}\" \"${DATA_CSV}\""
   #python csv2xlsx.py "${BASE_REPORT}" "${EXT}" "${HEADER_CSV}" "${DATA_CSV}"

   echo "\"${EXT}\" \"${HEADER_CSV}\" \"${DATA_CSV}\""
   echo "\"${EXT}\" \"${HEADER_CSV}\" \"${DATA_CSV}\"" >> "${BASE_REPORT}.list"
  #exit
done

CMD="python csv2xlsx.py ${BASE_REPORT} ${BASE_REPORT}.list"
eval "${CMD}"
echo "${CMD}"
