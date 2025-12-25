// Infra-Ops Skill
const operation = inputs.operation || 'setup';

const operations = {
  setup: `## VPS Initial Setup

### 1. Security Basics
\`\`\`bash
# Update system
apt update && apt upgrade -y

# Create non-root user
adduser deploy
usermod -aG sudo deploy

# Setup SSH key auth
mkdir -p /home/deploy/.ssh
chmod 700 /home/deploy/.ssh
# Add your public key to authorized_keys

# Disable password auth
sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
systemctl restart sshd
\`\`\`

### 2. Firewall
\`\`\`bash
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
\`\`\`

### 3. Fail2ban
\`\`\`bash
apt install fail2ban -y
systemctl enable fail2ban
\`\`\``,

  docker: `## Docker Setup

\`\`\`bash
# Install Docker
curl -fsSL https://get.docker.com | sh
usermod -aG docker deploy

# Install Docker Compose
apt install docker-compose-plugin -y

# Verify
docker --version
docker compose version
\`\`\`

### Docker Compose Template
\`\`\`yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    restart: unless-stopped
\`\`\``,

  coolify: `## Coolify Self-Hosted PaaS

### Installation
\`\`\`bash
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
\`\`\`

### Features
- One-click deployments
- Automatic SSL via Let's Encrypt
- Database provisioning
- Monitoring & logs
- GitHub/GitLab integration

### Post-Install
1. Access at https://your-server:8000
2. Create admin account
3. Add your Git source
4. Deploy applications`,

  secure: `## Security Hardening Checklist

### SSH Hardening
\`\`\`bash
# /etc/ssh/sshd_config
PermitRootLogin no
PasswordAuthentication no
MaxAuthTries 3
ClientAliveInterval 300
\`\`\`

### Auto Updates
\`\`\`bash
apt install unattended-upgrades -y
dpkg-reconfigure -plow unattended-upgrades
\`\`\`

### Monitoring
\`\`\`bash
# Install monitoring
apt install htop iotop nethogs -y
\`\`\``
};

console.log(operations[operation] || operations.setup);