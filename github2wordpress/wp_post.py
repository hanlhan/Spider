# encoding:utf-8
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import taxonomies
from wordpress_xmlrpc.methods.posts import EditPost, GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo


def wp_post(client, title, content, tags):
    post = WordPressPost()
    post.title = title
    post.content = content
    post.terms = tags

    post.id = client.call(NewPost(post))

    # whoops, I forgot to publish it!
    post.post_status = 'publish'
    post.custom_fields = []
    result = client.call(EditPost(post.id, post))
    return result


def wp_post_custom_field(client, title, content, custom_field):
    post = WordPressPost()
    post.title = title
    post.content = content
    post.custom_fields = []
    post.custom_fields.append(custom_field)
    post.id = client.call(NewPost(post))

    # whoops, I forgot to publish it!
    post.post_status = 'publish'
    post.custom_fields = []
    result = client.call(EditPost(post.id, post))
    return result


if __name__ == '__main__':
    client = Client('http://tf86.com/xmlrpc.php', 'fendouai', 'wo2010WO,./')
    categories = client.call(taxonomies.GetTerms(
        'category', {"search": "sklearn"}))
    title = 'My post custom ddd fields test'
    content = 'This is a wonderful blog post about XML-RPC. <img class="alignnone size-medium wp-image-30" src="http://wawa.tf86.com/wp-content/uploads/2019/04/WechatIMG1309-144x300.png" alt="" width="144" height="300" />'
    custom_field = {
        'key': 'hello1',
        'value': "world1"
    }

    result = wp_post(client, title, content, custom_field)
    print(result)
