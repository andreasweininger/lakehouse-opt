mkdir /wxd-install
cd /wxd-install

export LH_ROOT_DIR=/wxd-install
export LH_RELEASE_TAG=latest
export IBM_LH_TOOLBOX=cp.icr.io/cpopen/watsonx-data/ibm-lakehouse-toolbox:$LH_RELEASE_TAG
export LH_REGISTRY=cp.icr.io/cp/watsonx-data
export PROD_USER=cp
export IBM_ENTITLEMENT_KEY=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJJQk0gTWFya2V0cGxhY2UiLCJpYXQiOjE3MTY5ODIwNDgsImp0aSI6IjYxM2JhODk0Mzg5YzQ4ZjA5MGVkYjE3MTM3YTg2NzY1In0.uBOcL0PNPiNLA26IvE_chTHHflh5bvwTvxLr0Maywqw
export IBM_ICR_IO=cp.icr.io

export DOCKER_EXE=podman

$DOCKER_EXE pull $IBM_LH_TOOLBOX
id=$($DOCKER_EXE create $IBM_LH_TOOLBOX)
$DOCKER_EXE cp $id:/opt - > /tmp/pkg.tar
$DOCKER_EXE rm $id
id=

tar -xf /tmp/pkg.tar -C /tmp
cat /tmp/opt/bom.txt
cksum /tmp/opt/*/*
tar -xf /tmp/opt/dev/ibm-lh-dev-*.tgz -C $LH_ROOT_DIR

$DOCKER_EXE login ${IBM_ICR_IO} \
--username=${PROD_USER} \
--password=${IBM_ENTITLEMENT_KEY}

$LH_ROOT_DIR/ibm-lh-dev/bin/setup --license_acceptance=y --runtime=$DOCKER_EXE

$LH_ROOT_DIR/ibm-lh-dev/bin/setup-milvusetup-milvus
