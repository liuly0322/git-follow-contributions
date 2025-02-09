# github-follow-contributions

帮你收集 (~~视奸~~) 你 follow 的所有用户最近都贡献了哪些仓库。

Help you to see what repositories people you follow have recently contributed to.

## Setup

GitHub personal access token is required:

- Apply it [here](https://github.com/settings/personal-access-tokens).
- The **read permission of followers** is needed. Permissions -> Followers -> Access: Read-only -> Generate token.

Once you get the personal access token:

```bash
GITHUB_TOKEN=replace_me python3 main.py
```

## Local Preview

Host the website:

```bash
python3 -m http.server # then open http://localhost:8000
```

You can filter events that you are interested in.

![preview](https://github.com/user-attachments/assets/5c0b04b0-144c-4987-9470-57c8f1f7345c)

## GitHub Pages

(In repository page)

1. Settings -> Secrets and variables -> Actions -> Repository secrets -> set `GH_TOKEN` to the **personal access token** above.
2. Settings -> Actions -> General -> Workflow permissions -> **Read and write permissions**.
3. Actions -> Build and Deploy to GitHub Pages -> **Run workflow**.
4. Settings -> GitHub Pages -> Source: `gh-pages` branch.

## License

MIT
