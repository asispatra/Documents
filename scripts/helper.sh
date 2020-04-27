#!/bin/bash

#
# File Name: helper.sh
#
# Date: April 15, 2020
# Author: Asis Kumar Patra
# Purpose:
#
#

# Write your shell script here.

function EXEC {
  COMMAND=$1
  echo "# ${COMMAND}"
  if [ ${MODE} -eq 0 ] ; then
    echo "### START: $(date)"
    eval "${COMMAND}" 2>&1
    echo "### END: $(date)"
    echo
  fi
}

function SUBEXEC {
  COMMAND=$1
  echo "## ${COMMAND}"
  if [ ${MODE} -eq 0 ] ; then
    eval "${COMMAND}" 2>&1
    echo
  fi
}

function SMT {
  SMTV=${1}
  if [ ${SMTV} -ne $(echo "$(ppc64_cpu --smt | grep '=' || echo 'SMT=1')" | cut -d"=" -f2) ] ; then
    echo "Setting SMT=${SMTV}..."
    CMD="ppc64_cpu --smt=${SMTV}"
    EXEC "${CMD}"
    sleep ${SLEEP}
  else
    echo "SMT=${SMTV} : unchanged!"
  fi
  CMD="ppc64_cpu --smt"
  EXEC "${CMD}"

}

function HEADER {
  CMD="ls -l | head -${1}"
  SUBEXEC "${CMD}"
}
