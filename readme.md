# 说明

因 serv00 要求 90 天未登录会清理账号，本仓库通过 GitHub Actions 定期 SSH 登录并用 Server酱推送结果，帮助保持账号活跃。

## 准备
- Fork 本仓库，准备好 serv00 账号。
- 在 GitHub 仓库 Settings > Secrets 配置：
  - `SSH_INFO`：包含 SSH 连接信息的 JSON 字符串，例如：
    ```json
    [
      {"hostname": "服务器号", "username": "用户名", "password": "密码"},
      {"hostname": "s5.serv00.com", "username": "user", "password": "password"}
    ]
    ```
  - `SCKEY`：Server酱推送密钥。

## 运行
- Actions 页面手动触发一次 “Run SSH Login” 验证。
- 默认计划：每月 5 日 11:00 UTC（北京时间 19:00）。如需修改，在 `.github/workflows/run.yml` 调整 `cron`。

## 注意
- Secrets 含敏感信息，请勿泄露。
