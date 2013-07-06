#!/bin/bash

#DIR is directory ssh_wrapper.sh is located in
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ssh -p22 $1 $2
