#!/bin/bash

usage ()
{
  echo "usage: rdfunit.sh <parameters go here...>"
  echo "This script is not intended to be manually ran !"
}


if [ $# -lt 4 -o $# -gt 4 ]
then
  usage
  exit 1
fi