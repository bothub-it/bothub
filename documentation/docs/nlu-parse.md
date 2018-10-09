---
id: nlu-parse
title: NLU Parse - /parse
sidebar_label: /parse
---

Do a parse of a text/sentence.

## Resource Information

| Title | Value |
|--|--|
| Methods | GET, POST |
| Response formats | JSON |

## Parameters

The all parameters can be passed via query string using GET or body content (form-data or x-www-form-urlencoded) using POST.

| Name | Description | Required | Default value |
|--|--|--|--|
| text | | Yes | - |
| language | | Optional | The bot's base language |
| rasa_format | | Optional | False |

**Remember:** we do not recommend GET requests if the text contains sensitive data.

## Example Request

```bash
curl -X POST \
  https://nlp.bothub.it/parse/ \
  -H 'Authorization: Bearer 123e4567-e89b-12d3-a456-426655440000' \
  -F text=hello
```

## Example Response

```json
{
    "intent": {
        "name": "greet",
        "confidence": 0.8341536248216568
    },
    "intent_ranking": [
        {
            "name": "greet",
            "confidence": 0.8341536248216568
        },
        {
            "name": "bye",
            "confidence": 0.16584637517834322
        }
    ],
    "labels_list": [
        "hi"
    ],
    "entities_list": [
        "hello"
    ],
    "entities": {
        "hi": {
            "hello": [
                {
                    "value": "hello",
                    "entity": "hello",
                    "confidence": 0.7979280788804916
                }
            ]
        }
    },
    "text": "hello",
    "update_id": 4786,
    "language": "pt_br"
}
```