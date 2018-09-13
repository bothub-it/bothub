---
id: nlu-request
title: NLU Request
sidebar_label: Request
---

You can make HTTP requests to the NLU's endpoints available in NLP HTTP service.

**The available endpoints are:**

| Path | Description | Doc
|--|--|--|
| /info | Get repository info | [Access documentation](/docs/en/nlu-info)
| /parse | Parse/analyze text | [Access documentation](/docs/en/nlu-parse)
| /train | Train a new version of bot | [Access documentation](/docs/en/nlu-train)

## Credential

Credentials must be passed as the Authorization header for each request. Make sure you have the `Authentication: Bearer [Your Authorization Token]` HTTP header to all requests.

### Authorization Token

To make requests you need an Authorization Token. It identifies who are the user and what bot (repository) is responsible for processing, in other words, each user has a token for each repository that they have access to.

You can retrieve this Authorization Token visiting your repository page in Bothub Webapp at Analyze tab or make [authenticated request to API]() to [Authorization Token Endpoint]().

The Authorization Token is a UUID using canonical textual representation.

**E.g.:**

```text
123e4567-e89b-12d3-a456-426655440000
xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```