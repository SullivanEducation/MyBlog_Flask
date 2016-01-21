#!usr/bin/python
#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
import MySQLdb

app = Flask(__name__, static_url_path='')
conn = MySQLdb.connect(host="localhost", user='blog', db='blog',  passwd='sullivan', charset='utf8')

'''
   메인 페이지를 표시한다.
   @url /
'''
@app.route("/")
def main():
    # 게시물 목록
    c = conn.cursor()
    c.execute("SELECT * FROM `article` ORDER BY `timestamp` DESC")
    list = c.fetchall()

    #최근 게시물 목록
    c.execute("SELECT `title`, `id` FROM `article` ORDER BY `timestamp` DESC LIMIT 0, 3")
    recent = c.fetchall()
    c.close()

    return render_template("index.html", list=list, recent=recent)


#글 씁니다
@app.route('/write', methods=['GET', 'POST'])
def write() :
    if request.method=='GET' :
        return render_template("write.html")
    elif request.method=='POST':
        c = conn.cursor()
        c.execute("""INSERT INTO `article`(`title`, `body`) VALUES (\'%s\',
        \'%s\')""" % (request.form['title'], request.form['body']))
        conn.commit()
        c.close()

        return redirect("/")

#글 지웁니다
@app.route('/delete/<int:id>')
def delete(id) :
    c = conn.cursor()
    c.execute("DELETE FROM `article` WHERE id=%d" % id)
    conn.commit()
    c.close()

    return redirect("/")

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method=='GET' :
        # 기존 게시물 로드
        c = conn.cursor()
        c.execute("SELECT * FROM `article` WHERE id=%d" % id)
        article = c.fetchone()
        c.close()

        # 기존 게시물 내용 채워서 보여주기
        return render_template("edit.html", title=article[0], body=article[1])

    elif request.method=='POST' :
        # 수정하자. request.form 안에 수정내용 들어있을꺼임
        c = conn.cursor()
        c.execute("UPDATE `article` SET `title` = '%s', `body`='%s' WHERE id=%d"
            % (request.form['title'], request.form['body'], id))
        conn.commit()

        # 수정된 글 보여주기~
        return redirect("/article/%d" % id)

@app.route('/article/<int:id>')
def view(id):
    c = conn.cursor()
    c.execute("SELECT * FROM `article` WHERE id=%d"%id)
    obj = c.fetchone()

    c.execute("SELECT * FROM `comment` WHERE articleid=%d"%id)
    comment = c.fetchall()
    c.close()

    return render_template("view.html", title=obj[0], body=obj[1].split('\n'), article_id=id, comment=comment,
            comment_length=len(comment))

@app.route('/comment_post', methods=['POST'])
def comment():
    c = conn.cursor()
    c.execute("""INSERT INTO `comment`(`body`, `nicname`, `articleid`) VALUES
            (\'%s\', \'%s\', %s)""" % (request.form['body'], request.form['nickname'], request.form['id']))
    conn.commit()
    c.close()

    return redirect("/article/%s" % request.form['id'])

# 서버 키기
if __name__ == "__main__" :
    app.run(debug=True, host='0.0.0.0')
