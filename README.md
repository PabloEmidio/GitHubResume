# RPC Service to generate pdf files of resume based on user's GitHub's activity

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

---

This repository is part of [Git Resume RPC Architecture](https://github.com/PabloEmidio/GitResume). But can be used as you pelase
through nameko RPC, as seen in the example bellow.

```python
from nameko.standalone.rpc import ClusterRpcProxy

config = {
    'AMQP_URI': AMQP_URI # e.g. "pyamqp://guest:guest@localhost"
}

with ClusterRpcProxy(config) as cluster_rpc:
    cluster_rpc.GitHubResume.generate_pdf('MyUser')
```

or using your own service

```python
from nameko.rpc import rpc, RpcProxy


class MyServiceName:
    name = 'MyServiceName'
    gb = RpcProxy('GitHubResume')

    @rpc
    def use_github_service(self, *args, **kwargs) -> dict:
        return self.gb.generate_document(args.pop(0) or kwargs['name'])
```
