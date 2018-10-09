---
id: nlu-info
title: NLU Info - /info
sidebar_label: /info
---

Get bot (repository) details.

The response content is same from repository endpoint available in Bothub Engine HTTP service.

## Resource Information

| Title | Value |
|--|--|
| Methods | GET |
| Response formats | JSON |

## Parameters

| Name | Required | Description | Default value |
|--|--|--|--|

## Example Request

```bash
curl -X GET \
  https://nlp.bothub.it/info/ \
  -H 'Authorization: Bearer 123e4567-e89b-12d3-a456-426655440000'
```

## Example Response
```json
{
    "uuid": "b679cb31-a764-499d-9b0e-ae992c12f513",
    "owner": 1,
    "owner__nickname": "douglas",
    "name": "My Bot",
    "slug": "mybot",
    "language": "en",
    "available_languages": [
        "en"
    ],
    "categories": [
        1
    ],
    "categories_list": [
        {
            "id": 1,
            "name": "Communication"
        }
    ],
    "description": "Bot's description",
    "is_private": true,
    "intents": [
        "greet",
        "bye"
    ],
    "entities": [
        "hi",
        "hello",
        "bye"
    ],
    "labels": [
        {
            "repository": "Repository object (b679cb31-a764-499d-9b0e-ae992c12f513)",
            "value": "hi",
            "entities": [
                "hi",
                "hello"
            ]
        },
        {
            "repository": "Repository object (b679cb31-a764-499d-9b0e-ae992c12f513)",
            "value": "bye",
            "entities": [
                "bye"
            ]
        }
    ],
    "labels_list": [
        "hi",
        "bye"
    ],
    "examples__count": 15,
    "authorization": null,
    "available_request_authorization": false,
    "request_authorization": null,
    "ready_for_train": false,
    "votes_sum": null,
    "created_at": "2018-10-04T20:11:47.993485Z"
}
```