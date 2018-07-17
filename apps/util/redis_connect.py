from redis import Redis
# 0 is cache
# 1 is rds 分享链接
rds_for_share = Redis(host="127.0.0.1", port=6379, db=1, password="Lr715356")
# 2 is rds 短信验证码
rds_for_verify = Redis(host='127.0.0.1', port=6379, db=2, password='Lr715356')
# 3 4 is rds celery
