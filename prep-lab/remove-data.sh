# initialize Python
. ~labuser/venv/bin/activate

cd ~labuser/simple-rag/prep-lab

# delete data from Presto and Milvus
python ~labuser/simple-rag/prep-lab/remove-data.py