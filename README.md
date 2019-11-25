app.yamlはこんな感じ
```
runtime: python37
handlers:
- url: /main
  script: auto
env_variables:
  NOTION_MIKAN_TOKEN: 'V2_TOKEN'

```