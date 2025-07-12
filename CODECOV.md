# CodeCov in GitHub Actions

1. Get your Codecov token:

  - Create an account in `https://codecov.io/`
  - Navigate to your repository's settings
  - Copy the repository upload token (or org-wide token)

2. Add it as a GitHub Secret:
  - In your GitHub repo → Settings → Secrets & variables → Actions
  - Click New repository secret
  - Name: `CODECOV_TOKEN`
  - Value: `(paste your token)`
    
3. Modify your workflow to use the token:

```yaml
      - name: Upload to Codecov
        if: success()  # Only run if previous steps succeed
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}  # Uses the secret
          file: ./coverage.xml  # Explicit path to coverage file
          flags: github-actions  # Optional: tag this upload
```

4. Debugging Tips

  -  Manually inspect the file locally with:
```bash
python -m coverage xml  # If using coverage.py directly
```

  - Add a step to print the coverage summary:
```yaml
- name: Show coverage summary
  run: python -m coverage report

```
