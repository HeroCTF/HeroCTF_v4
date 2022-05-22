#!/bin/bash

cd /self
rm $(ls | grep "^.\{8\}\(-.\{4\}\)\{3\}-.\{12\}$") >& /dev/null
