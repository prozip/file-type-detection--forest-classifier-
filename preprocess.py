import os, get_repos

def get_full_paths(lan):
    ext = {'python': '.py', 'javascript': '.js', 'java': '.java'}
    full_paths = []
    for dirpath, dirnames, filenames in os.walk(f'repos\{lan}'):
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            if full_path.endswith(ext[lan]):
                full_paths.append(full_path)

    fpaths_len = len(full_paths)
    print(f"Full paths count: {fpaths_len}")
    return full_paths

def fetch_dataset(languages):

    for lan in languages:
        get_repos.fetch_urls(lan, 1000000, lan +'-urls.txt')
        get_repos.fetch_repos(lan, 20)

def get_dataset(languages):

    fetch_dataset(languages)

    corpus = []
    labels = []
    file_types_and_labels = [(languages[x], x-1) for x in range(3)]


    for files_path, label in file_types_and_labels:
        files = get_full_paths(files_path)
        for file_path in files:
            try:
                with open(file_path, "r") as f:
                    data = f.read().replace("\n","")
            except:
                pass
            data = str(data)
            corpus.append(data)
            labels.append(label)

    return corpus, labels