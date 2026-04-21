# IMC Prosperity API Notes

## Auth — AWS Cognito SRP

- **User Pool ID**: `eu-west-1_wKiTmHXUE`
- **Client ID**: `5kgp0jm69aeb91paqj1hnps838`
- **Region**: `eu-west-1`
- Flow: `USER_SRP_AUTH` → `PASSWORD_VERIFIER` challenge (handled by `pycognito`)
- Returns: `id_token` (JWT, 1hr expiry), `refresh_token`

## API Base URL

```
https://3dzqiahkw1.execute-api.eu-west-1.amazonaws.com/prod
```

All requests: `Authorization: Bearer {id_token}`

## Endpoints

| Method | Path | Notes |
|--------|------|-------|
| GET | `/rounds` | List rounds; find active round |
| GET | `/submissions/algo/{roundId}?page=1&pageSize=50` | List submissions for round |
| POST | `/submission/algo` | Submit algorithm; `multipart/form-data`, field `file` |
| GET | `/submissions/algo/{submissionId}/zip` | Get presigned S3 URL for results zip |
| GET | `/submissions/algo/{submissionId}/graph` | Get presigned S3 URL for graph |
| GET | `/results/round/{roundId}/algo/zip` | Round results zip |

## Submission Status Values

`SIMULATING` → `FINISHED` | `ERROR` | `ERROR_FINISHED` | `TIMEOUT`

## Submission Object Shape (from Zod schema in JS bundle)

```json
{
  "id": "uuid",
  "teamId": "string",
  "roundId": "string",
  "status": "SIMULATING | FINISHED | ERROR | ERROR_FINISHED | TIMEOUT",
  "submittedAt": "ISO datetime",
  "submittedBy": { "firstName": "string", "lastName": "string" }
}
```
