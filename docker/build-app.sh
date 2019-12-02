
SHPATH=$(cd `dirname $0`; pwd)
BASEPATH=`dirname "$SHPATH"`
if [ ! -f "${BASEPATH}/requirements.txt" ]; then
    echo "requirements.txt not found"
	exit 1
fi

docker build -t opsmanage-app -f ${BASEPATH}/docker/Dockerfile-app  ${BASEPATH}
