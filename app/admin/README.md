# Dealvoy Admin System

Comprehensive admin dashboard and management interface for the Dealvoy platform.

## Features

- 👥 **User Management**: View, edit, and manage user accounts and subscriptions
- 📊 **Analytics Dashboard**: Real-time analytics and business intelligence
- 🔧 **System Health**: Monitor system performance and service status
- 🔒 **Security Center**: Security monitoring and access control
- 💰 **Revenue Analytics**: Subscription and revenue tracking
- ⚙️ **System Settings**: Platform configuration and settings

## Components

### AdminLayout.tsx
Main layout component with navigation sidebar and responsive design.

### UserManagement.tsx
Complete user management interface with:
- User search and filtering
- Subscription status management
- Revenue tracking per user
- Bulk operations

### SystemHealth.tsx
System monitoring dashboard with:
- Real-time performance metrics
- Service status monitoring
- Alert management
- System resource usage

## API Routes

### User Management
- `GET /admin/users` - List users with pagination and filters
- `GET /admin/users/{id}` - Get detailed user information
- `PUT /admin/users/{id}/status` - Update user status

### Analytics
- `GET /admin/analytics/overview` - High-level analytics overview
- `GET /admin/analytics/revenue` - Revenue analytics
- `GET /admin/analytics/usage` - Usage statistics

### System Health
- `GET /admin/system/health` - System health metrics
- `GET /admin/system/logs` - System logs
- `POST /admin/system/restart` - Restart services

## Authentication & Authorization

All admin routes require:
1. Valid user authentication
2. Admin role privileges
3. Specific permissions for sensitive operations

### Permission Levels
- `user_management` - User account operations
- `subscription_management` - Billing and subscription control
- `system_monitoring` - System health and logs access
- `analytics_access` - Analytics and reporting
- `security_management` - Security settings and audit logs
- `super_admin` - Full system access

## Setup

1. **Install dependencies**:
   ```bash
   npm install lucide-react recharts
   ```

2. **Add admin routes to FastAPI**:
   ```python
   from .admin.admin_routes import router as admin_router
   app.include_router(admin_router)
   ```

3. **Configure admin authentication**:
   ```python
   from .admin.admin_auth import get_current_admin_user
   ```

4. **Set up database models** for admin permissions and roles

## Security Considerations

- All admin operations are logged for audit purposes
- Rate limiting on sensitive operations
- IP allowlisting for admin access (optional)
- Two-factor authentication for admin accounts
- Regular security audits and access reviews

## Usage Examples

### Check System Health
```javascript
const health = await fetch('/admin/system/health')
const data = await health.json()
console.log('System status:', data.overall_status)
```

### Get User Analytics
```javascript
const analytics = await fetch('/admin/analytics/overview')
const data = await analytics.json()
console.log('Total users:', data.users.total)
```

### Update User Status
```javascript
await fetch(`/admin/users/${userId}/status`, {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ status: 'suspended' })
})
```

## Development

- Use React DevTools for component debugging
- Test admin operations in a staging environment first
- Monitor admin action logs regularly
- Keep admin dependencies up to date

## Deployment

The admin system can be deployed as part of the main application or as a separate admin-only interface for enhanced security.

### Separate Admin Deployment
1. Create dedicated admin subdomain
2. Configure separate authentication
3. Restrict network access
4. Use dedicated admin database permissions

## Monitoring

- Admin action audit logs
- Failed authentication attempts
- System performance metrics
- User activity monitoring
- Revenue and subscription tracking

## License

Private - Dealvoy Platform
