# Challenge
>Can you get all the flags???
>
>Source: http://backdoor.static.beast.sdslabs.co/static/meow/dist.zip
>
>Link: http://51.158.118.84:16001/

# First Impression

The website looks like a twitter feed where users can create and report posts and all users can see all posts as show below:

![Imgur](https://i.imgur.com/6YpqOXN.png)

While looking at the posts, you can notice that some posts posted by Neko Cat (the verified user/ admin) are kind of censored with the message saying `Only approved followers can view the post` as shown below:

![Imgur](https://i.imgur.com/fOk6iV1.png)

So first thing I wanted to try was seeing the content of these posts.

# Source code

While checking the `db.py` file in the source code we can see a functionality to get the content of a certain post using it's  post_id and instance as shown below: 
```python
def get_post(session, post_id, instance):
    post = session.query(Post).filter_by(id=post_id,
                                         instance=instance).first()
    if not post:
        return (False, 'Post does not exist')

    poster = session.query(User).filter_by(username=post.posted_by).first()

    res = {'posted_by': post.posted_by, 'posted_name': poster.name,
           'content': post.content, 'preview': post.preview,
           'link': post.link, 'instance': post.instance,
           'id': post.id}

    return (True, res)
```

While looking at the report function in `app.py` I noticed that it sends the same parameters `post_id` and `instance` as shown below:
```python
def report(request):
    if request.method == 'GET':
        if not check_csrf(request):
            return redirect('/404')
        post_id = request.args.get('id')
        instance = request.args.get('instance')
        if post_id.isdigit():
            botuser("http://127.0.0.1", instance, post_id)

    return redirect('/')
```
# Looking at the hidden content posts

I continued by checking the GET request URL sent while reporting a post and got this:
 
`http://51.158.118.84:16001/report?id=3212&instance=ffe6fb23-9c99-442b-bbeb-3a2479b94d21&csrf=6174ccc91211e3c6`

After replacing `report` with `post` I could see the content of the post so I did that on the first hidden content post and got this :

![Imgur](https://i.imgur.com/XvkI1gz.png)

After looking through the hidden content posts managed to get the FLAG in one of them as shown below! : 

![Imgur](https://i.imgur.com/Z7I5igg.png)
