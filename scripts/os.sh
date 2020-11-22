#!/bin/sh

case "$(uname -s)" in

   Darwin)
     echo 1
     ;;

   Linux)
     echo 2
     ;;

   CYGWIN*|MINGW32*|MSYS*|MINGW*)
     echo 3
     ;;

   # Add here more strings to compare
   # See correspondence table at the bottom of this answer

   *)
     echo 0
     ;;
esac