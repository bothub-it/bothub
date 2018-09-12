---
id: bothub
title: About Bothub
sidebar_label: About Bothub
---

Bothub is an open platform for predicting, training and sharing NLP (Natural Language Processing) datasets in multiple languages. It is Github for NLP, which allows you to build, improve, train and translate datasets.

## Apps and services

The project has three applications, distributed in 3 Git repositories.

### Engine

[Github](https://github.com/Ilhasoft/bothub-engine) | [API Docs](/docs/en/api)

Bothub Engine is responsible for validating and persisting system data in the database. These data can be users, bots (repositories), sentences (examples), training (statistical models) and logs.

For communication with other applications, the Engine serves an HTTP service as Rest API. You can check API Docs [here](/docs/en/api).

### NLP

[Github](https://github.com/Ilhasoft/bothub-nlp) | [Documentação do NLU](/docs/en/nlu)

Bothub NLP integrates tools for training statistical models and for prediction based on them.

#### NLU

Currently NLP has only one service, the NLU application which is its main feature.

NLP retrieves the sentences (examples) fed by the Engine and using machine learning generates statistical models. After having a trained model the system begins to identify intentions and manages to extract entities of texts.

Users can communicate with the NLP through an HTTP service. See the documentation for this API  [here](/docs/en/nlu).

##### Example

Input:
```
I would like to buy a car.
```

Output:
```
Intent: "buy"

Entities:
- Entity: "car"
  Value: "carro"
  Label: "vehicle"
```

### Webapp

[Github](https://github.com/Ilhasoft/bothub-webapp)

Bothub Webapp is the web interface where users can communicate in an intuitive way with other projects.

In Webapp you can create and manage your account, bots, sentences and trainings.