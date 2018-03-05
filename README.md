# morning_file
deal the two file:compare or de-duplication them and so on

#show the two files differences
python run.py --show_different ./test-files1.txt ./test-files2.txt

#show the two files commons
python run.py --show_common ./test-files1.txt ./test-files2.txt

#if this file is dict or csv, you can specify key values and export the result file
python run.py --show_different ./techcrunch_normal.csv ./techcrunch3.csv  --export ./ repo_id repo_id