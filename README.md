app.yamlはこんな感じ
```
runtime: python37
handlers:
- url: /main
  script: main.py
env_variables:
  NOTION_MIKAN_TOKEN: 'V2_TOKEN'

```