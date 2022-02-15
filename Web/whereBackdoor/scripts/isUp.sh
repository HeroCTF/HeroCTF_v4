out=`curl -s $1`
if [ ${#out} -ge 1 ]
then
    echo $1": UP"
else
    echo $1": DOWN"
fi