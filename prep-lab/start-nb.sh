# kill previous instances of jupyter notebooks
echo "stop existing notebook servers"
kill $(ps aux|fgrep bin/jupyter-notebook|awk '{print $2}')

# start jupyter notebooks
echo "start notebook server"
. ~labuser/venv/bin/activate
nohup jupyter notebook 1>~labuser/simple-rag/logs/jupyter-notebook.log 2>&1 & 