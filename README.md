Document Converter
==================

You can convert various file formats back and forth. Supported formats are PDF, HTML, DOC, PPT and TXT


Document converter uses variuos other services - [LibreOffice](https://www.libreoffice.org/) (used as a service), [unoconv](https://github.com/dagwieers/unoconv), [PostgreSQL](http://www.postgresql.org/), [Amazon S3](http://aws.amazon.com/s3/), [RabbitMQ](https://www.rabbitmq.com/).

And requires following environment variables to be present :

1. `APP_ENVIRONMENT` - Specifies the environment in which the app should run, expected values are : production or development
2. `AWS_ACCESS_KEY_ID` - this is required by [Boto](https://github.com/boto/boto).
3. `AWS_SECRET_ACCESS_KEY` - this is required by [Boto](https://github.com/boto/boto).
4. `S3_BUCKET` - Specifies the bucket in which input/output files will be stored before/after conversion.
5. `POSTGRES_DB_URI` - Specifies PostgreSQL database URI
6. `FLASK_SECRET_KEY` - Specifies secret key needed by Flask [read more](http://flask.pocoo.org/docs/config/#configuration-basics).
7. `BROKER_URL` - Specifies broker URL of [Celery](http://celery.readthedocs.org/en/latest/configuration.html#broker-settings).
