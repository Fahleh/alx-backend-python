# 0x03. Unittests and Integration Tests

![unit test meme](https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/medias/2020/1/f088970b450e82c881ea.gif?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20240729%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240729T130649Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=e084c03c457b755ac32bb75657e02d8b065c2d06af39de146183aa142e7d2da6)

## Learning Objectives

At the end of this project, you are expected to be able to explain to anyone, without the help of Google:

- The difference between unit and integration tests.
- Common testing patterns such as mocking, parametrizations, and fixtures.

## Testing Overview

### Unit Testing

Unit testing is the process of testing that a particular function returns expected results for different sets of inputs. A unit test is designed to test standard inputs and corner cases. It should only test the logic defined inside the tested function. Calls to additional functions should generally be mocked, especially if they make network or database calls.

**Goal of Unit Testing:**  
To answer the question: _If everything defined outside this function works as expected, does this function work as expected?_

### Integration Testing

Integration tests aim to test a code path end-to-end. Generally, only low-level functions that make external calls such as HTTP requests, file I/O, or database I/O are mocked.

**Goal of Integration Testing:**  
To test interactions between every part of your code.

## Running Tests

Execute your tests with the following command:

```bash
$ python -m unittest path/to/test_file.py
```

## Learning Objectives

At the end of this project, you are expected to be able to [`explain to anyone`](https://fs.blog/feynman-learning-technique/), without the help of Google:

- The difference between unit and integration tests.
- Common testing patterns such as mocking, parametrizations and fixtures

## Requirements

- All your files will be interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7)
- All your files should end with a new line
- The first line of all your files should be exactly #!/usr/bin/env python3
- A README.md file, at the root of the folder of the project, is mandatory
- Your code should use the pycodestyle style (version 2.5)
- All your files must be executable
- All your modules should have a documentation (python3 -c 'print(**import**("my_module").**doc**)')
- All your classes should have a documentation (python3 -c 'print(**import**("my_module").MyClass.**doc**)')
- All your functions (inside and outside a class) should have a documentation (python3 -c 'print(**import**("my_module").my_function.**doc**)' and python3 -c 'print(**import**("my_module").MyClass.my_function.**doc**)')
- A documentation is not a simple word, it’s a real sentence explaining what’s the purpose of the module, class or method (the length of it will be verified)
- All your functions and coroutines must be type-annotated.

## Required Files

### `utility.py` [or `download`](https://intranet-projects-files.s3.amazonaws.com/webstack/utils.py)
```python
#!/usr/bin/env python3
"""Generic utilities for github org client.
"""
import requests
from functools import wraps
from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
)

__all__ = [
    "access_nested_map",
    "get_json",
    "memoize",
]


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access nested map with key path.
    Parameters
    ----------
    nested_map: Mapping
        A nested map
    path: Sequence
        a sequence of key representing a path to the value
    Example
    -------
    >>> nested_map = {"a": {"b": {"c": 1}}}
    >>> access_nested_map(nested_map, ["a", "b", "c"])
    1
    """
    for key in path:
        if not isinstance(nested_map, Mapping):
            raise KeyError(key)
        nested_map = nested_map[key]

    return nested_map


def get_json(url: str) -> Dict:
    """Get JSON from remote URL.
    """
    response = requests.get(url)
    return response.json()


def memoize(fn: Callable) -> Callable:
    """Decorator to memoize a method.
    Example
    -------
    class MyClass:
        @memoize
        def a_method(self):
            print("a_method called")
            return 42
    >>> my_object = MyClass()
    >>> my_object.a_method
    a_method called
    42
    >>> my_object.a_method
    42
    """
    attr_name = "_{}".format(fn.__name__)

    @wraps(fn)
    def memoized(self):
        """"memoized wraps"""
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return property(memoized)
```

### `client.py` [or `download`](https://intranet-projects-files.s3.amazonaws.com/webstack/client.py)
```python
#!/usr/bin/env python3
"""A github org client
"""
from typing import (
    List,
    Dict,
)

from utils import (
    get_json,
    access_nested_map,
    memoize,
)


class GithubOrgClient:
    """A Githib org client
    """
    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        """Init method of GithubOrgClient"""
        self._org_name = org_name

    @memoize
    def org(self) -> Dict:
        """Memoize org"""
        return get_json(self.ORG_URL.format(org=self._org_name))

    @property
    def _public_repos_url(self) -> str:
        """Public repos URL"""
        return self.org["repos_url"]

    @memoize
    def repos_payload(self) -> Dict:
        """Memoize repos payload"""
        return get_json(self._public_repos_url)

    def public_repos(self, license: str = None) -> List[str]:
        """Public repos"""
        json_payload = self.repos_payload
        public_repos = [
            repo["name"] for repo in json_payload
            if license is None or self.has_license(repo, license)
        ]

        return public_repos

    @staticmethod
    def has_license(repo: Dict[str, Dict], license_key: str) -> bool:
        """Static: has_license"""
        assert license_key is not None, "license_key cannot be None"
        try:
            has_license = access_nested_map(repo, ("license", "key")) == license_key
        except KeyError:
            return False
        return has_license
```

### `fixtures.py` [`download`](https://intranet-projects-files.s3.amazonaws.com/webstack/fixtures.py)
