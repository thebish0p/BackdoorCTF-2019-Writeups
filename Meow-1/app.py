from flagon import Flagon, render_template, url_parse, redirect
from db import get_session, user_exists, verified_user
from db import get_posts, get_users, add_user
from db import check_user, add_post, get_post, add_follower

from bs4 import BeautifulSoup
import requests
from functools import wraps
from os import urandom

from chal_visitor import botuser


app = Flagon(__name__)
session = get_session()


def get_post_preview(url):
    scheme, netloc, path, query, fragment = url_parse(url)

    # No oranges allowed
    if scheme != 'http' and scheme != 'https':
        return None

    try:
        r = requests.get(url)
    except Exception:
        return None

    if "/flaginfo" in r.url:
        return None

    soup = BeautifulSoup(r.text, 'html.parser')
    if soup.body:
        result = ''.join(soup.body.findAll(text=True)).strip()
        result = ' '.join(result.split())
        return result[:280]

    return None


def genrate_random_string(length):
    return urandom(length//2).hex()


def check_csrf(request):
    user_csrf = request.args.get('csrf') or request.form.get('csrf')
    session_csrf = request.session.get('csrf')
    request.session['csrf'] = genrate_random_string(16)

    if session_csrf == user_csrf:
        return True
    return False


def login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        uname = args[0].session.get('username')
        if not uname or not user_exists(session, uname)[0]:
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated_func


def apply_csp(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        resp = f(*args, **kwargs)
        csp = "; ".join([
            "script-src " + " ".join(["'self'",
                                      "cdnjs.cloudflare.com",
                                      "*.bootstrapcdn.com",
                                      "code.jquery.com"])
        ])
        resp.headers["Content-Security-Policy"] = csp

        return resp
    return decorated_func


def ensure_csrf(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        csrf = args[0].session.get('csrf', None)
        if csrf is None:
            args[0].session['csrf'] = genrate_random_string(16)
        return f(*args, **kwargs)
    return decorated_func


@app.route('/')
@ensure_csrf
@login_required
@apply_csp
def index(request):
    users = get_users(session, request.session['username'])[1]
    posts = get_posts(session, request.session['username'])[1]
    return render_template('index.html',
                           username=request.session['username'],
                           name=request.session['name'],
                           users=users,
                           posts=posts,
                           csrf=request.session['csrf'])


@app.route('/login')
@ensure_csrf
@apply_csp
def login(request):
    if request.method == 'GET':
        return render_template('login.html',
                               csrf=request.session['csrf'])

    if request.method == 'POST':
        if not check_csrf(request):
            return redirect('/404')
        success, msg = check_user(session,
                                  request.form['username'],
                                  request.form['password'])

        if success:
            request.session['username'] = request.form['username']
            request.session['name'] = msg
            return redirect('/')
        else:
            return render_template('login.html',
                                   error=msg,
                                   csrf=request.session['csrf'])


@app.route('/logout')
@ensure_csrf
@apply_csp
def logout(request):
    if not check_csrf(request):
        return redirect('/404')
    request.session['username'] = None
    return redirect('/login')


@app.route('/register')
@ensure_csrf
@apply_csp
def register(request):
    if request.method == 'GET':
        return render_template('register.html', csrf=request.session['csrf'])

    if request.method == 'POST':
        if not check_csrf(request):
            return redirect('/404')
        success, msg = add_user(session, request.form['username'],
                                request.form['fullname'],
                                request.form['password'],
                                request.form['confirm-password'])
        if success:
            request.session['username'] = request.form['username']
            request.session['name'] = request.form['fullname']
            return redirect('/')
        else:
            return render_template('register.html',
                                   error=msg,
                                   csrf=request.session['csrf'])


@app.route('/404')
@ensure_csrf
@apply_csp
def error(request):
    return render_template('404.html')


@app.route('/newpost')
@ensure_csrf
@login_required
@apply_csp
def newpost(request):
    if not check_csrf(request):
        return redirect('/404')
    post = request.form.get('submission-text')

    if (not post or len(post) > 280):
        return redirect('/')

    preview = None
    link = None

    for word in post.split(' '):
        if word.startswith('[link]'):
            link = " ".join(word.split('[link]')[1:]).strip()
            if verified_user(session, request.session.get('username'))[0]:
                preview = get_post_preview(link)
            link = link
            break

    post = post.replace('[link]', '')

    add_post(session, request.session.get('username'), post, link, preview)

    return redirect('/')


@app.route('/post')
@ensure_csrf
@login_required
@apply_csp
def view_post(request):
    if request.method == 'GET':
        post_id = request.args.get('id')
        instance = request.args.get('instance')
        success, post = get_post(session, post_id, instance)
        if success:
            return render_template('post.html',
                                   post=post,
                                   csrf=request.session['csrf'])
        else:
            return render_template('404.html')


@app.route('/report')
@ensure_csrf
@login_required
@apply_csp
def report(request):
    if request.method == 'GET':
        if not check_csrf(request):
            return redirect('/404')
        post_id = request.args.get('id')
        instance = request.args.get('instance')
        if post_id.isdigit():
            botuser("http://127.0.0.1", instance, post_id)

    return redirect('/')


@app.route('/approve')
@ensure_csrf
@login_required
@apply_csp
def approve_follower(request):
    # TODO: Frontend support for the private acounts
    if request.method == 'GET':
        if not check_csrf(request):
            return redirect('/404')

        approver_username = request.session.get('username')
        follower_username = request.args.get('username')

        success, msg = add_follower(session, approver_username,
                                    follower_username)

        if success:
            return redirect('/')
        else:
            return redirect('/404')


if __name__ == '__main__':
    app.run('0.0.0.0', port=80)
