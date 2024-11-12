# -*- coding: utf-8 -*-
import os
import oss2
from django.core.management.base import BaseCommand
from oss2.credentials import EnvironmentVariableCredentialsProvider


class Command(BaseCommand):
    help = 'Download data from OSS and import it into MySQL'

    def handle(self, *args, **options):
        # 从环境变量中获取访问凭证
        auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
        
        # 填写 Bucket 所在地域对应的 Endpoint 和实际 Bucket 名称
        bucket = oss2.Bucket(auth, 'https://oss-cn-beijing.aliyuncs.com', 'ist-mini-semester-july')

        # 下载 OSS 文件到本地文件
        object_name = 'runs/document.txt'
        local_file = 'C:/Users/86157/Desktop/Django_test/myproject/downloaded_file.txt'

        try:
            bucket.get_object_to_file(object_name, local_file)
            print(f"文件 {object_name} 已成功下载到 {local_file}")
        except oss2.exceptions.NoSuchKey:
            print(f"OSS 中找不到对象: {object_name}")
        except oss2.exceptions.ClientError as e:
            print(f"ClientError: {e}")
        except Exception as e:
            print(f"发生了其他错误: {e}")
