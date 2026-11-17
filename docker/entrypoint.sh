#!/bin/bash

# 1.启用错误检查
set -e

# 2.判断是否启用的迁移数据同步，如果是则将数据库迁移同步到数据库中
if [[ "${MIGRATION_ENABLED}" == "true" ]]; then
  echo "Runnable migrations" #输出一个提示
  flask --app app.http.app db upgrade #将迁移同步到数据库
fi

# 3.检测运行的模式(api/celery)，以执行不同的脚本
if [[ "${MODE}" == "celery" ]]; then
  # 4.运行Celery命令,工作模式默认值：-prefork
  celery -A app.http.app.celery worker -P ${CELERY_WORKER_CLASS:-prefork} -c ${CELERY_WORKER_AMOUNT:-1} --loglevel WARNING
else #运行API命令
  # 5.判断当前API环境是开发环境：development，还是生产环境，以执行不同的脚本
  if [[ "${FLASK_ENV}" == "development" ]]; then
    # 6.开发环境使用flask内置服务器，LLMOPS_BIND_ADDRESS默认值：0.0.0.0，port默认值：5001，debug：文件发生变化时，flask自动重启
    flask run --host=${LLMOPS_BIND_ADDRESS:-0.0.0.0} --port=${LLMOPS_PORT:-5001} --debug
  else
    # 7.生产环境使用gunicorn服务器进行部署，并且配置worker：启动的进程数、worker_class：工作进程类型、超时时间、预加载等
    gunicorn \
      --bind "${LLMOPS_BIND_ADDRESS:-0.0.0.0}:${LLMOPS_PORT:-5001}" \
      --workers ${SERVER_WORKER_AMOUNT:-1} \
      --worker-class ${SERVER_WORKER_CLASS:-gthread} \
      --threads ${SERVER_THREAD_AMOUNT:-2} \
      --timeout ${GUNICORN_TIMEOUT:-600} \
      --preload \
      app.http.app:app
  fi
fi