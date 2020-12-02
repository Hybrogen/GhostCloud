ProcNumber=`ps aux|grep -w "manage.py runserver 0.0.0.0:23333"|grep -v grep|wc -l`
if [ $ProcNumber -ne 0 ];then
   result=$ProcNumber
else
   result=0
   python3 manage.py runserver 0.0.0.0:23333
fi
# echo ${result}
