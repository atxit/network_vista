import markdown

with open("user_guides/complianceAudit/cfgAudit.md", "r", encoding="utf-8") as f:
    md_content = f.read()

html_content = markdown.markdown(md_content)

with open("user_guides/complianceAudit/cfgAudit.html", "w", encoding="utf-8") as f:
    f.write(html_content)
