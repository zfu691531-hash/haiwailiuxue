import shutil
import os

api_dir = "d:/Users/Windows/PycharmProjects/haiwailiuxue/api"
if os.path.exists(api_dir):
    shutil.rmtree(api_dir)
    print(f"已删除目录: {api_dir}")
else:
    print(f"目录不存在: {api_dir}")
