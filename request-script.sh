# bash request-script.sh
# param:
#-c, --concurrent=NUM      CONCURRENT users, default is 10
#-r, --reps=NUM            REPS, number of times to run the test.
TIMES=5
for i in $(eval echo "{1..$TIMES}")
do
    siege -c 1 -r 3 http://localhost:8000/
    siege -c 3 -r 5 http://localhost:8000/getBookByAuthor
    siege -c 2 -r 5 http://localhost:8000/getBooksByCategory/5000 #Simulation d'erreur
    siege -c 2 -r 5 http://localhost:8082/getBooksByCategory/5000 #Simulation d'erreur
    siege -c 5 -r 3 http://localhost:8082/getBooksByCategory/1
    siege -c 2 -r 3 http://localhost:8000/getBookByAuthor/panama
    siege -c 2 -r 3 http://localhost:8082/getBooksByAuthor/h
    siege -c 1 -r 1 http://localhost:8082/getBooksByTitle/h
    siege -c 3 -r 5 http://localhost:8000/getAllBooks
    siege -c 10 -r 5 http://localhost:8082/getAllBooks
    sleep 5
done
