---
id: nlu
title: NLU Docs
sidebar_label: Introduction
---

Currently [NLP](/docs/en/bothub#nlp) has only one service, the NLU application which is its main feature.

NLU retrieves the sentences (examples) fed by the [Bothub Engine](/docs/en/bothub#engine) and, using machine learning generates statistical models. After having a trained model, the system begins to identify intents and entities in the analyzed texts.

Users can communicate with the NLU through an HTTP service (provided by [NLP](/docs/en/bothub#nlp)) as a API. See the documentation for this API and endpoints [here](/docs/en/nlu-request).

## Example

Input:
```text
I would like to buy a car.
```

Output:
```text
Intent: "buy"

Entities:
- Entity: "car"
  Value: "carro"
  Label: "vehicle"
```