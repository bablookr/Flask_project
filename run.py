from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import jsonify
import smtplib
import hashlib
import MySQLdb as mdb

from wtforms import Form
from wtforms import TextField
from wtforms import PasswordField
from wtforms import validators
from wtforms.validators import Required
from wtforms.validators import Email
from wtforms.validators import length
from wtforms.validators import ValidationError

from form import *

app=Flask(__name__)
app.secret_key='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

db=mdb.connect('localhost','root','','assignment')
cur=db.cursor()

def pass_send_s(receiver,message):
	sender='iitbhuacadportal@gmail.com'
	receivers=[]
	receivers.append(receiver)
	message = """From: %s
To: %s
Subject: IIT BHU Academic Portal Account Confirmation mail
	
Thank you for registring with IBAP.
We appreciate your interest. 
You are just one step away to access all the information available on our forum.
Kindly click on the following link to verify your E-Mail account and to complete the last steps of setting up your account:
Link- 127.0.0.1:5000%s







This is a system generated mail.Kindly do not reply to it.
For any assisstance or queries please direct your mails to abc@xyz.com

Please ignore this mail if you do not wish to register with IBAP 
 
	""" % (sender, ", ".join(receivers),message)
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('iitbhuacadportal', '1234@4321')
	server.sendmail(sender, receivers, message)
	server.close()
	
def pass_send_t(receiver,message):
	sender='iitbhuacadportal@gmail.com'
	receivers=[]
	receivers.append(receiver)
	message = """From: %s
To: %s
Subject: IIT BHU Academic Portal Account Confirmation mail
	
Thank you for registring with IBAP.
We appreciate your interest. 
You are just one step away to access all the information available on our forum.
Kindly click on the following link to verify your E-Mail account and to complete the last steps of setting up your account:
Link- 127.0.0.1:5000%s







This is a system generated mail.Kindly do not reply to it.
For any assisstance or queries please direct your mails to abc@xyz.com

Please ignore this mail if you do not wish to register with IBAP 
 
	""" % (sender, ", ".join(receivers),message)
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('iitbhuacadportal', '1234@4321')
	server.sendmail(sender, receivers, message)
	server.close()

@app.route('/',methods=['GET','POST'])
def sin():
	if 'student' in session :
		return 'Bye'
	if 'teacher' in session:
		return redirect(url_for('fac'))
	form=loginform(request.form)
	if request.method=='POST':
		if form.validate():
			username=form.username.data
			password=form.password.data
			p=hashlib.md5()
			p.update(password)
			password=p.hexdigest()
			with db:
				cur.execute('select s_pass,roll from s_login where s_email=%s',(username,))
				s_details=cur.fetchall()
				cur.execute('select e_pass,empid from t_login where e_email=%s',(username,))
				t_details=cur.fetchall()
				if s_details:
					if password==s_details[0][0]:
						session['student']=s_details[0][1]
						return redirect(url_for('stud'))
					else:
						return 'Wrong Password'
				elif t_details:
					if password==t_details[0][0]:
						session['teacher']=t_details[0][1]
						return redirect(url_for('fac'))
					else:
						return 'Wrong Password'
				else:
					return 'Wrong Email'
	return render_template('sin.html',form=form)
	
@app.route('/sout_s')
def sout_s():
	session.pop('student',None)
	return redirect(url_for('sin'))

@app.route('/sout_t')
def sout_t():
	session.pop('teacher',None)
	return redirect(url_for('sin'))
			
@app.route('/sup_s')
def sup_s():
	if 'student' in session or 'teacher' in session:
		return 'Bye'
	else:
		return render_template('s_sup.html')

@app.route('/sup_comp_s',methods=['POST'])
def sup_comp_s():
	roll=request.form['text']
	with db:
		cur.execute('select * from s_login where roll=%s',(roll,))
		sup_data=cur.fetchall()
	pass_send_s(sup_data[0][2],url_for('passw',mailid=sup_data[0][2],passw=sup_data[0][5]))
	return render_template('sup_comp_s.html')
		
@app.route('/sup_disp_s')
def sup_disp_s():
	roll=request.args.get('roll',0)
	with db:
		cur.execute('select * from s_login where roll=%s and active=0',(roll,))
		sup_s_dispdata=cur.fetchall()
	return jsonify(sup_s_dispdata=sup_s_dispdata)

@app.route('/sup_t')
def sup_t():
	if 'student' in session or 'teacher' in session:
		return 'Bye'
	else:
		return render_template('t_sup.html')
		
@app.route('/sup_comp_t',methods=['POST'])
def sup_comp_t():
	empid=request.form['emp_id']
	with db:
		cur.execute('select * from t_login where empid=%s',(empid,))
		sup_data=cur.fetchall()
	pass_send_t(sup_data[0][2],url_for('passw',passw=sup_data[0][4],mailid=sup_data[0][2]))
	return render_template('sup_comp_t.html')
	
@app.route('/sup_disp_t')
def sup_disp_t():
	empid=request.args.get('empid',0)
	with db:
		cur.execute('select * from t_login where empid=%s and active=0',(empid,))
		sup_t_dispdata=cur.fetchall()
	return jsonify(sup_t_dispdata=sup_t_dispdata)
	
@app.route('/passw')	
def passw():
	if 'student' in session or 'teacher' in session:
		return 'Bye'
	else:
		passhash=request.args.get('passw')
		mailid=request.args.get('mailid')
	with db:
		cur.execute('select * from s_login where s_email=%s and s_pass=%s',(mailid,passhash))
		sdata=cur.fetchall()
		if sdata:
			return render_template('pass_set_s.html',mailid=mailid)
		else:
			cur.execute('select * from t_login where e_email=%s and e_pass=%s',(mailid,passhash))
			edata=cur.fetchall()
			if edata:
				return render_template('pass_set_t.html',mailid=mailid)
	return redirect(url_for('sin'))

@app.route('/pass_set_s',methods=['POST'])
def pass_set_s():
	email=request.form['mailid']
	password=request.form['pass']
	password=hashlib.md5(password).hexdigest()
	with db:
		cur.execute('update s_login set s_pass=%s and active=1 where s_email=%s',(password,email))
		return render_template('pass_conf_s.html')
		
@app.route('/pass_set_t',methods=['POST'])
def pass_set_t():
	email=request.form['mailid']
	password=request.form['pass']
	password=hashlib.md5(password).hexdigest()
	with db:
		cur.execute('update t_login set e_pass=%s and active=1 where e_email=%s',(password,email))
		return render_template('pass_conf_t.html')
		
@app.route('/fac')
def fac():
	if 'teacher' in session:
		with db:
			cur.execute('select * from subject where empid=%s',(session['teacher'],))
			courses=cur.fetchall()
		return render_template('faculty.html',courses=courses)
	return redirect(url_for('sin'))	
		
@app.route('/fac_course',methods=['GET','POST'])
def fac_course():
	if 'teacher' in session:
		course_id=request.args.get('course');
		if course_id:
			with db:
				cur.execute('select * from subject where empid=%s and course_id=%s',(session['teacher'],course_id))
				return render_template('faculty_course.html',course=cur.fetchall())
		return redirect(url_for('fac'))		
	else:
		return redirect(url_for('sin'))

@app.route('/add_new_course')
def index():
    if 'teacher' in session:
        with db:
        	cur.execute('select course_name from course')
        	courses=list(cur.fetchall())
        	course=[courses[i][0] for i in range(len(courses))]

        	cur.execute('select distinct dept from t_login')
        	dept=list(cur.fetchall())
        	depts=[dept[i][0] for i in range(len(dept))]

        years=['1','2','3','4','5']
        return render_template("add_new_course.html",years=years,depts=depts,course=course)
    else:
		return redirect(url_for('sin'))

@app.route('/ins',methods=['POST'])
def ins():
    if 'teacher' in session:
        course_id=request.form['course']
        dept1=request.form['dept1']
        dept2=request.form['dept2']
        dept3=request.form['dept3']
        year1=str(request.form['year1'])
        year2=str(request.form['year2'])
        year3=str(request.form['year3'])

        with db:
            cur.execute("insert into subject values('','0',%s,%s,'1')",(course_id,session['teacher'],))
            cur.execute("select sno from subject where course_id=%s",(course_id,))
            l=list(cur.fetchall())
            llink=str(l[0][0])
            cur.execute("update subject set link=%s where course_id=%s",(llink,course_id,))

            if(dept1!='Select Dept.'and year1!='Select Year'):
                cur.execute('select roll from s_login where branch=%s and year=%s',(dept1,year1,))
                roll=list(cur.fetchall())
                for i in range(len(roll)):
                    cur.execute('insert into subdata(link,roll) values(%s,%s)',(llink,roll[i][0],))

            if(dept2!='Select Dept.'and year2!='Select Year'):
                cur.execute('select roll from s_login where branch=%s and year=%s',(dept2,year2,))
                rol=list(cur.fetchall())
                for i in range(len(rol)):
                    cur.execute('insert into subdata(link,roll) values(%s,%s)',(llink,rol[i][0],))

            if(dept3!='Select Dept.' and year3!='Select Year'):
                cur.execute('select roll from s_login where branch=%s and year=%s',(dept3,year3,))
                ro=list(cur.fetchall())
                for i in range(len(ro)):
                    cur.execute('insert into subdata(link,roll) values(%s,%s)',(llink,ro[i][0],))

        return "Added"
    else:
        return redirect(url_for('sin'))

@app.route('/fac_marks')
def fac_marks():
	if 'teacher' in session:
		course_id=request.args.get('course')
		if course_id:
			with db:
				cur.execute('select * from subject where empid=%s and course_id=%s',(session['teacher'],course_id))
				course=cur.fetchall()
				cur.execute('select * from marks where link=%s',(course[0][1],))
				course_col=cur.fetchall()
				cur.execute('select roll from subdata where link=%s',(course[0][1],))
				students=cur.fetchall()
				return render_template('faculty_marks.html',course=course,course_col=course_col,students=students)
		return redirect(url_for('fac'))
	else:
		return redirect(url_for('sin'))

@app.route('/fac_add_marks',methods=['GET','POST'])
def fac_add_marks():
	if 'teacher' in session:
		if request.method=='POST':
			col=request.form['col']
			link=request.form['link']
			name=request.form['name']
			max_marks=request.form['max_marks']
			weightage=request.form['weightage']
			with db:
				cur.execute('insert into marks values(%s,%s,%s,%s,%s)',(link,col,name,max_marks,weightage))
				cur.execute('select course_id from subject where link=%s',(link,))
				return redirect(url_for('fac_marks',course=cur.fetchall()[0][0]))
		else:	
			course_id=request.args.get('course');
			if course_id:
				with db:
					cur.execute('select * from subject where empid=%s and course_id=%s',(session['teacher'],course_id))
					course=cur.fetchall()
					cur.execute('select * from marks where link=%s',(course[0][1],))
					column_data=cur.fetchall()
					if len(column_data)<12:
						return render_template('faculty_add_marks.html',course=course,column_data=column_data)
					else:
						return 'All 12 Column Filled'
			return redirect(url_for('fac'))
	else:
		return redirect(url_for('sin'))
		
@app.route('/fac_insert_marks',methods=['POST'])
def fac_insert_marks():
	if 'teacher' in session:
		link=request.form['link']
		test=request.form['test']
		start=request.form['start']
		end=request.form['end']
		with db:
			cur.execute('select col_no from marks where col_name=%s and link=%s',(test,link))
			sql='select roll,m_col_'+str(cur.fetchall()[0][0])+' from subdata where link=%s and roll between %s and %s' 
			cur.execute(sql,(link,start,end))
			marks_data=list(cur.fetchall())
			for i in range(len(marks_data)):
				marks_data[i]=list(marks_data[i])
				cur.execute('select s_name from s_login where roll=%s',(marks_data[i][0],))
				marks_data[i].append(cur.fetchall()[0][0])
			return render_template('faculty_insert_marks.html',marks_data=marks_data,link=link,test=test)
	return redirect(url_for('sin'))		

@app.route('/fac_update_marks',methods=['POST'])
def fac_update_marks():
	if 'teacher' in session:
		f=request.form
		marks={}
		for key in f.keys():
			for value in f.getlist(key):
				marks[key]=value
		link=marks['link']
		test=marks['test']
		del marks['link']	
		del marks['test']
		with db:
			cur.execute('select col_no from marks where col_name=%s and link=%s',(test,link))
			sql='update subdata set m_col_'+str(cur.fetchall()[0][0])+'=%s where roll=%s and link=%s'
			for i in marks:
				cur.execute(sql,(marks[i],i,link))
			cur.execute('select course_id from subject where link=%s',(link,))
			return redirect(url_for('fac_marks',course=cur.fetchall()[0][0]))	
	return redirect(url_for('sin'))

@app.route('/fac_attendance')
def fac_attendance():
	if 'teacher' in session:
		course_id=request.args.get('course')
		if course_id:
			with db:
				cur.execute('select * from subject where empid=%s and course_id=%s',(session['teacher'],course_id))
				course=cur.fetchall()
				cur.execute('select * from attendance where link=%s',(course[0][1],))
				course_col=cur.fetchall()
				cur.execute('select roll from subdata where link=%s',(course[0][1],))
				students=cur.fetchall()
				return render_template('faculty_attendance.html',course=course,course_col=course_col,students=students)
		return redirect(url_for('fac'))		
	return redirect(url_for('sin'))

@app.route('/fac_add_attendance',methods=['GET','POST'])
def fac_add_attendance():
	if 'teacher' in session:
		if request.method=='POST':
			col=request.form['col']
			link=request.form['link']
			name=request.form['name']
			max_attendance=request.form['max_attendance']
			with db:
				cur.execute('insert into attendance values(%s,%s,%s,%s)',(link,col,name,max_attendance))
				cur.execute('select course_id from subject where link=%s',(link,))
				return redirect(url_for('fac_attendance',course=cur.fetchall()[0][0]))
		else:	
			course_id=request.args.get('course');
			if course_id:
				with db:
					cur.execute('select * from subject where empid=%s and course_id=%s',(session['teacher'],course_id))
					course=cur.fetchall()
					cur.execute('select * from attendance where link=%s',(course[0][1],))
					column_data=cur.fetchall()
					if len(column_data)<8:
						return render_template('faculty_add_attendance.html',course=course,column_data=column_data)
					else:
						return 'All 8 Column Filled'
			return redirect(url_for('fac'))
	else:
		return redirect(url_for('sin'))
		
@app.route('/fac_insert_attendance',methods=['POST'])
def fac_insert_attendance():
	if 'teacher' in session:
		link=request.form['link']
		attendance=request.form['attendance']
		start=request.form['start']
		end=request.form['end']
		with db:
			cur.execute('select col_no from attendance where col_name=%s and link=%s',(attendance,link))
			sql='select roll,a_col_'+str(cur.fetchall()[0][0])+' from subdata where link=%s and roll between %s and %s' 
			cur.execute(sql,(link,start,end))
			attendance_data=list(cur.fetchall())
			for i in range(len(attendance_data)):
				attendance_data[i]=list(attendance_data[i])
				cur.execute('select s_name from s_login where roll=%s',(attendance_data[i][0],))
				attendance_data[i].append(cur.fetchall()[0][0])
			return render_template('faculty_insert_attendance.html',attendance_data=attendance_data,link=link,attendance=attendance)
	return redirect(url_for('sin'))		

@app.route('/fac_update_attendance',methods=['POST'])
def fac_update_attendance():
	if 'teacher' in session:
		f=request.form
		attendance={}
		for key in f.keys():
			for value in f.getlist(key):
				attendance[key]=value
		link=attendance['link']
		attend=attendance['attendance']
		del attendance['link']	
		del attendance['attendance']
		with db:
			cur.execute('select col_no from attendance where col_name=%s and link=%s',(attend,link))
			sql='update subdata set a_col_'+str(cur.fetchall()[0][0])+'=%s where roll=%s and link=%s'
			for i in attendance:
				cur.execute(sql,(attendance[i],i,link))
			cur.execute('select course_id from subject where link=%s',(link,))
			return redirect(url_for('fac_attendance',course=cur.fetchall()[0][0]))	
	return redirect(url_for('sin'))	
		
@app.route('/stud')	
def stud():
	if 'student' in session:
		with db:
			roll=session['student']
			cur.execute('select b.course_id from subdata a,subject b where a.roll=%s and a.link=b.link',(roll,))
			courses=cur.fetchall()[0]
		return render_template('student_login.html',courses=courses)
	return redirect(url_for('sin'))		
	
@app.route('/student_view',methods=['POST'])
def student_view():
	if 'student' in session:
		course=request.form['courses']
		with db:
			roll=session['student']
			cur.execute('select c.col_name from subject a,subdata b,marks c where b.link=a.link and b.roll=%s and a.link=c.link and a.course_id=%s ',(roll,course))
			headings1=cur.fetchall()
			cur.execute('select d.col_name from subject a,subdata b,attendance d where a.course_id=%s and b.link=a.link and b.roll=%s and a.link=d.link ',(course,roll))
			headings2=cur.fetchall()
			headings_temp=headings1+headings2
			headings=headings_temp[0]
			#cur.execute('select m_col_1 from subject a,subdata b where m_col_1 is not NULL and a.link=a.course_id and b.link=a.link and b.roll=%s,(roll,) UNION select m_col_2 from subject a,subdata b where m_col_1 is not NULL and a.link=a.course_id and b.link=a.link and b.roll=%s,(roll,) UNION select m_col_3 from subject a,subdata b where m_col_1 is not NULL and a.link=a.course_id and b.link=a.link and b.roll=%s,(roll,) UNION select m_col_4 from subject a,subdata b where m_col_1 is not NULL and a.link=a.course_id and b.link=a.link and b.roll=%s,(roll,) UNION select m_col_5 from subject a,subdata b where m_col_1 is not NULL and a.link=a.course_id and b.link=a.link and b.roll=%s,(roll,) UNION select m_col_6 from subject a,subdata b where m_col_1 is not NULL and a.link=a.course_id and b.link=a.link and b.roll=%s,(roll,) UNION select m_col_7 from subject a,subdata b where m_col_1 is not NULL and a.link=a.course_id and b.link=a.link and b.roll=%s,(roll,) UNION select a_col_1 from subject a,subdata b where m_col_1 is not NULL and a.link=a.course_id and b.link=a.link and b.roll=%s,(roll,) UNION select a_col_2 from subject a,subdata b where m_col_1 is not NULL and a.link=a.course_id and b.link=a.link and b.roll=%s,(roll,) UNION select a_col_3 from subject a,subdata b where m_col_1 is not NULL and a.link=a.course_id and b.link=a.link and b.roll=%s,(roll,) UNION select a_col_4 from subject a,subdata b where m_col_1 is not NULL and a.link=a.course_id and b.link=a.link and b.roll=%s,(roll,) UNION select a_col_5 from subject a,subdata b where m_col_1 is not NULL and a.link=a.course_id and b.link=a.link and b.roll=%s,(roll,) UNION select a_col_6 from subject a,subdata b where m_col_1 is not NULL and a.link=a.course_id and b.link=a.link and b.roll=%s(roll,) UNION select a_col_7 from subject a,subdata b where m_col_1 is not NULL and a.link=a.course_id and b.link=a.link and b.roll=%s',(roll,))
			#data=cur.fetchall()[0]
		return render_template('student_view.html',roll=roll,list=headings,)	
	return redirect(url_for('sin'))	
			
if __name__=='__main__':
	app.run(debug=True)