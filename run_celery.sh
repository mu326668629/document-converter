. bin/activate;
export AWS_ACCESS_KEY_ID=AKIAJLVAFTGBYJAHPSQA;
export AWS_SECRET_ACCESS_KEY=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;
celery -A tasks worker --loglevel=info;