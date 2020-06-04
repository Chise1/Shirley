更新文档之后要make html执行，
- 生成新的文档
```shell script
make html
```

- 代码上传到pypi的方法：
```shell script
# 打包
python setup.py sdist
# 注册包
twine register dist/*
# 上传包
twine upload dist/*
```