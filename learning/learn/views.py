from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import datetime
import pytz
from . models import *
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from . decorators import logged_inn

# Index Home Functions

def home(request):
    sdd = Subject.objects.all()
    sd = []
    for i in sdd:
        if i.Subject_title not in sd:
            sd.append(i.Subject_title)
    return render(request, 'sama.html',{'sd': sd})

def news(request):
    page = requests.get('https://www.indiatoday.in/education-today')
    soup = BeautifulSoup(page.content,'html.parser')
    week = soup.find(class_ = 'special-top-news')
    wm = week.find(class_ = 'itg-listing')
    w = wm.find_all('a')
    ww = []
    for x in w:
        ww.append(x.get_text())
    x = datetime.datetime.now()
    return render(request,'news.html',{'ww':ww,'x':x})

def about_page(request):
    df = Registration.objects.get(User_role='admin')
    gt = Registration.objects.filter(User_role='teacher')
    return render(request, 'about_page.html', {'df': df, 'gt': gt})

def add_blog(request):
    if request.method == 'POST':
        nam = request.POST.get('nam')
        c_b = request.POST.get('c_b')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        date1 = request.POST.get('date1')
        b = Blogs()
        b.Name = nam
        b.Blog_content = c_b
        b.Image = photo
        b.Date_blog = date1
        b.Approval_status = 'Rejected'
        b.save()
        messages.success(request, 'Blog added successfully. Please wait for approval')
        return render(request, 'sama.html')
    return render(request,'add_blog.html')

def display_blog(request):
    dc = Blogs.objects.filter(Approval_status='Approved')
    return render(request, 'display_blog.html', {'dc': dc})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        reg = Messages()
        reg.Category = 'guest'
        reg.Name = name
        reg.From_email = email
        reg.To_email = 'admin@gmail.com'
        reg.Message_content = subject
        reg.save()
        messages.success(request, 'You have successfully registered your comment')
        return render(request, 'sama.html')
    else:
        return render(request, 'contact.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            b = User.objects.get(username=username)
            cd = Registration.objects.filter(user=b)
            for i in cd:
                if i.User_role == 'admin':
                    request.session['logg'] = i.id
                    return render(request, 'admin_home.html')
                elif i.User_role == 'student':
                    request.session['logg'] = i.id
                    return render(request, 'student_home.html')
                elif i.User_role == 'teacher':
                    request.session['logg'] = i.id
                    return render(request, 'teacher_home.html')
                else:
                    messages.info(request, 'Your account Blocked')
                    return render(request, 'login.html')

            auth.login(request, user)
        else:
            messages.info(request, 'invalid credentials')
            return render(request, 'sama.html')

    return render(request, 'login.html')


def register_teacher(request):
        if request.method == 'POST':
            x = datetime.datetime.now()
            y = x.strftime("%Y-%m-%d")
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            user_name = request.POST.get('user_name')
            psw = request.POST.get('psw')
            qual = request.POST.get('qual')
            intro = request.POST.get('intro')
            photo = request.FILES['photo']
            enrol = request.POST.get('enrol')
            avg_rev = request.POST.get('avg_rev')
            tot_rev = request.POST.get('tot_rev')
            teach = request.POST.get('teacher')
            reg1 = Registration.objects.all()
            for i in reg1:
                if i.Email == email:
                    messages.success(request, 'User already exists')
                    return render(request, 'sama.html')

            if User.objects.filter(username=user_name).exists():
                messages.success(request, 'Teacher already exists')
                return render(request, 'register_teacher.html')
            usr = User.objects.create_user(username=user_name, password=psw, email=email, first_name=first_name,
                                           last_name=last_name)
            usr.save()
            t = Registration()
            t.First_name = first_name
            t.Last_name = last_name
            t.Email = email
            t.Password = psw
            t.Registration_date = y
            t.Qualification = qual
            t.Introduction_brief = intro
            t.Image = photo
            t.Num_of_enrolled_students = enrol
            t.Average_review_rating = avg_rev
            t.Num_of_reviews = tot_rev
            t.About_website = 'Nil'
            t.User_role = teach
            t.user = usr
            t.save()
            messages.success(request, 'You have successfully registered')
            return render(request, 'sama.html')
        else:
            return render(request, 'register_teacher.html')

def register_student(request):
        if request.method == 'POST':
            x = datetime.datetime.now()
            y = x.strftime("%Y-%m-%d")
            typ = request.POST.get('student')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            user_name = request.POST.get('user_name')
            psw = request.POST.get('psw')
            photo = request.FILES['photo']
            mgn = Registration.objects.all()
            for w in mgn:
                if w.Email == email and w.User_role == 'student':
                    messages.success(request, 'You have already registered..Please login')
                    return render(request, 'login.html')
            if User.objects.filter(username = user_name).exists():
                messages.success(request, 'Student already exists')
                return render(request, 'register_student.html')
            usr = User.objects.create_user(username=user_name, password=psw, email=email, first_name=first_name, last_name=last_name )
            usr.save()
            fs = FileSystemStorage()
            fs.save(photo.name, photo)
            reg = Registration()
            reg.First_name = first_name
            reg.Last_name = last_name
            reg.Email = email
            reg.Password = psw
            reg.Registration_date = y
            reg.Qualification = 'Nil'
            reg.Introduction_brief = 'Nil'
            reg.Image = photo
            reg.Num_of_enrolled_students = 0
            reg.Average_review_rating = 0
            reg.Num_of_reviews = 0
            reg.About_website = 'Nil'
            reg.User_role = typ
            reg.user = usr
            reg.save()
            messages.success(request, 'You have successfully registered')
            return render(request, 'sama.html')
        else:
            return render(request, 'register_student.html')


def register_admin(request):
    if request.method == 'POST':
        lk = Registration.objects.all()
        for t in lk:
            if t.User_role == 'admin':
                messages.success(request, 'You are not allowed to be registered as admin')
                return render(request, 'sama.html')
        x = datetime.datetime.now()
        z = x.strftime("%Y-%m-%d")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        user_name = request.POST.get('user_name')
        psw = request.POST.get('psw')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        admin = request.POST.get('adminn1')
        reg1 = Registration.objects.all()
        for i in reg1:
            if i.Email == email:
                messages.success(request, 'User already exists')
                return render(request, 'sama.html')
        if User.objects.filter(username=user_name).exists():
            messages.success(request, 'Admin already exists')
            return render(request, 'register_admin.html')
        usr = User.objects.create_user(username=user_name, password=psw, email=email, first_name=first_name,
                                       last_name=last_name)
        usr.save()
        t = Registration()
        t.First_name = first_name
        t.Introduction_brief = 'Nil'
        t.Last_name = last_name
        t.Email = email
        t.Password = psw
        t.Registration_date = z
        t.Qualification = 'Nil'
        t.Image = photo
        t.Num_of_enrolled_students = 0
        t.Average_review_rating = 0
        t.Num_of_reviews = 0
        t.About_website = 'Nil'
        t.User_role = admin
        t.user = usr
        t.save()
        messages.success(request, 'You have successfully registered as admin')
        return render(request, 'sama.html')
    else:
        return render(request, 'register_admin.html')

def admin(request):
    return render(request, 'admin.html')

def footer(request):
    return render(request, 'footer.html')

@logged_inn
def admin_home(request):
    return render(request, 'admin_home.html')

def student_home(request):
    return render(request, 'student_home.html')

def teacher_home(request):
    return render(request, 'teacher_home.html')

def logout(request):
    del request.session['logg']
    auth.logout(request)
    sdd = Subject.objects.all()
    sd = []
    for i in sdd:
        if i.Subject_title not in sd:
            sd.append(i.Subject_title)
    if 'logg' in request.session:
        del request.session['logg']
        return render(request, 'sama.html', {'sd': sd})
    return render(request, 'sama.html', {'sd': sd})

#Admin Home Functions

def admin_profile(request):
    dc = Registration.objects.get(id=request.session['logg'])
    kk = User.objects.get(username= dc.user)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        kk.first_name = first_name
        kk.last_name = last_name
        kk.email = email
        kk.save()

        dc.First_name = first_name
        dc.Last_name = last_name
        dc.Email = email
        dc.save()
        messages.success(request, 'Edit data successfully saved')
        return render(request, 'admin_home.html')

    else:
        return render(request, 'admin_profile.html', {'dc': dc})

def blogs_admin(request):
    dc = Blogs.objects.all()
    return render(request, 'blogs_admin.html', {'dc': dc})

def admin_approve(request, apr):
    d = Blogs.objects.get(id = apr)
    d.Approval_status = 'Approved'
    d.save()
    dc = Blogs.objects.all()
    return render(request, 'blogs_admin.html', {'dc': dc})

def admin_reject(request, rej):
    d = Blogs.objects.get(id = rej)
    d.Approval_status = 'Rejected'
    d.save()
    dc = Blogs.objects.all()
    return render(request, 'blogs_admin.html', {'dc': dc})

def admin_delete(request, delt):
    Blogs.objects.get(id = delt).delete()
    dc = Blogs.objects.all()
    return render(request, 'blogs_admin.html', {'dc': dc})

def upload_cer(request):
    ss = Registration.objects.filter(User_role='student')
    bc = Enrollment.objects.all()
    kk = []
    kj = []
    ks = []
    ka = []
    kb = []
    kc = []
    for i in ss:
        for t in bc:
            if i.Email == t.Student_email:
                kk.append(i.First_name)
                kj.append(i.Last_name)
                ks.append(i.Email)
                ka.append(t.Subject_name)
                kb.append(t.Course_name)
                kc.append(t.Teacher_email)
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        gg = stu_id.split(";")
        hu = gg[0]
        tq = gg[1]
        tp = gg[2]
        wx = gg[3]
        cert = request.FILES['cert']
        fs = FileSystemStorage()
        fs.save(cert.name, cert)
        try:
            cc = Enrollment.objects.get(Student_email=hu, Subject_name=tq, Course_name=tp, Teacher_email=wx)
        except:
            messages.success(request, 'Please delete old certificates of student')
            return render(request, "admin_home.html")
        cc.Certificate = cert
        cc.save()
        messages.success(request, 'Certificate uploaded successfully')
        return render(request, "admin_home.html")
    ms = zip(kk, kj, ks, ka, kb, kc)
    return render(request, 'upload_cer.html', {'ms': ms})

def delete_cer(request):
    df = Enrollment.objects.all()
    return render(request, 'delete_cer.html', {'df': df})

def delete_certificate(request, id):
    k = Enrollment.objects.get(id=id).delete()
    df = Enrollment.objects.filter(Certificate__isnull=False)
    messages.success(request, 'Deleted certificate')
    return render(request, 'del_cer.html', {'df': df})

def about_content(request):
    if request.method == 'POST':
        about_web = request.POST.get('about_web')
        dc = Registration.objects.get(User_role = 'admin')
        dc.About_website = about_web
        dc.save()
        messages.success(request, 'Data successfully saved as About website')
        return render(request, 'admin_home.html')
    else:
        return render(request, 'about_content.html')

def block(request):
    t_reg = Registration.objects.filter(Q(User_role="teacher") | Q(User_role="teacher_blocked"))
    s_reg = Registration.objects.filter(Q(User_role="student") | Q(User_role="student_blocked"))
    return render(request, 'block.html', {'t_reg': t_reg, 's_reg': s_reg})

def t_allow(request, talw):
    d = Registration.objects.get(id = talw)
    d.User_role = 'teacher'
    d.save()
    t_reg = Registration.objects.filter(Q(User_role="teacher") | Q(User_role="teacher_blocked"))
    s_reg = Registration.objects.filter(Q(User_role="student") | Q(User_role="student_blocked"))
    return render(request, 'block.html', {'t_reg': t_reg, 's_reg': s_reg})

def t_block(request, tblc):
    d = Registration.objects.get(id=tblc)
    d.User_role = 'teacher_blocked'
    d.save()
    t_reg = Registration.objects.filter(Q(User_role="teacher") | Q(User_role="teacher_blocked"))
    s_reg = Registration.objects.filter(Q(User_role="student") | Q(User_role="student_blocked"))
    return render(request, 'block.html', {'t_reg': t_reg, 's_reg': s_reg})

def s_allow(request, salw):
    d = Registration.objects.get(id=salw)
    d.User_role = 'student'
    d.save()
    t_reg = Registration.objects.filter(Q(User_role="teacher") | Q(User_role="teacher_blocked"))
    s_reg = Registration.objects.filter(Q(User_role="student") | Q(User_role="student_blocked"))
    return render(request, 'block.html', {'t_reg': t_reg, 's_reg': s_reg})

def s_block(request, sblc):
    d = Registration.objects.get(id=sblc)
    d.User_role = 'student_blocked'
    d.save()
    t_reg = Registration.objects.filter(Q(User_role="teacher") | Q(User_role="teacher_blocked"))
    s_reg = Registration.objects.filter(Q(User_role="student") | Q(User_role="student_blocked"))
    return render(request, 'block.html', {'t_reg': t_reg, 's_reg': s_reg})

def feedback(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'feedback.html', {'feedbacks': feedbacks})

def feed_delete(request,feed):
    Feedback.objects.get(id = feed).delete()
    messages.success(request, 'Deleted Successfully')
    feedbacks = Feedback.objects.all()
    return render(request, 'feedback.html', {'feedbacks': feedbacks})

def pass_req(request):
    return render(request, 'pass_req.html')

def member_messages(request):
    p = Registration.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email)
    return render(request, 'member_messages.html', {'bb': bb})

def del_msg_admin(request, id):
    Messages.objects.get(id = id).delete()
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email)
    messages.success(request, 'Message deleted successfully')
    return render(request,'member_messages.html',{'bb':bb})

def reply_msg_admin(request, id):
    pa = Messages.objects.get(id=id)
    p = Registration.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email)
    if request.method == 'POST':
        f_email = request.POST.get('f_email')
        to_email = request.POST.get('to_email')
        msg_cont = request.POST.get('msg_cont')
        pa1 = Messages()
        pa1.Category = p.User_role
        pa1.From_email = to_email
        pa1.To_email = f_email
        pa1.Message_content = msg_cont
        pa1.save()
        messages.success(request, 'Message reply successful')
        return render(request, 'member_messages.html', {'bb': bb})
    return render(request, 'reply_msg_admin.html', {'pa': pa})

def sent_msg_admin(request):
    kk = Registration.objects.all()
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    if request.method == 'POST':
        to_em = request.POST.get('to_em')
        ddp = str(to_em)
        gg = ddp.split()
        pnm = gg[0]
        msg_cont = request.POST.get('msg_cont')
        nm = Messages()
        nm.Category = p.User_role
        kkp = Registration.objects.get(id = request.session['logg'])
        nm.From_email = kkp.Email
        nm.To_email = pnm
        nm.Message_content = msg_cont
        nm.save()
        messages.success(request, 'Message sent successfully')
        return render(request, 'member_messages.html', {'bb': bb})
    return render(request,'sent_msg_admin.html',{'kk':kk})


def guest_messages(request):
    bb = Messages.objects.filter(Category='guest')
    return render(request, 'guest_messages.html', {'bb': bb})
def delete_g_msg(request, id):
    Messages.objects.get(id = id).delete()
    bb = Messages.objects.filter(Category='guest')
    return render(request, 'guest_messages.html', {'bb': bb})

def chapter_add(request):
    dd = Subject.objects.all()
    gt = Registration.objects.all()
    sub_nam = []
    cou_nam = []
    ch_tit = []
    n_o_a = []
    tea_em = []
    tea_fn = []
    tea_ln = []
    c_id = []
    for i in dd:
        sub_nam.append(i.Subject_title)
        cou_nam.append(i.Course_title)
        ch_tit.append(i.Chapter_title)
        n_o_a.append(i.Num_of_assignments)
        c_id.append(i.id)
        for t in gt:
            if t == i.Sub_reg:
                tea_em.append(t.Email)
                tea_fn.append(t.First_name)
                tea_ln.append(t.Last_name)
    lenn = len(sub_nam)
    for z in range(lenn):
        kpk = len(sub_nam)
        r = int(z)
        r += 1
        try:
            a = sub_nam[z]
        except:
            break
        b = cou_nam[z]
        c = tea_em[z]
        d = ch_tit[z]
        for k in range(lenn):
            if int(r) >= int(kpk):
                continue
            try:
                if sub_nam[r] == a and cou_nam[r] == b and tea_em[r] == c and ch_tit[r] == d:
                    del sub_nam[r]
                    del cou_nam[r]
                    del ch_tit[r]
                    del n_o_a[r]
                    del tea_em[r]
                    del tea_fn[r]
                    del tea_ln[r]
                    del c_id[r]
                    r -= 1
                r += 1
            except:
                break
    grg1 = zip(sub_nam, cou_nam, ch_tit, n_o_a, tea_em, tea_fn, tea_ln, c_id)
    return render(request, 'chapter_add.html', {'grg1': grg1})

def edit_chapter_ad(request, id, idd, idt, idk, pkm):
    pkm = int(pkm)
    id = str(id)
    idd = str(idd)
    idt = str(idt)
    idk = str(idk)
    ftf = Registration.objects.get(Email=idk)
    gh1 = Subject.objects.filter(Subject_title=id, Course_title=idd, Chapter_title = idt, Sub_reg=ftf)
    gh = Subject.objects.get(id=pkm)

    if request.method == 'POST':
        sub = request.POST.get('sub')
        cou = request.POST.get('cou')
        c_tt = request.POST.get('c_tt')
        n_s = request.POST.get('n_s')
        for k in gh1:
            k.Subject_title = sub
            k.Course_title = cou
            k.Chapter_title = c_tt
            k.Num_of_assignments = n_s
            k.save()

        dd = Subject.objects.all()
        gt = Registration.objects.all()
        sub_nam = []
        cou_nam = []
        ch_tit = []
        n_o_a = []
        tea_em = []
        tea_fn = []
        tea_ln = []
        c_id = []
        for i in dd:
            sub_nam.append(i.Subject_title)
            cou_nam.append(i.Course_title)
            ch_tit.append(i.Chapter_title)
            n_o_a.append(i.Num_of_assignments)
            c_id.append(i.id)
            for t in gt:
                if t == i.Sub_reg:
                    tea_em.append(t.Email)
                    tea_fn.append(t.First_name)
                    tea_ln.append(t.Last_name)
        lenn = len(sub_nam)
        for z in range(lenn):
            kpk = len(sub_nam)
            r = int(z)
            r += 1
            try:
                a = sub_nam[z]
            except:
                break
            b = cou_nam[z]
            c = tea_em[z]
            d = ch_tit[z]
            for k in range(lenn):
                if int(r) >= int(kpk):
                    continue
                try:
                    if sub_nam[r] == a and cou_nam[r] == b and tea_em[r] == c and ch_tit[r] == d:
                        del sub_nam[r]
                        del cou_nam[r]
                        del ch_tit[r]
                        del n_o_a[r]
                        del tea_em[r]
                        del tea_fn[r]
                        del tea_ln[r]
                        del c_id[r]
                        r -= 1
                    r += 1
                except:
                    break
        grg1 = zip(sub_nam, cou_nam, ch_tit, n_o_a, tea_em, tea_fn, tea_ln, c_id)
        messages.success(request, 'Chapter edited successfully')
        return render(request, 'chapter_add.html', {'grg1': grg1})
    return render(request, 'edit_chapter_ad.html', {'gh': gh, 'ftf': ftf})

def delete_chapter_ad(request, id, idd, idt, idk, pkm):
    pkm = int(pkm)
    id = str(id)
    idd = str(idd)
    idt = str(idt)
    idk = str(idk)
    ftf = Registration.objects.get(Email=idk)
    Subject.objects.filter(Subject_title=id, Course_title=idd, Chapter_title=idt, Sub_reg=ftf).delete()

    dd = Subject.objects.all()
    gt = Registration.objects.all()
    sub_nam = []
    cou_nam = []
    ch_tit = []
    n_o_a = []
    n_o_v = []
    n_o_p = []
    n_o_i = []
    tea_em = []
    tea_fn = []
    tea_ln = []
    c_id = []
    for i in dd:
        sub_nam.append(i.Subject_title)
        cou_nam.append(i.Course_title)
        ch_tit.append(i.Chapter_title)
        n_o_a.append(i.Num_of_assignments)
        n_o_v.append(0)
        n_o_i.append(0)
        n_o_p.append(0)
        c_id.append(i.id)
        for t in gt:
            if t == i.Sub_reg:
                tea_em.append(t.Email)
                tea_fn.append(t.First_name)
                tea_ln.append(t.Last_name)
    lenn = len(sub_nam)
    for z in range(lenn):
        kpk = len(sub_nam)
        r = int(z)
        r += 1
        try:
            a = sub_nam[z]
        except:
            break
        b = cou_nam[z]
        c = tea_em[z]
        d = ch_tit[z]
        for k in range(lenn):
            if int(r) >= int(kpk):
                continue
            try:
                if sub_nam[r] == a and cou_nam[r] == b and tea_em[r] == c and ch_tit[r] == d:
                    del sub_nam[r]
                    del cou_nam[r]
                    del ch_tit[r]
                    del n_o_a[r]
                    del tea_em[r]
                    del tea_fn[r]
                    del tea_ln[r]
                    del c_id[r]
                    r -= 1
                r += 1
            except:
                break
    grg1 = zip(sub_nam, cou_nam, ch_tit, n_o_a, tea_em, tea_fn, tea_ln, c_id)
    messages.success(request, 'Chapter deleted successfully')
    return render(request, 'chapter_add.html', {'grg1': grg1})



def sub_edit_admin(request, h):
    dc = Subject.objects.get(id = h)
    if request.method == 'POST':
        sub_tit = request.POST.get('sub_tit')
        cou_tit = request.POST.get('cou_tit')
        #rt = Subject.objects.filter(Sub_reg=request.session['logg'])
        c_brief = request.POST.get('c_brief')
        c_dur = request.POST.get('c_dur')
        n_chapt = request.POST.get('n_chapt')
        c_fee = request.POST.get('c_fee')
        lang = request.POST.get('lang')

        """
        for u in rt:
            if u.Subject_title == sub_tit and u.Course_title == cou_tit:
                dd = Subject.objects.filter(Sub_reg=request.session['logg'])
                a = []
                b = []
                c = []
                d = []
                e = []
                f = []
                g = []
                h = []
                for i in dd:
                    if i.Course_title not in a:
                        a.append(i.Course_title)
                        b.append(i.Subject_title)
                        c.append(i.Course_brief)
                        d.append(i.Course_duration)
                        e.append(i.Num_of_chapters)
                        f.append(i.Course_fee)
                        g.append(i.Language)
                        h.append(i.id)
                hh = zip(a, b, c, d, e, f, g, h)
                messages.success(request, 'Subject Already Exists')
                return render(request, 'course.html', {'hh': hh})"""

        dc.Subject_title = sub_tit
        dc.Course_title = cou_tit
        dc.Course_brief = c_brief
        dc.Course_duration = c_dur
        dc.Num_of_chapters = n_chapt
        dc.Course_fee = c_fee
        dc.Language = lang
        dc.save()

        dd = Subject.objects.all()
        a = []
        b = []
        c = []
        d = []
        e = []
        f = []
        g = []
        h = []
        for i in dd:
            if i.Course_title not in a:
                a.append(i.Course_title)
                b.append(i.Subject_title)
                c.append(i.Course_brief)
                d.append(i.Course_duration)
                e.append(i.Num_of_chapters)
                f.append(i.Course_fee)
                g.append(i.Language)
                h.append(i.id)
        hh = zip(a, b, c, d, e, f, g, h)
        db = Registration.objects.get(id = request.session['logg'])
        if db.User_role == 'admin':
            dd = Subject.objects.all()
            a = []
            b = []
            c = []
            d = []
            e = []
            f = []
            g = []
            h = []
            for i in dd:
                if i.Course_title not in a:
                    a.append(i.Course_title)
                    b.append(i.Subject_title)
                    c.append(i.Course_brief)
                    d.append(i.Course_duration)
                    e.append(i.Num_of_chapters)
                    f.append(i.Course_fee)
                    g.append(i.Language)
                    h.append(i.id)
            hh = zip(a, b, c, d, e, f, g, h)
            messages.success(request, 'Subject Edited')
            return render(request, 'sub_view.html', {'hh': hh})

    return render(request, 'sub_edit_admin.html', {'dc': dc})


def sub_view(request):
    dd = Subject.objects.all()
    a = []
    b = []
    c = []
    d = []
    e = []
    f = []
    g = []
    h = []
    for i in dd:
        if i.Course_title not in a:
            a.append(i.Course_title)
            b.append(i.Subject_title)
            c.append(i.Course_brief)
            d.append(i.Course_duration)
            e.append(i.Num_of_chapters)
            f.append(i.Course_fee)
            g.append(i.Language)
            h.append(i.id)
    hh = zip(a, b, c, d, e, f, g, h)
    return render(request, 'sub_view.html', {'hh': hh})

def content_add(request):
    gt = Registration.objects.filter(User_role='teacher')
    dm = Subject.objects.all()
    return render(request, 'content_add.html', {'gt': gt, 'dm': dm})

def edit_content_ad(request, id):
    gh1 = Subject.objects.get(id=id)
    gt = Registration.objects.filter(User_role='teacher')
    dm = Subject.objects.all()
    if request.method == 'POST':
        sub = request.POST.get('sub')
        cou = request.POST.get('cou')
        c_n1 = request.POST.get('c_n')
        s = request.POST.get('s')
        time = request.POST.get('time')
        s1 = request.POST.get('s1')
        cont_typ = request.POST.get('cont_typ')
        textt = request.POST.get('textt')
        gh1.Subject_title = sub
        gh1.Course_title = cou
        gh1.Chapter_title = c_n1
        gh1.Chapter_text_content = textt
        if cont_typ == 1:
            gh1.Chapter_Content_type = 'Image'
        if cont_typ == 2:
            gh1.Chapter_Content_type = 'Text'
        if cont_typ == 3:
            gh1.Chapter_Content_type = 'Video'
        gh1.Chapter_Content_Is_mandatory  = s
        gh1.Chapter_Content_Time_required_in_sec  = time
        gh1.Chapter_Content_Is_open_for_free  = s1
        gh1.save()
        messages.success(request, 'Chapter content edited successfully')
        return render(request, 'content_add.html', {'gt':gt,'dm':dm})
    return render(request, 'edit_content_ad.html', {'gh1': gh1})

def delete_content_ad(request,id):
    Subject.objects.get(id=id).delete()
    gt = Registration.objects.filter(User_role='teacher')
    dm = Subject.objects.all()
    messages.success(request, 'Chapter content deleted successfully')
    return render(request, 'content_add.html', {'gt': gt, 'dm': dm})



#Teacher Home Functions

def teacher_profile(request):
    dc = Registration.objects.get(id=request.session['logg'])
    kk = User.objects.get(username = dc.user)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        qual = request.POST.get('qual')
        intro = request.POST.get('intro')

        kk.first_name = first_name
        kk.last_name = last_name
        kk.email = email
        kk.save()

        dc.First_name = first_name
        dc.Last_name = last_name
        dc.Email = email
        dc.Qualification = qual
        dc.Introduction_brief = intro
        dc.save()

        messages.success(request, 'Edit data successfully saved')
        return render(request, 'teacher_home.html')

    else:
        return render(request, 'teacher_profile.html', {'dc': dc})

def student_progress(request):
    vc = Registration.objects.get(id = request.session['logg'])
    hgh1 = Enrollment.objects.filter(Teacher_email = vc.Email)
    hgh = []
    for i in hgh1:
        if i.Student_email not in hgh:
            hgh.append(i.Student_email)
    dd = Learning_progress.objects.all()
    return render(request,'student_progress.html',{'dd': dd,'hgh': hgh})

def t_change_password(request):
    th = Registration.objects.get(id=request.session['logg'])
    if request.method == 'POST':
        new_pass = request.POST.get('pssw')
        old_pass = request.POST.get('pssw_old')
        email = request.POST.get('em')
        category = request.POST.get('usr')
        name = request.POST.get('nam')

        passwords = make_password(new_pass)
        print(passwords)
        u = User.objects.get(email = th.Email)

        if th.Password == old_pass:
            th.Password = new_pass
            th.save()

            u.password = passwords
            u.save()

        g = Requests()
        g.Name = name
        g.Email = email
        g.User_category = category
        g.Old_password = old_pass
        g.New_password = new_pass
        g.Req_reg = th
        g.save()

        messages.success(request, 'Password Successfully Changed')
        return render(request, 'teacher_home.html')
    return render(request, 't_change_password.html', {'th': th})

def course(request):
    dd = Subject.objects.filter(Sub_reg=request.session['logg'])
    a = []
    b = []
    c = []
    d = []
    e = []
    f = []
    g = []
    h = []
    for i in dd:
        if i.Course_title not in a:
            a.append(i.Course_title)
            b.append(i.Subject_title)
            c.append(i.Course_brief)
            d.append(i.Course_duration)
            e.append(i.Num_of_chapters)
            f.append(i.Course_fee)
            g.append(i.Language)
            h.append(i.id)
    hh = zip(a, b, c, d, e, f, g, h)
    return render(request, 'course.html', {'hh': hh})

    #c_details = Subject.objects.filter(id = request.session['logg'])
    #return render(request, 'course.html', {'c_details': c_details})


def sub_edit(request, h):
    dc = Subject.objects.get(id = h)
    if request.method == 'POST':
        sub_tit = request.POST.get('sub_tit')
        cou_tit = request.POST.get('cou_tit')
        rt = Subject.objects.filter(Sub_reg=request.session['logg'])

        c_brief = request.POST.get('c_brief')
        c_dur = request.POST.get('c_dur')
        n_chapt = request.POST.get('n_chapt')
        c_fee = request.POST.get('c_fee')
        lang = request.POST.get('lang')

        """
        for u in rt:
            if u.Subject_title == sub_tit and u.Course_title == cou_tit:
                dd = Subject.objects.filter(Sub_reg=request.session['logg'])
                a = []
                b = []
                c = []
                d = []
                e = []
                f = []
                g = []
                h = []
                for i in dd:
                    if i.Course_title not in a:
                        a.append(i.Course_title)
                        b.append(i.Subject_title)
                        c.append(i.Course_brief)
                        d.append(i.Course_duration)
                        e.append(i.Num_of_chapters)
                        f.append(i.Course_fee)
                        g.append(i.Language)
                        h.append(i.id)
                hh = zip(a, b, c, d, e, f, g, h)
                messages.success(request, 'Subject Already Exists')
                return render(request, 'course.html', {'hh': hh})"""

        dc.Subject_title = sub_tit
        dc.Course_title = cou_tit
        dc.Course_brief = c_brief
        dc.Course_duration = c_dur
        dc.Num_of_chapters = n_chapt
        dc.Course_fee = c_fee
        dc.Language = lang
        dc.save()

        dd = Subject.objects.filter(Sub_reg=request.session['logg'])
        a = []
        b = []
        c = []
        d = []
        e = []
        f = []
        g = []
        h = []
        for i in dd:
            if i.Course_title not in a:
                a.append(i.Course_title)
                b.append(i.Subject_title)
                c.append(i.Course_brief)
                d.append(i.Course_duration)
                e.append(i.Num_of_chapters)
                f.append(i.Course_fee)
                g.append(i.Language)
                h.append(i.id)
        hh = zip(a, b, c, d, e, f, g, h)
        db = Registration.objects.get(id = request.session['logg'])
        if db.User_role == 'teacher':
            messages.success(request, 'Subject Edited')
            return render(request, 'course.html', {'hh': hh})
        if db.User_role == 'admin':
            dd = Subject.objects.all()
            a = []
            b = []
            c = []
            d = []
            e = []
            f = []
            g = []
            h = []
            for i in dd:
                if i.Course_title not in a:
                    a.append(i.Course_title)
                    b.append(i.Subject_title)
                    c.append(i.Course_brief)
                    d.append(i.Course_duration)
                    e.append(i.Num_of_chapters)
                    f.append(i.Course_fee)
                    g.append(i.Language)
                    h.append(i.id)
            hh = zip(a, b, c, d, e, f, g, h)
            messages.success(request, 'Subject Edited')
            return render(request, 'sub_view.html', {'hh': hh})

    return render(request, 'sub_edit.html', {'dc': dc})

def sub_delete(request, h):
    Subject.objects.get(id=h).delete()
    dd = Subject.objects.filter(Sub_reg=request.session['logg'])
    a = []
    b = []
    c = []
    d = []
    e = []
    f = []
    g = []
    h = []
    for i in dd:
        if i.Course_title not in a:
            a.append(i.Course_title)
            b.append(i.Subject_title)
            c.append(i.Course_brief)
            d.append(i.Course_duration)
            e.append(i.Num_of_chapters)
            f.append(i.Course_fee)
            g.append(i.Language)
            h.append(i.id)
    hh = zip(a, b, c, d, e, f, g, h)
    db = Registration.objects.get(id=request.session['logg'])
    if db.User_role == 'teacher':
        messages.success(request, 'Deleted Successfully')
        return render(request, 'course.html', {'hh': hh})
    if db.User_role == 'admin':
        dd = Subject.objects.all()
        a = []
        b = []
        c = []
        d = []
        e = []
        f = []
        g = []
        h = []
        for i in dd:
            if i.Course_title not in a:
                a.append(i.Course_title)
                b.append(i.Subject_title)
                c.append(i.Course_brief)
                d.append(i.Course_duration)
                e.append(i.Num_of_chapters)
                f.append(i.Course_fee)
                g.append(i.Language)
                h.append(i.id)
        hh = zip(a, b, c, d, e, f, g, h)
        messages.success(request, 'Deleted Successfully')
        return render(request, 'sub_view.html', {'hh': hh})

def add_subject(request):
    if request.method == 'POST':
        sub_tit = request.POST.get('sub_tit')
        cou_tit = request.POST.get('cou_tit')
        rt = Subject.objects.filter(Sub_reg=request.session['logg'])
        for u in rt:
            if u.Subject_title == sub_tit and u.Course_title == cou_tit:
                dd = Subject.objects.filter(Sub_reg=request.session['logg'])
                a = []
                b = []
                c = []
                d = []
                e = []
                f = []
                g = []
                h = []
                for i in dd:
                    if i.Course_title not in a:
                        a.append(i.Course_title)
                        b.append(i.Subject_title)
                        c.append(i.Course_brief)
                        d.append(i.Course_duration)
                        e.append(i.Num_of_chapters)
                        f.append(i.Course_fee)
                        g.append(i.Language)
                        h.append(i.id)
                hh = zip(a, b, c, d, e, f, g, h)
                messages.success(request, 'Subject already exists')
                return render(request, 'course.html', {'hh': hh})
        c_brief = request.POST.get('c_brief')
        c_dur = request.POST.get('c_dur')
        n_chapt = request.POST.get('n_chapt')
        c_fee = request.POST.get('c_fee')
        lang = request.POST.get('lang')
        pk = Registration.objects.get(id=request.session['logg'])
        cdt = Subject()
        cdt.Subject_title = sub_tit
        cdt.Course_title = cou_tit
        cdt.Course_brief = c_brief
        cdt.Course_duration = c_dur
        cdt.Num_of_chapters = n_chapt
        cdt.Course_fee = c_fee
        cdt.Chapter_title = 'Nil'
        cdt.Num_of_videos = 0
        cdt.Num_of_paragraphs = 0
        cdt.Num_of_images = 0
        cdt.Num_of_assignments = 0
        cdt.Chapter_Content_name = 'Nil'
        cdt.Chapter_Content_type = 'Nil'
        cdt.Chapter_Content_Is_mandatory = 0
        cdt.Chapter_Content_Time_required_in_sec = 0
        cdt.Chapter_Content_Is_open_for_free = 0
        cdt.Language = lang
        cdt.Sub_reg = pk
        cdt.save()
        dd = Subject.objects.filter(Sub_reg=request.session['logg'])
        a = []
        b = []
        c = []
        d = []
        e = []
        f = []
        g = []
        h = []
        for i in dd:
            if i.Course_title not in a:
                a.append(i.Course_title)
                b.append(i.Subject_title)
                c.append(i.Course_brief)
                d.append(i.Course_duration)
                e.append(i.Num_of_chapters)
                f.append(i.Course_fee)
                g.append(i.Language)
                h.append(i.id)
        hh = zip(a, b, c, d, e, f, g, h)
        messages.success(request, 'Added subject successfully')
        return render(request, 'course.html', {'hh': hh})
    return render(request, 'add_subject.html')

def chapter(request):
    dm = Subject.objects.filter(Sub_reg=request.session['logg'])
    a = []
    b = []
    c = []
    d = []
    e = []
    for i in dm:
        if i.Chapter_title not in c:
            a.append(i.Subject_title)
            b.append(i.Course_title)
            c.append(i.Chapter_title)
            d.append(i.Num_of_assignments)
            e.append(i.id)
    hh = zip(a, b, c, d, e)
    return render(request, 'chapter.html', {'hh': hh})

def t_edit_chapter(request, a,b,c,e):
    idm = int(e)
    #id = str(id)
    #idd = str(idd)
    #idk = str(idk)
    dm = Subject.objects.filter(Sub_reg=request.session['logg'])
    #dmr = Subject.objects.filter(Sub_reg=request.session['logg'], Subject_title=id, Course_title=idd, Chapter_title=idk)
    gh = Subject.objects.get(id=idm)
    if request.method == 'POST':
        sub = request.POST.get('sub')
        cou = request.POST.get('cou')
        c_tt = request.POST.get('c_tt')
        n_s = request.POST.get('n_s')

        gh.Subject_title = sub
        gh.Course_title = cou
        gh.Chapter_title = c_tt
        gh.Num_of_assignments = n_s
        gh.save()

        a = []
        b = []
        c = []
        d = []
        e = []
        for i in dm:
            if i.Chapter_title not in c:
                a.append(i.Subject_title)
                b.append(i.Course_title)
                c.append(i.Chapter_title)
                d.append(i.Num_of_assignments)
                e.append(i.id)
        hh = zip(a, b, c, d, e)
        messages.success(request, 'Chapter edited successfully')
        return render(request, 'chapter.html', {'hh': hh})
    return render(request, 't_edit_chapter.html', {'gh': gh})

def t_delete_chapter(request, a,b,c,e):
    #idm = int(e)
    id = str(a)
    idd = str(b)
    idk = str(c)
    Subject.objects.filter(Sub_reg=request.session['logg'], Subject_title=id, Course_title=idd,
                           Chapter_title=idk).delete()
    dm = Subject.objects.filter(Sub_reg=request.session['logg'])
    a = []
    b = []
    c = []
    d = []
    e = []
    for i in dm:
        if i.Chapter_title not in c:
            a.append(i.Subject_title)
            b.append(i.Course_title)
            c.append(i.Chapter_title)
            d.append(i.Num_of_assignments)
            e.append(i.id)
    hh = zip(a, b, c, d, e)
    messages.success(request, 'Chapter deleted successfully')
    return render(request, 'chapter.html', {'hh': hh})

def t_add_chapter(request):
    dm = Subject.objects.filter(Sub_reg=request.session['logg'])
    rr = Registration.objects.get(id=request.session["logg"])
    kk = []
    for i in dm:
        if i.Subject_title not in kk:
            kk.append(i.Subject_title)
    if request.method == 'POST':
        cou_tit = request.POST.get('cou_tit1')
        sub_tit = request.session['subj_n']
        ch_tit1 = request.POST.get('ch_tit1')
        assi = request.POST.get('assi')
        cdt = Subject()
        for u in dm:
            if u.Subject_title == sub_tit and u.Course_title == cou_tit and u.Chapter_title == ch_tit1:
                a = []
                b = []
                c = []
                d = []
                e = []
                for i in dm:
                    if i.Chapter_title not in c:
                        a.append(i.Subject_title)
                        b.append(i.Course_title)
                        c.append(i.Chapter_title)
                        d.append(i.Num_of_assignments)
                        e.append(i.id)
                hh = zip(a, b, c, d, e)
                messages.success(request, 'Chapter already exists')
                return render(request, 'chapter.html', {'hh': hh})

        cdt.Subject_title = sub_tit
        cdt.Course_title = cou_tit
        cdt.Course_brief = 'Nil'
        cdt.Course_duration = 0
        cdt.Num_of_chapters = 0
        cdt.Course_fee = 0.0
        cdt.Language = 'Nil'
        cdt.Chapter_title = ch_tit1
        cdt.Num_of_assignments = assi
        cdt.Chapter_Content_name = 'Nil'
        cdt.Chapter_Content_type = 'Nil'
        cdt.Chapter_Content_Is_mandatory = 0
        cdt.Chapter_Content_Time_required_in_sec = 0
        cdt.Chapter_Content_Is_open_for_free = 0
        cdt.Sub_reg = rr
        cdt.save()
        dm = Subject.objects.filter(Sub_reg=request.session['logg'])

        a = []
        b = []
        c = []
        d = []
        e = []
        for i in dm:
            if i.Chapter_title not in c:
                a.append(i.Subject_title)
                b.append(i.Course_title)
                c.append(i.Chapter_title)
                d.append(i.Num_of_assignments)
                e.append(i.id)
        hh = zip(a, b, c, d, e)
        messages.success(request, 'Chapter added successfully')
        return render(request, 'chapter.html', {'hh': hh})
    return render(request, 't_add_chapter.html', {'kk': kk})

def add_chapter1(request):
   gg = request.POST.get('subj')
   gg1 = Subject.objects.filter(Subject_title = gg, Sub_reg = request.session['logg'])
   mm = []
   for y in gg1:
       if y.Course_title not in mm:
           mm.append(y.Course_title)
   request.session['subj_n'] = gg
   return render(request,'add_chapter1.html',{'gg1':gg1,'mm':mm})


def t_content(request):
    mm = Registration.objects.get(id=request.session['logg'])
    mm1 = Subject.objects.filter(Sub_reg=mm)
    return render(request, 't_content.html', {'mm1': mm1})

def t_edit_content(request, id):
    mm = Registration.objects.get(id = request.session['logg'])
    mm1 = Subject.objects.filter(Sub_reg = mm)
    gh = Subject.objects.get(id = id)
    if request.method == 'POST':
        try:
            sub = request.POST.get('sub')
            cou = request.POST.get('cou')
            c_n1 = request.POST.get('c_n')
            c_b1 = request.POST.get('c_b')
            up_cont = request.FILES['up_cont']
            fs = FileSystemStorage()
            fs.save(up_cont.name, up_cont)
            s1 = request.POST.get('s1')
            s = request.POST.get('s')
            time = request.POST.get('time')
            cont_typ = request.POST.get('cont_typ')
            gh.Subject_title = sub
            gh.Course_title = cou
            gh.Chapter_title = c_n1
            if int(cont_typ) == 1:
                gh.Chapter_Content_type = 'Image'
            if int(cont_typ) == 2:
                gh.Chapter_Content_type = 'Text'
            if int(cont_typ) == 3:
                gh.Chapter_Content_type = 'Video'
            gh.Chapter_Content_Is_mandatory  = s
            gh.Chapter_Content_Time_required_in_sec  = time
            gh.Chapter_Content_Is_open_for_free  = s1
            gh.Chapter_Content_name = up_cont
            gh.Chapter_text_content = c_b1
            gh.save()
            messages.success(request, 'Chapter content edited successfully')
            return render(request, 'cont_tr.html', {'mm1': mm1})
        except:
            sub = request.POST.get('sub')
            cou = request.POST.get('cou')
            c_n1 = request.POST.get('c_n')
            c_b1 = request.POST.get('c_b')
            u_con = request.POST.get('u_con')
            s = request.POST.get('s')
            time = request.POST.get('time')
            s1 = request.POST.get('s1')
            cont_typ = request.POST.get('cont_typ')
            gh.Subject_title = sub
            gh.Course_title = cou
            gh.Chapter_title = c_n1
            if int(cont_typ) == 1:
                gh.Chapter_Content_type = 'Image'
            if int(cont_typ) == 2:
                gh.Chapter_Content_type = 'Text'
            if int(cont_typ) == 3:
                gh.Chapter_Content_type = 'Video'
            gh.Chapter_Content_Is_mandatory = s
            gh.Chapter_Content_Time_required_in_sec = time
            gh.Chapter_Content_Is_open_for_free = s1
            gh.Chapter_Content_name = u_con
            gh.Chapter_text_content = c_b1
            gh.save()
            messages.success(request, 'Chapter content edited successfully')
            return render(request, 't_content.html', {'mm1': mm1})
    return render(request, 't_edit_content.html', {'gh': gh})

def t_delete_content(request, id):
    mm = Registration.objects.get(id = request.session['logg'])
    mm1 = Subject.objects.filter(Sub_reg = mm)
    Subject.objects.get(id = id).delete()
    messages.success(request, 'Chapter content deleted successfully')
    return render(request, 't_content.html',{'mm1': mm1})

def t_add_chapter_content(request):
    mm = Registration.objects.get(id = request.session['logg'])
    mm1 = Subject.objects.filter(Sub_reg = mm)
    kkc = Subject.objects.filter(Sub_reg = request.session['logg'])
    kk = []
    for i in kkc:
        if i.Subject_title not in kk:
            kk.append(i.Subject_title)
    if request.method == 'POST':
        sub_tit = request.session['subj_nn']
        sel_c = request.session['court0']
        tex_con = request.POST.get('tex_con')
        ch_tit1 = request.POST.get('ch_tit1')
        fg = Subject.objects.filter(Course_title=sel_c, Subject_title=sub_tit, Chapter_title = ch_tit1, Sub_reg=mm)
        up_c = request.FILES['up_c']
        fs = FileSystemStorage()
        fs.save(up_c.name, up_c)
        s1 = request.POST.get('s1')
        s = request.POST.get('s')
        time = request.POST.get('time')
        cont_typ = request.POST.get('cont_typ')
        for y in fg:
            cdt = Subject()
            cv = int(cont_typ)
            if cv == 1:
                cdt.Chapter_Content_type = 'Image'
            if cv == 2:
                cdt.Chapter_Content_type = 'Text'
            if cv == 3:
                cdt.Chapter_Content_type = 'Video'
            cdt.Subject_title = sub_tit
            cdt.Course_title = y.Course_title
            cdt.Course_brief = y.Course_brief
            cdt.Num_of_chapters = y.Num_of_chapters
            cdt.Course_fee = y.Course_fee
            cdt.Language = y.Language
            cdt.Num_of_assignments = y.Num_of_assignments
            cdt.Chapter_title  = ch_tit1
            cdt.Chapter_Content_name  = up_c
            cdt.Chapter_text_content = tex_con
            cdt.Chapter_Content_Is_mandatory = s
            cdt.Chapter_Content_Time_required_in_sec = time
            cdt.Chapter_Content_Is_open_for_free = s1
            cdt.Course_duration = time
            cdt.Sub_reg = mm
            cdt.save()
            messages.success(request, 'Chapter content added successfully')
            return render(request, 't_content.html', {'mm1': mm1})
    return render(request,'t_add_chapter_content.html',{'kk':kk})

def t_add_chapter_content0(request):
    request.session['subj_nn'] = gg  = request.POST.get('subj')
    bbm = Subject.objects.filter(Sub_reg=request.session['logg'], Subject_title=gg)
    bb = []
    for i in bbm:
        if i.Course_title not in bb:
            bb.append(i.Course_title)
    return render(request, 't_add_chapter_content0.html', {'bb': bb})

def t_add_chapter_content1(request):
    gg = request.session['subj_nn']
    request.session['court0'] = request.POST.get('cou')
    gg = str(gg)
    bbm = Subject.objects.filter(Sub_reg = request.session['logg'], Subject_title = gg, Course_title = request.session['court0'])
    kk = []
    for i in bbm:
        if i.Chapter_title not in kk:
            kk.append(i.Chapter_title)
    return render(request, 't_add_chapter_content1.html', {'gg': gg, 'kk': kk})

def schedule_test(request):
    sew = Registration.objects.get(id=request.session['logg'])
    stz = Enrollment.objects.filter(Teacher_email=sew.Email, Teacher_response='Accepted')
    return render(request, 'schedule_test.html', {'stz': stz})

def schedule_test1(request):
    numbb = request.POST.get('numbb')
    nmbb = int(numbb)
    request.session['exam_start'] = dtt = request.POST.get('dtt')
    request.session['exam_stop'] = stt = request.POST.get('stt')
    request.session['cc'] = nmbb
    k = request.POST.getlist('scd')
    request.session['stu_for_test'] = k
    return render(request,'schedule_test1.html')

def schedule_test2(request):
    m = request.session['stu_for_test']
    ques = request.POST.get('ques')
    op1 = request.POST.get('op1')
    op2 = request.POST.get('op2')
    op3 = request.POST.get('op3')
    ans = request.POST.get('ans')
    c = request.session['cc']
    if c>0:
        for i in m:
            stz = Enrollment.objects.get(id = i)
            fd = Exam()
            fd.Student_name = stz.Student_name
            fd.Student_email = stz.Student_email
            fd.Teacher_name = stz.Teacher_name
            fd.Subject_name = stz.Subject_name
            fd.Course_name = stz.Course_name
            fd.Option1 = op1
            fd.Option2 = op2
            fd.Option3 = op3
            fd.Correct_answer = ans
            fd.Question = ques

            drts = request.session['exam_start']
            drtd = drts.replace('T',' ')
            time_zone = pytz.timezone('Asia/Calcutta')
            drtd = datetime.datetime.strptime(drtd,"%Y-%m-%d %H:%M")
            fd.Time_start = time_zone.localize(drtd)

            drts1 = request.session['exam_stop']
            drtd1 = drts1.replace('T', ' ')
            time_zone = pytz.timezone('Asia/Calcutta')
            drtd1 = datetime.datetime.strptime(drtd1, "%Y-%m-%d %H:%M")
            fd.Time_stop = time_zone.localize(drtd1)

            dt = Registration.objects.get(id = request.session["logg"])
            fd.Exam_reg = dt
            fd.save()
        c -= 1
        request.session['cc'] = c
        if c == 0:
            messages.success(request, 'Exam scheduled successfully')
            return render(request, 'teacher_home.html')
        return render(request,'schedule_test1.html')
    else:
        messages.success(request, 'Exam scheduled successfully')
        return render(request, 'teacher_home.html')



def delete_test(request):
    hh = Registration.objects.get(id=request.session['logg'])
    fg = Exam.objects.filter(Exam_reg=hh)
    return render(request, 'delete_test.html', {'fg': fg})

def delete_test1(request, id):
    Exam.objects.get(id = id).delete()
    hh = Registration.objects.get(id=request.session['logg'])
    fg = Exam.objects.filter(Exam_reg=hh)
    messages.success(request, 'Test Deleted successfully')
    return render(request, 'delete_test.html', {'fg': fg})

def exam_results(request):
    hh = Registration.objects.get(id=request.session['logg'])
    gt = Exam_results.objects.filter(Teacher_name=hh.First_name)
    return render(request, 'exam_results.html', {'hh': hh, 'gt': gt})

def delete_ex_re(request, id):
    Exam_results.objects.get(id =id).delete()
    hh = Registration.objects.get(id=request.session['logg'])
    gt = Exam_results.objects.filter(Teacher_name=hh.First_name)
    messages.success(request, 'Exam Result Deleted successfully')
    return render(request, 'exam_results.html', {'hh': hh, 'gt': gt})

def t_messages(request):
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    return render(request,'t_messages.html',{'bb':bb})

def t_send_msg(request):
    p = Registration.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email)
    kk = Registration.objects.all()
    if request.method == 'POST':
        to_em = request.POST.get('to_em')
        ddp = str(to_em)
        gg = ddp.split()
        pnm = gg[0]
        first = gg[2]
        last = gg[3]
        msg_cont = request.POST.get('msg_cont')
        nm = Messages()
        nm.Category = p.User_role
        kkp = Registration.objects.get(id=request.session['logg'])
        nm.Name = first + ' ' + last
        nm.From_email = kkp.Email
        nm.To_email = pnm
        nm.Message_content = msg_cont
        nm.save()
        messages.success(request, 'Message sent successfully')
        return render(request, 't_messages.html', {'bb': bb})
    return render(request, 't_send_msg.html', {'kk': kk})

def del_msg_teacher(request, id):
    Messages.objects.get(id=id).delete()
    p = Registration.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email)
    messages.success(request, 'Message Delete successfully')
    return render(request, 't_messages.html', {'bb': bb})

def reply_msg_teacher(request, id):
    pa = Messages.objects.get(id = id)
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    if request.method == 'POST':
        f_email = request.POST.get('f_email')
        to_email = request.POST.get('to_email')
        msg_cont = request.POST.get('msg_cont')
        pa1 = Messages()
        pa1.Category = p.User_role
        pa1.From_email = to_email
        pa1.To_email = f_email
        pa1.Message_content = msg_cont
        pa1.save()
        messages.success(request, 'Message reply successful')
        return render(request, 't_messages.html', {'bb': bb})
    return render(request,'reply_msg_teacher.html',{'pa':pa})

def attendence(request):
    h = Registration.objects.get(id=request.session['logg'])
    ss = Enrollment.objects.filter(Teacher_email=h.Email)
    if request.method == 'POST':
        atn = request.POST.get('atn')
        atn1 = request.POST.get('atn1')
        dw = Enrollment.objects.get(id=atn)
        dw.Attendance = atn1
        dw.save()
        messages.success(request, 'Attendance given')
        return render(request, 'teacher_home.html')
    return render(request, 'attendence.html', {'ss': ss})

def t_student_booked(request):
    seww = Registration.objects.get(id=request.session['logg'])
    stzz = Enrollment.objects.filter(Teacher_email=seww.Email)
    return render(request, 't_student_booked.html', {'stzz': stzz})

def stu_accept(request, id):
    seww = Registration.objects.get(id=request.session['logg'])
    stzz = Enrollment.objects.filter(Teacher_email = seww.Email)
    sas = Enrollment.objects.get(id = id)
    sas.Teacher_response = 'Accepted'
    sas.save()
    return render(request,'t_student_booked.html',{'stzz':stzz})

def stu_reject(request, id):
    seww = Registration.objects.get(id = request.session['logg'])
    stzz = Enrollment.objects.filter(Teacher_email = seww.Email)
    sas = Enrollment.objects.get(id=id)
    sas.Teacher_response = 'Rejected'
    sas.save()
    return render(request, 't_student_booked.html', {'stzz': stzz})

def stu_delete(request, id):
    Enrollment.objects.get(id = id).delete()
    seww = Registration.objects.get(id=request.session['logg'])
    stzz = Enrollment.objects.filter(Teacher_email=seww.Email)
    messages.success(request, 'Enrolled student deleted successfully')
    return render(request, 't_student_booked.html', {'stzz': stzz})


#student functions


def student_booked_courses(request):
    st = Registration.objects.get(id=request.session['logg'])
    buk = Enrollment.objects.filter(enrol_reg=st)
    return render(request, 'student_booked_courses.html', {'buk': buk, 'st': st})

def acc_chapter0(request, id):
    #request.session['courss'] = str(ikm)
    gh = Enrollment.objects.get(id=id)
    if gh.Teacher_response == 'To be expected':
        messages.success(request, 'Please wait for approval')
        return render(request, 'student_home.html')
    ftr = Registration.objects.get(Email = gh.Teacher_email)
    dd = Subject.objects.filter(Course_title = gh.Course_name, Sub_reg = ftr)
    nn = Registration.objects.get(Email = gh.Teacher_email)
    dm = Subject.objects.filter(Subject_title = gh.Subject_name, Course_title = gh.Course_name, Sub_reg = nn.id)
    for i in dm:
        if i.Course_fee > gh.Paid_amount:
            messages.success(request, 'Your payment balance is pending')
            return render(request, 'student_home.html')
    fd = []
    for i in dd:
        if i.Chapter_title not in fd:
            fd.append(i.Chapter_title)
    return render(request, 'acc_chapter0.html', {'fd':fd})


def acc_chapter1(request):
    kp = Learning_progress.objects.filter(Learn_p_reg = request.session["logg"], Status = "P")
    sz1 = request.POST.get('cha')
    ksk = Learning_progress.objects.filter(Learn_p_reg=request.session["logg"], Course_chapter_name = sz1)
    for y in ksk:
        if y.Status == "C":
            messages.success(request, 'You have already finished this chapter')
            return render(request, 'student_home.html')
    sz = Subject.objects.filter(Chapter_title = sz1)
    return render(request,'acc_chapter1.html',{'sz':sz,'kp':kp})

def compp(request):
    mnm = Registration.objects.get(id = request.session["logg"])
    idd = request.POST.getlist('id')
    comm = request.POST.getlist('comm')
    ggt = zip(idd, comm)
    for i,h in ggt:
        df = Subject.objects.get(id = i)
        t_id = df.Sub_reg_id
        t = Registration.objects.get(id = t_id)
        t_mail = t.Email
        try:
           pk = Learning_progress.objects.get(Student_name = mnm.First_name, Student_email = mnm.Email, Subject_name = df.Subject_title, Course_name = df.Course_title,Course_chapter_name =  df.Chapter_title,Course_chapter_content_name = df.Chapter_Content_name)
           pk.Student_name = mnm.First_name
           pk.Student_email = mnm.Email
           pk.Subject_name = df.Subject_title
           pk.Course_name = df.Course_title
           pk.Course_chapter_name = df.Chapter_title
           pk.Course_chapter_content_name = df.Chapter_Content_name
           pk.Status = h
           pk.Learn_p_reg = mnm
           pk.Teacher_email = t_mail
           pk.save()
        except:
           pk = Learning_progress()
           pk.Student_name = mnm.First_name
           pk.Student_email = mnm.Email
           pk.Subject_name = df.Subject_title
           pk.Course_name = df.Course_title
           pk.Course_chapter_name = df.Chapter_title
           pk.Course_chapter_content_name = df.Chapter_Content_name
           pk.Status = h
           pk.Learn_p_reg = mnm
           pk.Teacher_email = t_mail
           pk.save()
    return render(request,'student_home.html')

def stu_book_course(request):
    kkc = Subject.objects.all()
    kk = []
    for i in kkc:
        if i.Subject_title not in kk:
            kk.append(i.Subject_title)
        #messages.success(request, 'Chapter content added successfully')
        #return render(request, 't_content.html')
    return render(request, 'stu_book_course.html', {'kk': kk})

def stu_book_course0(request):
    if request.method == 'POST':
        request.session['subj_nn'] = gg = request.POST.get('subj')
        bbm = Subject.objects.filter(Subject_title=gg)
        bb = []
        for i in bbm:
            if i.Course_title not in bb:
                bb.append(i.Course_title)
        return render(request, 'stu_book_course0.html', {'bb': bb})

def stu_book_course1(request):
    gg = request.session['subj_nn']
    request.session['court0'] = request.POST.get('cou')
    gg = str(gg)
    bbm = Subject.objects.filter(Sub_reg=request.session['logg'], Subject_title=gg,
                                 Course_title=request.session['court0'])
    kk = []
    for i in bbm:
        if i.Chapter_title not in kk:
            kk.append(i.Chapter_title)
    if request.method == 'POST':
        sub_tit = request.session['subj_nn']
        sel_c = request.session['court0']
        dc = Subject.objects.filter(Subject_title=sub_tit, Course_title=sel_c)
        for i in dc:
            sub_id = i.Sub_reg_id
        db = Registration.objects.filter(id = sub_id)
        a = []
        b = []
        c = []
        d = []
        e = []
        f = []
        g = []
        h = []
        i = []
        j = []
        k = []
        l = []
        m = []
        n = []

        for z in db:
            a.append(z.First_name)
            b.append(z.Email)
            c.append(z.Qualification)
            d.append(z.Introduction_brief)
            e.append(z.Image)
            f.append(z.Num_of_reviews)
            n.append(z.id)

        for z in dc:
            g.append(z.Subject_title)
            h.append(z.Course_title)
            i.append(z.Course_brief)
            j.append(z.Course_duration)
            k.append(z.Num_of_chapters)
            l.append(z.Course_fee)
            m.append(z.Language)

        kc = zip(a, b, c, d, e, f, g, h, i, j, k, l, m, n)

        return render(request,'stu_book_course1.html', {'kc': kc} )
    return render(request, 'stu_book_course0.html', {'gg': gg, 'kk': kk})

def stu_course_payment(request, l, n):
    request.session['t_id'] = n
    paidd = l
    if request.method == 'POST':
        #paidd = request.POST.get('pay')
        dh = Registration.objects.get(id=request.session['logg'])
        nm = Registration.objects.get(id=request.session['t_id'])
        gg = Subject.objects.filter(Sub_reg=nm.id, Course_title=request.session['court0'],
                                    Subject_title=request.session['subj_nn'])
        spp = Enrollment()
        spp.Student_name = dh.First_name
        spp.Student_email = dh.Email
        spp.Subject_name = request.session['subj_nn']
        spp.Course_name = request.session['court0']
        spp.Teacher_name = nm.First_name
        spp.Teacher_email = nm.Email
        spp.Paid_amount = paidd
        spp.Attendance = 0
        spp.Pending_days = 0
        spp.Teacher_response = 'To be expected'
        for i in gg:
            if i.Course_fee > 0:
                spp.Is_paid_subscription = 'True'
            else:
                spp.Is_paid_subscription = 'False'
        spp.enrol_reg = dh
        spp.save()
        messages.success(request, 'You have successfully booked a course')
        return render(request, 'student_home.html')

    return render(request,'stu_course_payment.html',{'l': l})

def down_cer(request):
    dd = Registration.objects.get(id=request.session['logg'])
    sr = Enrollment.objects.filter(Student_name=dd.First_name, Student_email=dd.Email)
    j = []
    for p in sr:
        if p.Certificate != "":
            j.append(p.Certificate)
    if not j:
        messages.success(request, 'No certificate available')
        return render(request, 'student_home.html')
    return render(request, 'down_cer.html', {'sr': sr})

def stu_profile(request):
    dc = Registration.objects.get(id=request.session['logg'])
    kk = User.objects.get(username=dc.user)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        kk.first_name = first_name
        kk.last_name = last_name
        kk.email = email
        kk.save()

        dc.First_name = first_name
        dc.Last_name = last_name
        dc.Email = email
        dc.save()
        messages.success(request, 'Edit data successfully saved')
        return render(request, 'stu_profile.html', {'dc': dc})
    else:
        return render(request, 'stu_profile.html', {'dc': dc})

def stu_feedback(request):
    x = datetime.datetime.now()
    y = x.strftime("%Y-%m-%d")
    dd = Registration.objects.get(id=request.session['logg'])
    ds = Enrollment.objects.filter(enrol_reg=dd)
    fd = []
    for i in ds:
        if i.Course_name not in fd:
            fd.append(i.Course_name)
    fd1 = []
    for i in ds:
        if i.Subject_name not in fd1:
            fd1.append(i.Subject_name)
    fd2 = []
    fd3 = []
    for i in ds:
        if i.Teacher_email not in fd3:
            fd3.append(i.Teacher_email)
            fd2.append(i.Teacher_name)
    fd4 = zip(fd2, fd3)
    if request.method == 'POST':
        course = request.POST.get('select')
        subject = request.POST.get('select3')
        teach = request.POST.get('select4')
        teach1 = teach.split(";")
        try:
            tt = teach1[0]
            ttt = teach1[1]
        except:
            messages.success(request, 'Please register a course')
            return render(request, 'stu_feedback.html', {'fd': fd, 'fd1': fd1, 'fd4': fd4})
        score = request.POST.get('select1')
        text_feed = request.POST.get('text_feed')
        qw = Feedback()
        qw.Subject_name = subject
        qw.Teacher_name = tt
        qw.Teacher_email = ttt
        for i in ds:
            qw.Student_name = i.Student_name
            qw.Student_email = i.Student_email
            break
        qw.Course_name = course
        qw.Feedback_text = text_feed
        qw.Rating_score = score
        qw.Submission_date = y
        qw.Feed_reg = dd
        qw.save()
        messages.success(request, 'Thank you for your valuable feedback')
        return render(request, 'student_home.html')
    return render(request, 'stu_feedback.html', {'fd': fd, 'fd1': fd1, 'fd4': fd4})

def stu_change_pass(request):
    th = Registration.objects.get(id=request.session['logg'])
    if request.method == 'POST':
        new_pass = request.POST.get('pssw')
        old_pass = request.POST.get('pssw_old')
        email = request.POST.get('em')
        category = request.POST.get('usr')
        name = request.POST.get('nam')

        passwords = make_password(new_pass)
        print(passwords)
        u = User.objects.get(email=th.Email)

        if th.Password == old_pass:
            th.Password = new_pass
            th.save()

            u.password = passwords
            u.save()

        g = Requests()
        g.Name = name
        g.Email = email
        g.User_category = category
        g.Old_password = old_pass
        g.New_password = new_pass
        g.Req_reg = th
        g.save()
        messages.success(request, 'Please wait for your password approval.. Continue to use old password')
        return render(request, 'student_home.html')
    return render(request, 'stu_change_pass.html', {'th': th})

def exam_notifi(request):
    local_tz = pytz.timezone("Asia/Calcutta")
    hh = Registration.objects.get(id=request.session['logg'])
    fg = Exam.objects.filter(Student_email=hh.Email)
    kk = []
    for i in fg:
        bb = i.Time_start
        cpp = bb.replace(tzinfo=pytz.utc).astimezone(local_tz)
        bbn = cpp.strftime("%Y-%B-%d %H:%M:%S %p")
        if bbn not in kk:
            kk.append('Subject name')
            kk.append(i.Subject_name)
            kk.append('Course name')
            kk.append(i.Course_name)
            kk.append('Start time')
            ft = i.Time_start
            ftt = ft.replace(tzinfo=pytz.utc).astimezone(local_tz)
            fty = ftt.strftime("%Y-%B-%d %H:%M:%S %p")
            kk.append(fty)
            kk.append('Stop time')
            fte = i.Time_stop
            ftee = fte.replace(tzinfo=pytz.utc).astimezone(local_tz)
            fty1 = ftee.strftime("%Y-%B-%d %H:%M:%S %p")
            kk.append(fty1)
            kk.append('....................................................................')
    return render(request, 'exam_notifi.html', {'kk': kk})

def start_test(request):
    local_tz = pytz.timezone("Asia/Calcutta")
    hh = Registration.objects.get(id = request.session['logg'])
    fg = Exam.objects.filter(Student_email = hh.Email)
    x = datetime.datetime.now()
    x = pytz.utc.localize(x)
    fgc = timezone.now()
    hj = []
    for i in fg:
        zz = i.Time_start
        nb = i.Time_stop
        nbn = nb.replace(tzinfo=pytz.utc).astimezone(local_tz)
        nbnn = nbn.strftime("%Y-%B-%d %I:%M:%S %p")
        if fgc>zz and fgc<nb:
            nb = Exam.objects.filter(Student_email = hh.Email, Time_start__lte = fgc, Time_stop__gte = fgc)
            for i in nb:
                if i.Lock == 'locked':
                    messages.success(request, 'You have already attended the exam')
                    return render(request, 'student_home.html')
            for i in nb:
                hj.append(i.Correct_answer)
                request.session['teec'] = i.Teacher_name
                request.session['ssub'] = i.Subject_name
                request.session['student'] = i.Student_name
                request.session['student_ema'] = i.Student_email
                gg = str(nbnn)
            request.session['exam_id'] = hj
            return render(request,'start_test.html',{'nb':nb,'gg':gg})
    messages.success(request, 'No exam is scheduled now')
    return render(request, 'student_home.html')

def save_exam(request):
    end_time = request.POST.get('end_time')
    edr = datetime.datetime.strptime(end_time, '%Y-%B-%d %I:%M:%S %p')
    b = datetime.datetime.now()
    bb = b.strftime('%Y-%B-%d %H:%M:%S ')
    edr1 = datetime.datetime.strptime(bb, '%Y-%B-%d %H:%M:%S ')
    if edr < edr1:
        messages.success(request, 'You have timed out')
        return render(request, 'student_home.html')
    correct_answers = request.POST.getlist('exx3')
    answers = request.POST.getlist('exx')
    if len(correct_answers) != len(answers):
        messages.success(request, 'Your exam attempt failed due to selecting multiple answers')
        return render(request,'student_home.html')
    count = 0
    count1 = 0
    for i in correct_answers:
        count1 += 1
    for i,j in zip(correct_answers,answers):
        if i == j:
            count += 1
    hh = Registration.objects.get(id = request.session['logg'])
    fg = Exam.objects.filter(Student_email = hh.Email)
    x = datetime.datetime.now()
    x = pytz.utc.localize(x)
    fgc = timezone.now()
    for i in fg:
        zz = i.Time_start
        nb = i.Time_stop
        if fgc > zz and fgc < nb:
            nb = Exam.objects.filter(Student_email = hh.Email, Time_start__lte = fgc, Time_stop__gte = fgc)
            for i in nb:
                i.Lock = 'locked'
                i.save()
    ddd = Exam_results()
    ddd.Student_name = request.session['student']
    ddd.Student_email = request.session['student_ema']
    ddd.Teacher_name = request.session['teec']
    ddd.Subject_name = request.session['ssub']
    ddd.Total_marks = count1
    ddd.Acquired_marks = count
    avg = 100 * float(count)/float(count1)
    if avg >= 80:
        ddd.Grade = 'A'
    elif avg < 80 and avg >= 50 :
        ddd.Grade = 'B'
    elif avg < 50 and avg >= 30:
        ddd.Grade = 'C'
    elif avg < 50 and avg >= 30:
        ddd.Grade = 'C'
    else:
        ddd.Grade = 'Failed'
    ddd.Time_stop = b
    ddd.Exam_res_reg = hh
    ddd.save()
    messages.success(request, 'You have successfully finished your exam')
    return render(request, 'student_home.html')


def exam_result(request):
    gt = Exam_results.objects.all()
    hh = Registration.objects.get(id=request.session['logg'])
    return render(request, 'exam_result.html', {'hh': hh, 'gt': gt})

def stu_message(request):
    p = Registration.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email)
    return render(request, 'stu_message.html', {'bb': bb})

def s_send_msg(request):
    p = Registration.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email)
    kk = Registration.objects.all()
    if request.method == 'POST':
        to_em = request.POST.get('to_em')
        ddp = str(to_em)
        gg = ddp.split()
        pnm = gg[0]
        first = gg[2]
        last = gg[3]
        msg_cont = request.POST.get('msg_cont')
        nm = Messages()
        nm.Category = p.User_role
        kkp = Registration.objects.get(id=request.session['logg'])
        nm.Name = first + ' ' + last
        nm.From_email = kkp.Email
        nm.To_email = pnm
        nm.Message_content = msg_cont
        nm.save()
        messages.success(request, 'Message sent successfully')
        return render(request, 'stu_message.html', {'bb': bb})
    return render(request, 's_send_msg.html', {'kk': kk})

def del_msg_student(request, id):
    Messages.objects.get(id=id).delete()
    p = Registration.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email)
    messages.success(request, 'Message Delete successfully')
    return render(request, 'stu_message.html', {'bb': bb})

def reply_msg_student(request, id):
    pa = Messages.objects.get(id = id)
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    if request.method == 'POST':
        f_email = request.POST.get('f_email')
        to_email = request.POST.get('to_email')
        msg_cont = request.POST.get('msg_cont')
        pa1 = Messages()
        pa1.Category = p.User_role
        pa1.From_email = to_email
        pa1.To_email = f_email
        pa1.Message_content = msg_cont
        pa1.save()
        messages.success(request, 'Message reply successful')
        return render(request, 'stu_message.html', {'bb': bb})
    return render(request,'reply_msg_student.html',{'pa':pa})


