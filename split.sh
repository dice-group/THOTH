#!/usr/bin/env bash
cd $1
shuf --random-source=../random-file orig.$2 > data.$2
shuf --random-source=../random-file orig.$3 > data.$3
x=`wc -l data.$2 | cut -f1 -d' '`
a=$(($x*8/10))
b=$(($x-$a))
c=$(($b/2))
d=$c
echo "Splitting by ($a,$b,$c,$d)..."
head -n$a data.$2 > train.$2
head -n$a data.$3 > train.$3
tail -n$b data.$2 > atad.$2
tail -n$b data.$3 > atad.$3
head -n$c atad.$2 > dev.$2
head -n$c atad.$3 > dev.$3
tail -n$d atad.$2 > test.$2
tail -n$d atad.$3 > test.$3
python ../build_vocab.py orig.$2 > vocab.$2 2> /dev/null
python ../build_vocab.py orig.$3 > vocab.$3 2> /dev/null
wc -l *.$2
wc -l *.$3
cd ..
