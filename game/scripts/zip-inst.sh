tar cf $1.tar $1
gzip -9 $1.tar
mv $1.tar.gz ../pics
