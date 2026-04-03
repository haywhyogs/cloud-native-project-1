
#### Application Not Loading (504 Error)

Azure App Service requires explicit port configuration. The application was updated to run on port 80 to align with platform expectations.

Set:
WEBSITES_PORT=80

#### Docker Login Failure (WSL Issue)

Docker login failed with credential storage errors

* Cause:

Conflict between WSL and Docker Desktop credential helper

* Solution:

Removed credential helper from Docker config
Used --password-stdin for login