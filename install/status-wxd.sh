export LH_ROOT_DIR=/wxd-install

$LH_ROOT_DIR/ibm-lh-dev/bin/start
$LH_ROOT_DIR/ibm-lh-dev/bin/start-milvus
$LH_ROOT_DIR/ibm-lh-dev/bin/expose-minio[labuser@RAG install]$ cat status-wxd.sh
export LH_ROOT_DIR=/wxd-install

$LH_ROOT_DIR/ibm-lh-dev/bin/status --all
