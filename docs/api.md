### Endpoints:
| Endpoint  | Request | Req body | Description | Success response |
| --- | --- | --- | --- | --- |
| `/api/user` | `GET /api/user?user_id=<user_id>` | (none) | Get user data | `{ "status": "success", "user": {"user_id": ..., "username": ..., "registration_date": ..., "last_login_date": ..., "num_contributions": ..., "karma": ..., "email_verified": ... }} ` |
| `/api/user` | `POST /api/user` | `{"username": "<username>", "password": "<password>", "email": "<email>"}` | Create a new user | `{ "status": "success", "message": "User created successfully" }` |
| `/api/user` | `PUT /api/user` | `{"user_id": "<user_id>", "password": "<password>", "email": "<email>", "sesskey"="<sesskey>"}` | Update user data | `{ "status": "success", "message": "User updated successfully" }` |
| `/api/user` | `DELETE /api/user` | `{"user_id": "<user_id>", "sesskey": "<sesskey>"}` | Delete user | `{ "status": "success", "message": "User deleted successfully" }` |
| `/api/email-verify` | `GET /api/email-verify?token=<token>&username=<username>` | (none) | Verify email | `{ "status": "success", "message": "Email verified." }` |
| `/api/status` | `GET /api/status` | (none) | Get API status | `{ "status": "success", "message": "Service is running" }` |
| `/api/session` | `PUT /api/session` | `{ "username": "<username>", "password": "<password>" }` | Start user session | `{ "status": "success", "message": "Session created successfully.", "session_key": ... }` |
| `/api/session` | `DELETE /api/session` | `{ "username": "<username>", "session_key": "<session_key>" }` | Start user session | `{ "status": "success", "message": "Session deleted successfully." }` |

### Notice
- Error response is always in the format of `{"status": "error", "message": "..."}`
