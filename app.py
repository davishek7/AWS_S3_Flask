from flask import Flask,render_template,request,redirect,url_for,flash,Response,session
from flask_bootstrap import Bootstrap
from filters import datetimeformat,file_type
from resources import get_bucket,get_bucket_list
from config import SECRET_KEY

app=Flask(__name__)
Bootstrap(app)
app.jinja_env.filters['datetimeformat']=datetimeformat
app.jinja_env.filters['file_type']=file_type
app.secret_key=SECRET_KEY


@app.route('/',methods=['GET','POST'])
def index():
	if request.method=='POST':
		bucket=request.form['bucket']
		session['bucket']=bucket
		return redirect(url_for('files'))
	else:
		buckets=get_bucket_list()
		return render_template('index.html',buckets=buckets,title="Bucket")

@app.route('/files')
def files():
	my_bucket=get_bucket()
	summaries=my_bucket.objects.all()

	return render_template('files.html',my_bucket=my_bucket,files=summaries,title="Object")

@app.route('/upload',methods=['POST'])
def upload():
	file=request.files['file']

	my_bucket=get_bucket()
	my_bucket.Object(file.filename).put(Body=file)

	flash('File uploaded successfully!')
	return redirect(url_for('files'))

@app.route('/delete',methods=['POST'])
def delete():
	key=request.form['key']

	my_bucket=get_bucket()
	my_bucket.Object(key).delete()

	flash('File deleted successfully!')
	return redirect(url_for('files'))

@app.route('/download',methods=['POST'])
def download():
	key=request.form['key']

	my_bucket=get_bucket()

	file_obj=my_bucket.Object(key).get()

	return Response(
		file_obj['Body'].read(),
		mimetype='text/plain',
		headers={"Content-Disposition":f"attachment;filename{key}"}
		)


if __name__=='__main__':
	app.run()