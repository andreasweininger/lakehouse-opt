# this script initializes the environment and resets the lab

# 1. clean lab directory and reload from git
sudo rm -rf ~labuser/lakehouse-opt
sudo su - labuser -c "git clone https://github.com/andreasweininger/lakehouse-opt.git"

# 2. install the required python libraries
sudo su - labuser -c ~labuser/lakehouse-opt/prep-lab/install-python-requirements.sh

# 3. start the jupyter notebooks
sudo su - labuser -c ~labuser/lakehouse-opt/prep-lab/start-nb.sh

# 4. (re-)start the watsonx.data engine
sudo ~labuser/lakehouse-opt/install/stop-wxd.sh
sudo ~labuser/lakehouse-opt/install/start-wxd.sh

# 5. delete data from Presto tables and Milvus collection
sudo su - labuser -c ~labuser/lakehouse-opt/prep-lab/remove-data.sh

# 6. delete data in Minio
/usr/local/bin/mc rm --recursive --force myminio/iceberg-bucket/simple_rag
