# CI/CD Workflows

This directory contains GitHub Actions workflows for continuous integration and deployment.

## Workflows

### 1. CI Pipeline (`ci.yml`)

**Triggers**: Push and PR to `main` and `develop` branches

**Jobs**:
- **Lint Backend**: Python linting with Ruff and Black
- **Lint Frontend**: TypeScript linting with oxlint
- **Build Frontend**: Build React app and upload artifacts
- **Docker Build**: Build both backend and frontend Docker images
- **Security Scan**: Trivy vulnerability scanning

**Status Badge**:
```markdown
[![CI](https://github.com/Rishu22889/grid07_ai/actions/workflows/ci.yml/badge.svg)](https://github.com/Rishu22889/grid07_ai/actions/workflows/ci.yml)
```

### 2. Docker Publish (`docker-publish.yml`)

**Triggers**: 
- Git tags matching `v*` (e.g., `v1.0.0`)
- Manual workflow dispatch

**Jobs**:
- Build and push Docker images to GitHub Container Registry (ghcr.io)
- Automatic semantic versioning from git tags

**Usage**:
```bash
# Create and push a tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

**Pulling images**:
```bash
docker pull ghcr.io/rishu22889/grid07_ai-backend:latest
docker pull ghcr.io/rishu22889/grid07_ai-frontend:latest
```

### 3. Vercel Deploy (`vercel-deploy.yml`)

**Triggers**: Manual workflow dispatch only

**Jobs**:
- Deploy to Vercel on manual trigger

**Setup Required**:
Add `VERCEL_TOKEN` to repository secrets:
1. Go to Vercel Dashboard → Settings → Tokens
2. Create new token
3. Add to GitHub: Settings → Secrets → Actions → New repository secret
   - Name: `VERCEL_TOKEN`
   - Value: Your token

### 4. LLM Evaluation (`evaluation.yml`)

**Triggers**: 
- Weekly schedule (Sunday at midnight)
- Manual workflow dispatch
- Pull requests (optional)

**Jobs**:
- Run full LLM-as-Judge evaluation suite
- Generate dashboard and reports
- Upload results as artifacts
- Comment on PRs with evaluation summary
- Quality gate check (fail if score < 3.0)

**Setup Required**:
Add these secrets to repository:
- `GROQ_API_KEY`: For LLM judge
- `GOOGLE_API_KEY`: For embeddings (if using RAG)

**Artifacts**:
- `latest.json` - Full evaluation results
- `latest.csv` - Spreadsheet format
- `dashboard.html` - Interactive visualization

## Setup Instructions

### Required Secrets

Add these secrets to your GitHub repository (Settings → Secrets → Actions):

1. **VERCEL_TOKEN**: Vercel deployment token (optional, only for automated Vercel deploys)
2. **GROQ_API_KEY**: For LLM evaluation (optional, only for automated eval)
3. **GOOGLE_API_KEY**: For embeddings in evaluation (optional)

### Required Permissions

Ensure GitHub Actions has the following permissions:
- **Contents**: Read
- **Packages**: Write (for Docker registry)
- **Security events**: Write (for Trivy results)
- **Pull requests**: Write (for eval comments)

Configure in: Settings → Actions → General → Workflow permissions

## Branch Protection

Recommended branch protection rules for `main`:

- ✅ Require status checks to pass before merging
  - `Lint Python Backend`
  - `Lint React Frontend`
  - `Build React Frontend`
  - `Build Docker Images`
- ✅ Require branches to be up to date before merging
- ✅ Require linear history

## Local Testing

### Test Python linting locally:
```bash
pip install ruff black
ruff check app/
black --check app/
```

### Test frontend linting locally:
```bash
cd frontend
npm run lint
```

### Test Docker builds locally:
```bash
docker build -f Dockerfile.backend -t grid07-backend:test .
docker build -f Dockerfile.frontend -t grid07-frontend:test .
```

### Test evaluation locally:
```bash
python -m eval.runner
python -m eval.dashboard
open eval/results/dashboard.html
```

## Workflow Files

- `ci.yml` - Main CI pipeline
- `docker-publish.yml` - Docker image publishing
- `vercel-deploy.yml` - Vercel deployment
- `evaluation.yml` - LLM-as-Judge evaluation

## Status Badges

Add these to your README.md:

```markdown
[![CI](https://github.com/Rishu22889/grid07_ai/actions/workflows/ci.yml/badge.svg)](https://github.com/Rishu22889/grid07_ai/actions/workflows/ci.yml)
[![Docker Publish](https://github.com/Rishu22889/grid07_ai/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/Rishu22889/grid07_ai/actions/workflows/docker-publish.yml)
[![Vercel Deploy](https://github.com/Rishu22889/grid07_ai/actions/workflows/vercel-deploy.yml/badge.svg)](https://github.com/Rishu22889/grid07_ai/actions/workflows/vercel-deploy.yml)
[![LLM Evaluation](https://github.com/Rishu22889/grid07_ai/actions/workflows/evaluation.yml/badge.svg)](https://github.com/Rishu22889/grid07_ai/actions/workflows/evaluation.yml)
```
