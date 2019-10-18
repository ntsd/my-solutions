#!/bin/bash
head -c -1 | perl -lpe '$_=unpack"B*"' | sed -E '
s/.(.{7})/\1/g;
s/(^|[1])0/\1 00 0/g;
s/(^|[0])1/\1 0 1/g;
s/1/0/g;
s/^.//'


# 1. Dump binary stream
#    1.1. Display file as formatted binary (without a trailing newline)
#    1.2. Strip extra data (file position and ASCII representation)
#    1.3. Strip a leading 0 from every octet
#    1.4. Strip whitespaces
# 2. Split homogeneous groups by newlines
# 3. Extract first character of every line to a separate column
# 4. Replace leading zeros with "00" sentence
# 5. Replace all 1's with 0's (this will encode both leading 1
#    as "0" sentence and series of 1's for length encoding
# 6. Replace newlines with spaces and trim trailing space
tr -d '\n' | xxd -b | sed -e 's/[^:]*:\([01 ]\+\).*$/\1/g' | sed -e 's/ 0/ /g' | tr -d ' \n' |\
sed -e 's/\(0\+\|1\+\)/\1\n/g' |\
sed -e 's/^\(\(.\).*\)$/\2 \1/g' |\
sed -e 's/^0/00/g' |\
tr '1\n' '0 ' |\
sed -e 's/ \+$//g'

echo $(
    bc<<<"obase=2;`tr -d '\n' | od -An -tuC | tr \  \;`" |
    while read; do printf '%07d' "$REPLY"; done |
    tr -d \\n |
    grep -oP "1+|0+" |
    sed 's/^0/00 0/;s/^1/0 0/;s/1/0/g'
)

read -r M
for((i = 0; i < ${#M}; i++))
do
c=$(printf "%d" "'${M:i:1}")
b=$(echo "obase=2;"$c | bc)
printf "%07d" $b
done |\
sed -r 's/(0+)/00 \1 /g;s/(1+)/0 \1 /g;s/1/0/g;s/.$//'


read M
for((i=0;i<${#M};i++))
do
printf "%07d" $(echo "obase=2;"$(printf "%d" "'${M:i:1}")|bc)
done|sed -r 's/(0+)/00 \1 /g;s/(1+)/0 \1 /g;s/1/0/g;s/.$//'

https://unix.stackexchange.com/questions/98948/ascii-to-binary-and-binary-to-ascii-conversion-tools