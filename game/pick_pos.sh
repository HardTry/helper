mmax=20
mmin=1

for i in `seq $mmin $mmax`
do
   echo $i
   python pick_pos.py
done

python glue.py
