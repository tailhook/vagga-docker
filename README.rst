===============
Vagga in Docker
===============

:Status: PoC / `tracking issue`_

This is a prototype which brings vagga as the first-class tool to OS X and
(possibly) windows through docker's layer of compatibility.

.. _tracking issue: https://github.com/tailhook/vagga-docker/issues/1


Installation
============

Currently it's (you need python >= 3.4)::

    $ pip3 install git+http://github.com/tailhook/vagga-docker
    [ .. snip .. ]
    $ vagga
    Available commands:
        run



Short FAQ
=========

**Why is it in python?** For a quick prototype. It will be integrated into
vagga as soon as is proven to be useful. Or may be we leave it in python if
it would be easier to install.

**So should I try this version or wait it integrated in vagga?** Definitely you
should. The integrated version will work the same.

**Why this uses `docker run` instead of API?** We don't want to reimplement
whole tty handling that is done by docker. If it is proven to be bad descision
we will revisit it later. Also we use API for other things that are not
running anything.

**Is there any difference between this and vagga on linux?** There are two key
differences: you need to export ports that you want to be accessible from the
host system. And we keep files of a container filesystem inside a docker
volume (`the reasons are here`__) However, you can export some part of the
filesystem that is non-sensible for ownership semantics, like this:

__ https://github.com/tailhook/vagga/issues/269

.. code-block:: yaml

    containers:
      django:
        setup:
        - !Alpine v3.3
        - !Py3Install ['Django >=1.9,<1.10']
        _expose-dirs:
        - /usr/lib/python3.5

    commands:
      run: !Command
        description: Start the django development server
        container: django
        _expose-ports: [8080]
        run: python3 manage.py runserver

**Please report if you find any other differences using the tool**. Ah, but
exact text of some error messages may differ, don't be too picky :)

**Why `_expose-ports` and `_expose-dirs` are underscored?** This is a standard
way to add extension metadata or user-defined things in vagga.yaml. We will
remove the underscores as soon as integrate it into main code. Fixing
underscores isn't going to be a big deal.

**Will linux users add `_expose-ports` and `_expose-dirs` for me?** Frankly,
currently probably now. But it's small change that probably noone will need
to delete. In the future we want to apply ``seccomp`` filters to allow to bind
only exposed ports on linux too. And ``expose-dirs`` will be used to filter
directories that will not be optimized for disk usage, so IDE see them as a
normal directory.

(It's also cool project to detect ``expose-dirs`` in vagga metadata and add
them to the project files automatically. But I'm not IDE guy, so I'm not sure
if this is possible, or viable)

**What will be changed when we integrate this into vagga?** We will move more
operations from docker into host system. For example list of commands will
be executed by mac os. Also ``vagga _list``, some parts of ``vagga _clean`` and
so on. But we will do our best to keep semantics exactly the same.


LICENSE
=======

This project has been placed into the public domain.
