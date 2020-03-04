# Bothub
[![Build Status](https://travis-ci.org/Ilhasoft/bothub-engine.svg?branch=master)](https://travis-ci.org/Ilhasoft/bothub-engine) [![Coverage Status](https://coveralls.io/repos/github/Ilhasoft/bothub-engine/badge.svg?branch=master)](https://coveralls.io/github/Ilhasoft/bothub-engine?branch=master) [![Python Version](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/) [![License GPL-3.0](https://img.shields.io/badge/license-%20GPL--3.0-yellow.svg)](https://github.com/Ilhasoft/bothub-engine/blob/master/LICENSE)

Bothub is an open platform for predicting, training and sharing NLP datasets in multiple languages.


## About

Bothub is the Github for NLP datasets, that allows to build, improve and translate them.

You can read more about the project's purpose on this
[blog post](https://push.al/en/this-is-how-bothub-started/).


## What's here

This repo is the "master" repo for all Bothub-related projects. It hosts 
the documentation and other misc. resources for Bothub. Code for other
projects, like the [WebApp](https://github.com/ilhasoft/bothub-webapp), [Engine](https://github.com/ilhasoft/bothub-engine) 
and [NLP](https://github.com/ilhasoft/bothub-nlp), are hosted in other 
repositories.

## Documentation

All documentation available on [docs.bothub.it](https://docs.bothub.it/).

# Deployment

## Instant Server Installation with Docker

<a href="https://hub.docker.com/u/bothubit"><img src="https://www.docker.com/sites/default/files/d8/styles/role_icon/public/2019-07/horizontal-logo-monochromatic-white.png?itok=SBlK2TGU" width="230" height="70" alt="Bothub" /></a>

Instead of using standard Docker commands, you may want a little more automated management of your deployment. This is where using Docker-compose can be useful.

* Make sure Docker and Docker-compone are installed and operational.
* Check if your docker-swarm is enabled, if not, go to the [installation](https://docs.docker.com/engine/swarm/swarm-tutorial/) session.
* Edit image: bothubit/bothub-(project): develop to specify which image you want to use (see the section Images available in Docker)


Add two networks for internal project communication:
```
docker network create bothub-nlp -d overlay
```

```
docker network create postgres -d overlay
```

Then add docker-compose.yml with docker stack

```
docker stack deploy --compose-file=docker-compose.yml bothub
```

This docker stack process allows you to upload our services quickly, it automatically downloads our images generated from the Docker Hub itself.
With that you have practically moved up our entire stack, you will only be missing the frontend.

To build the bothub-webapp project you need to have the dependencies installed correctly:

| # | Version |
|--|--|
| git | >= 2.x.x
| nodejs | >= 12.x.x
| yarn | >= 1.x.x

To install the project you must clone the project:

```
make clone_webapp
```

Then, you can notice that a new folder was created with the project code [bothub-webapp](), just access the directory with the command:
```
cd bothub-webapp
```

and install the project dependencies with the yarn command:
```
yarn install
```

after installing the dependencies, just start bothub-webapp's development server with the command:
```
yarn start
```

this way you will already be able to use our entire stack, remembering that each project has its environment variables configurable, to change consult the documentation for each specific project.


## Contributing

**We are looking for collaboration from the Open Source community!** There's so much we want to do, 
including but not limited to: enhancing existing applications with new features, 
optimizing the NLP tools and algorithms involved that boost accuracy, and bringing our work closer to
the public to leverage their inputs via blog posts and tutorials.

* Please read our [contribution guidelines](https://github.com/ilhasoft/bothub/blob/master/.github/CONTRIBUTING.md) 
for details on what and how you can contribute.

* Report a bug by using [this guideline](https://github.com/ilhasoft/bothub/blob/master/.github/CONTRIBUTING.md#report-a-bug) 
for details on what and how you can contribute.

## Using the issue tracker

The issues created here will be analysed and validated. They can be submitted to the [bothub](https://github.com/ilhasoft/bothub), [bothub-webapp](https://github.com/ilhasoft/bothub-webapp), and/or [bothub-nlp](https://github.com/ilhasoft/bothub-nlp) repository as well.

The issue tracker is the preferred channel for [bug reports](https://github.com/ilhasoft/bothub/blob/master/.github/CONTRIBUTING.md#report-a-bug) and [features requests](#features), but please respect the following restrictions:

- Please **do not** use the issue tracker for personal support requests (send an email to bothub@ilhasoft.com.br).

- Please **do not** derail or troll issues. Keep the discussion on topic and respect the opinions of others.

<a name="features"></a>
## Feature requests

Feature requests are welcome. But take a moment to find out whether your idea fits with the scope and aims of the project. It's up to *you* to make a strong case to convince the project's developers of the merits of this feature. Please provide as much detail and context as possible.

To request a new feature, create a new issue using the label `feature request`.
