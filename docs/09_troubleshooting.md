# Troubleshooting

## Authentication Errors
Check that the API key is present in the `.env` file and is valid for the API project.

## Empty Results
Confirm that Markdown files exist inside the docs folder.

## Gemini Service Unavailable
Temporary Gemini `503 UNAVAILABLE` errors are retried up to two times with a short delay. If the service remains unavailable, wait and try again later.
