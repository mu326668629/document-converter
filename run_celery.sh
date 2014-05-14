. /home/ubuntu/.virtualenvs/document-converter/bin/activate
. /home/ubuntu/aws_key.sh;
celery -A tasks worker --loglevel=info;
