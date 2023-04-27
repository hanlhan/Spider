# coding=utf-8
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import media, posts
from wp_media import upload_image

from find_image import *

def down_image(image):
    print("image:",image)
    temp_path="images_temp"
    image_name=image.split("/")[-1]
    ir = requests.get(image)
    if ir.status_code == 200:
        open(os.path.join(temp_path, image_name), 'wb').write(ir.content)
        return image_name
    else:
        return None

def image_localization(md, images_temp, client, repo):
    # 找 html 格式图片
    html_images = find_html_images(md)
    for html_image in html_images:
        image_src = find_html_image_src(html_image)
        # 如果是绝对地址，直接下载然后上传
        if "http" in image_src:
            download_image_src = image_src
        elif image_src[0] == ".":
            download_image_src = "https://raw.githubusercontent.com/" + \
                repo+"/master"+image_src[1:]
        else:
            download_image_src = "https://github.com/"+image_src
        image_name = down_image(download_image_src)
        image_url = upload_image(images_temp, image_name, client=client)
        if (image_url == None):
            print("fail to dowload image")
        else:
            md = md.replace(image_src, image_url)

    # 找 md 格式的图片
    md_images = find_md_images(md)
    for md_image in md_images:
        image_src = find_md_image_src(md_image)
        image_src = image_src[0].replace("(", "").replace(")", "")
        # 如果是绝对地址，直接下载然后上传
        if "http" in image_src:
            download_image_src = image_src
        elif image_src[0] == ".":
            download_image_src = "https://raw.githubusercontent.com/" + \
                repo+"/master"+image_src[1:]
            print(download_image_src)
        else:
            download_image_src = "https://github.com/"+image_src
        try:
            image_name = down_image(download_image_src)
        except Exception as e:
            # print(e)
            image_name = None
        if (image_name == None):
            image_url = None
        else:
            image_url = upload_image(images_temp, image_name, client=client)
        if (image_url == None):
            print("fail to dowload image")
        else:
            md = md.replace(image_src, image_url)

    return md


if __name__ == "__main__":
    # or using an access token
    g = Github("9a94f25c8bf511b0c94b0ac1e936e56b859a7e56")
    repo_name = "haizlin/fe-interview"
    repo = g.get_repo(repo_name)
    print(repo.get_topics())

    contents = repo.get_contents("README.md")
    print(type(contents))
    print(contents.content)
    str_md = base64.b64decode(contents.content).decode("utf-8")
    print(str_md)
    images_temp = "images_temp"
    client = Client('http://tf86.com/xmlrpc.php', 'fendouai', 'wo2010WO,./')

    print(image_localization(str_md, images_temp, client, repo_name))
