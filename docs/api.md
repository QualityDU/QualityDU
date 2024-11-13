### Endpoints:
| Endpoint  | Request | Req body | Description | Success response |
| --- | --- | --- | --- | --- |
| `/api/user` | `GET /api/user?user_id=<user_id>` | (none) | Get user data | `...` |
| `/api/user` | `POST /api/user` | ... | Create a new user | `...` |
| `/api/user` | `PUT /api/user` | ... | Update user data | `...` |
| `/api/user` | `DELETE /api/user` | ... | Delete user | `...` |
| `/api/email-verify` | `GET /api/email-verify?token=<token>&username=<username>` | (none) | Verify email | `...` |

### Notice
- Error response is always in the format of `{"status": "error", "message": "..."}`