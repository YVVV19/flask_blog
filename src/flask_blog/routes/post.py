from sqlalchemy import select, delete
import asyncio
from quart import render_template, request, redirect, url_for
from . import Author, Post, app, Config


@app.get("/posts")
async def posts():
    with Config.SESSION.begin() as session:
        smth = select(Post)
        posts = session.scalars(smth).all()
        return await render_template(
            "index.html",
            posts=[
                Post(
                    id=x.id,
                    created=x.created,
                    content=x.content,
                    author=x.author,
                    title=x.title,
                )
                for x in posts
            ],
        )

@app.post("/posts")
async def create_post():
    form = await request.form
    if form:
        with Config.SESSION.begin() as session:
            post = Post(
                **form,
                author=Author(name="vadim"),
            )
            session.add(post)
    
    return redirect(url_for("posts"))


@app.get("/posts/<int:index>/details")
async def post_details(index: int):
    await asyncio.sleep(1)

    return "Hello world"


@app.get("/posts/delete/<int:index>")
async def delete_post_page(index:int):
    return await render_template("delete_posts.html",index = index) 

@app.post("/posts/delete")
async def delete_post():
    form = await request.form
    post_id = form.get("post_id")
    if post_id:
        with Config.SESSION.begin() as session:
            session.execute(delete(Post).where(Post.id == post_id))
            # post = session.scalars(select(Post).where(Post.id == post_id)).first()
            # if post:
    #         post = Post(
    #             **form,
    #             author=Author(name="vadim"),
    #         )
    #         session.delete(post)
    # await asyncio.sleep(1)
    return redirect(url_for(posts.__name__))