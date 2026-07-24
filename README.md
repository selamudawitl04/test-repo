# Free GitHub AI Code Review with Gemini

This repository demonstrates a **100% free** AI code review setup using Google's Gemini API and GitHub Actions, with no third-party marketplace actions or paid services.

## How It Works

1. When you open or update a **pull request**, the GitHub Actions workflow triggers
2. The workflow extracts the code diff from your PR
3. It sends the diff to **Google Gemini API** (free tier) for review
4. The AI review is posted as a comment on your PR automatically

## Setup Instructions

### Step 1: Get a Free Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey) (free, no credit card needed)
2. Click **"Create API Key"** → **"Create API key in new project"**
3. Copy your API key (starts with `AIza...`)

### Step 2: Add the Key to Your Repository

1. Go to your GitHub repository **Settings**
2. Navigate to **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Name: `GEMINI_API_KEY`
5. Value: Paste your API key from Step 1
6. Click **"Add secret"**

### Step 3: Test It

1. Create a new branch and make some code changes (e.g., add a problematic line)
2. Push to GitHub and open a **Pull Request**
3. GitHub Actions will automatically run and post an AI review comment within ~30-60 seconds
4. Check the PR for the 🤖 **Gemini AI Code Review** comment

## How the Files Work

- **`.github/workflows/gemini-review.yml`** — The GitHub Actions workflow that triggers on PRs
- **`.github/scripts/gemini_review.py`** — Python script that calls the Gemini API and formats the review
- **`index.html`** — Example file with intentional code issues for testing the reviewer

## Cost

**Completely free!**
- Google Gemini API free tier: up to **60 requests per minute** (plenty for code reviews)
- GitHub Actions: free tier includes **2,000 minutes/month** (this uses ~1-2 min per review)
- No credit card required, no hidden charges

## What It Checks For

The AI reviewer looks for:
- 🔒 Security issues (XSS, injection attacks, etc.)
- ♿ Accessibility problems (missing alt text, semantic HTML, etc.)
- ⚡ Performance issues
- 📋 Code quality and best practices
- ⚠️ Deprecated APIs or HTML tags

## Customization

Edit `.github/scripts/gemini_review.py` to:
- Change the review prompt (lines ~30-50) to focus on different issues
- Switch to a different Gemini model (currently `gemini-2.0-flash`)
- Add support for other file types beyond HTML

Edit `.github/workflows/gemini-review.yml` to:
- Run on different trigger events (`push`, `pull_request_review`, etc.)
- Exclude certain file types from review
- Post reviews to a different channel (Slack, Discord, etc.)

## Limitations

- ⏱️ **API Rate Limits**: Free tier is generous but limited to 60 req/min
- 📝 **Diff Size**: Very large diffs (>30KB) may hit token limits and need truncation
- 🌐 **Network**: Requires internet access to call Gemini API
- 🔑 **API Key Security**: Keep the key secret! GitHub automatically masks it in logs

## Troubleshooting

**"API key not set" error**
- Double-check the secret name is exactly `GEMINI_API_KEY`
- Make sure you're in the correct repository (not a fork)
- Re-save the secret and try again

**"No diff found" warning**
- Make sure the PR base branch exists on GitHub (e.g., `main` or `master`)
- Check that you actually have code changes in the PR

**"Rate limit exceeded"**
- Wait a minute and try again
- Or open a new PR with fewer/smaller changes

## License

Free to use for any purpose. This is a learning/testing setup.
