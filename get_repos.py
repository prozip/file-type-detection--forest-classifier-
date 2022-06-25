import requests, os
from tqdm import tqdm

# fetch clone urls from github api v3
def fetch_urls(language, fetch_star, save_file):
    print("start fetch_urls...")

    f = open("repos_url/" + save_file, "a")
    token = open("github_token.txt", "r").read()
    headers = {"Authorization": f"token {token}"}


    # fetch by most star github repos
    url = f"https://api.github.com/search/repositories?q=language:{language}&sort=stars&order=desc&per_page=100"
    data = requests.get(url, headers=headers)
    obj = data.json()
    if obj.get("items"):
        for items in obj.get("items"):
            clone_url = items.get("clone_url")
            author = items.get("owner").get("login")
            name = items.get("name")
            f.write(clone_url + "\t" + name + "\t" + author + "\n")

    print(f"fetch done, saved to {save_file}")


# Keep only python file
def clean_repos(path, lan):
    ext = {'python':'.py', 'javascript':'.js', 'java':'.java'}

    os.system(f"rm -rf {path}/.git")

    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            if full_path.endswith(ext[lan]):
                pass
                # print((f"Keeping {full_path}"))
            else:
                # print((f"Deleting {full_path}"))
                os.remove(full_path)


# download repos and clean
def fetch_repos(language, num):
    f = open(f"repos_url/{language}-urls.txt", "r")
    line = 0
    for data in f:
        print("current line: ", line)
        url, name, author = data.strip().split("\t")
        os.system(f"git clone --depth 1 {url} repos/{language}/{author}/{name}")
        clean_repos(f"repos/{language}/{author}/{name}", language)
        line += 1
        if line>num:
            break
