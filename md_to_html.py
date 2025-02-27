import os
import markdown


def find_markdown_files(base_folder="user_guides"):
    md_files = []
    for root, _, files in os.walk(base_folder):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    return md_files


def main():
    for mark_down_file in find_markdown_files():
        print(f'processing {mark_down_file}')
        with open(mark_down_file, "r", encoding="utf-8") as f:
            md_content = f.read()
        html_content = markdown.markdown(md_content)
        with open(mark_down_file.replace('.md','.html'), "w", encoding="utf-8") as f:
            print(f"wrote {mark_down_file.replace('.md','.html')}")
            f.write(html_content)


if __name__ == '__main__':
    main()
