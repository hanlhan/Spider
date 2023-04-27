import base64

from github import Github

# or using an access token
g = Github("9a94f25c8bf511b0c94b0ac1e936e56b859a7e56")

repo = g.get_repo("fendouai/FaceRank")
print(repo.get_topics())

contents = repo.get_contents("readme.md")
print(type(contents))
print(contents.content)
str_url = base64.b64decode(contents.content).decode("utf-8")
print(str_url)
# print(dir(contents))

contents = repo.get_contents("")
for content in contents:
    print(content)
