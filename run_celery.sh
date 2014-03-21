workon document-converter
. /home/ubuntu/aws_key.sh;
celery -A tasks worker --loglevel=info;
