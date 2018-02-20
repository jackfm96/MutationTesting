for mutant in [0-9].py;
do
	rm $mutant;
done
python3 mutate.py fuzzywuzzy.py 10
for mutant in [0-9].py;
do
	rm -f *.pyc ;
	cp $mutant fuzzywuzzy.py;
	python publictest-half.py 2> test.output;
	echo $mutant;
	grep FAILED test.output;
done
cp OldFuzzyWuzzy.py fuzzywuzzy.py
#rm test.output