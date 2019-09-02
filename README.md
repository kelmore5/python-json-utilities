# JSONs

JSONs is a small library of JSON utility functions compiled for personal needs. There's 
nothing too fancy nor anything you can't find from another library, but JSONs consists of
smaller functions to be used rather than relying on larger packages.

The functions include things like check equal, flatten, intersection, merge, replace keys, etc.

## Personal Note

JSONs is only on Github because I reference it in other projects. I don't have any plans 
to maintain this project, but I will update it from time to time. 

# Install

You can install this project directly from Github via:

```bash
$ pip3.7 install git+https://github.com/kelmore5/python-json-utilities.git
```

## Dependencies

- Python 3.7
- [kelmore_arrays](https://github.com/kelmore5/python-array-utilities)

# Usage

Once installed, you can import the main class like so:

    >>> from kelmore_json import JSONTools as JSON
    >>>
    >>> x = { 'one': 1, 'two': 2, 'three': 3 }
    >>> y = { 'four': 4, 'five': 5 }
    >>> z = { 'one': 1, 'two': 2 }
    >>>
    >>> JSON.transform.create(['key_one', 'key_two'], [1, 2])                   # { 'key_one': 1, 'key_two': 2 }
    >>> JSON.transform.merge(x, y)                                              # { 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5 }
    >>> JSON.transform.replace_keys(z, ['one', 'two'], ['first', 'second'])     # { 'first': 1, 'second': 2 }
    .
    .
    .

# Documentation

To be updated
