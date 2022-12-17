if [ $PORT -eq 8080 ]
then
  python3 -m flask run --host=0.0.0.0 --port=8080
else
  python3 -m flask run --host=0.0.0.0 --port=80
fi
