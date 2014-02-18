. bin/activate;
source /home/ubuntu/aws_key.sh;
celery -A tasks worker --loglevel=info;