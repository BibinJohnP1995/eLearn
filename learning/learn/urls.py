from django.urls import path
import learn.views

urlpatterns = [
    #index home paths
    path('', learn.views.home, name='home'),
    path('home', learn.views.home, name='home'),
    path('news', learn.views.news, name='news'),
    path('about_page', learn.views.about_page, name='about_page'),
    path('add_blog', learn.views.add_blog, name='add_blog'),
    path('display_blog', learn.views.display_blog, name='display_blog'),
    path('contact', learn.views.contact, name='contact'),
    path('login', learn.views.login, name='login'),
    path('register_teacher', learn.views.register_teacher, name='register_teacher'),
    path('register_student', learn.views.register_student, name='register_student'),
    path('register_admin', learn.views.register_admin, name='register_admin'),
    path('admin', learn.views.admin, name='admin'),
    path('footer', learn.views.footer, name='footer'),
    path('logout', learn.views.logout, name='logout'),
    path('t_add_chapter',learn.views.t_add_chapter, name='t_add_chapter'),
    path('add_chapter1',learn.views.add_chapter1, name='add_chapter1'),


    #admin home paths
    path('admin_home', learn.views.admin_home, name='admin_home'),
    path('admin_profile', learn.views.admin_profile, name='admin_profile'),
    path('blogs_admin', learn.views.blogs_admin, name='blogs_admin'),

    path('upload_cer', learn.views.upload_cer, name='upload_cer'),
    path('delete_cer', learn.views.delete_cer, name='delete_cer'),
    path('delete_certificate/<id>', learn.views.delete_certificate, name='delete_certificate'),


    path('about_content', learn.views.about_content, name='about_content'),
    path('block', learn.views.block, name='block'),
    path('feedback', learn.views.feedback, name='feedback'),
    path('feed_delete/<feed>', learn.views.feed_delete, name='feed_delete'),
    path('pass_req', learn.views.pass_req, name='pass_req'),

    path('member_messages', learn.views.member_messages, name='member_messages'),
    path('del_msg_admin/<id>', learn.views.del_msg_admin, name='del_msg_admin'),
    path('reply_msg_admin/<id>', learn.views.reply_msg_admin, name='reply_msg_admin'),
    path('sent_msg_admin', learn.views.sent_msg_admin, name='sent_msg_admin'),

    path('guest_messages', learn.views.guest_messages, name='guest_messages'),
    path('delete_g_msg/<id>', learn.views.delete_g_msg, name='delete_g_msg'),

    path('sub_edit_admin/<h>', learn.views.sub_edit_admin, name='sub_edit_admin'),
    path('sub_view', learn.views.sub_view, name='sub_view'),
    path('chapter_add', learn.views.chapter_add, name='chapter_add'),
    path('edit_chapter_ad/<id>/<idd>/<idt>/<idk>/<pkm>', learn.views.edit_chapter_ad, name='edit_chapter_ad'),
    path('delete_chapter_ad/<id>/<idd>/<idt>/<idk>/<pkm>', learn.views.delete_chapter_ad, name='delete_chapter_ad'),

    path('content_add', learn.views.content_add, name='content_add'),
    path('edit_content_ad/<id>', learn.views.edit_content_ad, name='edit_content_ad'),
    path('delete_content_ad/<id>', learn.views.delete_content_ad, name='delete_content_ad'),

    path('approve_admin/<apr>', learn.views.admin_approve, name='approve_admin'),
    path('reject_admin/<rej>', learn.views.admin_reject, name='reject_admin'),
    path('delete_admin/<delt>', learn.views.admin_delete, name='delete_admin'),
    path('t_allow/<talw>', learn.views.t_allow, name='t_allow'),
    path('t_block/<tblc>', learn.views.t_block, name='t_block'),
    path('s_allow/<salw>', learn.views.s_allow, name='s_allow'),
    path('s_block/<sblc>', learn.views.s_block, name='s_block'),


    #teacher home paths
    path('teacher_home', learn.views.teacher_home, name='teacher_home'),
    path('teacher_profile', learn.views.teacher_profile, name='teacher_profile'),
    path('student_progress', learn.views.student_progress, name='student_progress'),
    path('t_change_password', learn.views.t_change_password, name='t_change_password'),
    path('course', learn.views.course, name='course'),
    path('add_subject', learn.views.add_subject, name='add_subject'),
    path('sub_edit/<h>', learn.views.sub_edit, name='sub_edit'),
    path('sub_delete/<h>', learn.views.sub_delete, name='sub_delete'),
    path('chapter', learn.views.chapter, name='chapter'),
    path('t_edit_chapter/<a>/<b>/<c>/<e>', learn.views.t_edit_chapter, name='t_edit_chapter'),
    path('t_delete_chapter/<a>/<b>/<c>/<e>', learn.views.t_delete_chapter, name='t_delete_chapter'),
    path('t_add_chapter', learn.views.t_add_chapter, name='t_add_chapter'),
    path('t_content', learn.views.t_content, name='t_content'),
    path('t_edit_content,/<id>', learn.views.t_edit_content, name='t_edit_content'),
    path('t_delete_content,/<id>', learn.views.t_delete_content, name='t_delete_content'),
    path('t_add_chapter_content', learn.views.t_add_chapter_content, name='t_add_chapter_content'),
    path('t_add_chapter_content0', learn.views.t_add_chapter_content0, name='t_add_chapter_content0'),
    path('t_add_chapter_content1', learn.views.t_add_chapter_content1, name='t_add_chapter_content1'),

    path('t_student_booked', learn.views.t_student_booked, name='t_student_booked'),
    path('stu_accept/<id>', learn.views.stu_accept, name='stu_accept'),
    path('stu_reject/<id>', learn.views.stu_reject, name='stu_reject'),
    path('stu_delete/<id>', learn.views.stu_delete, name='stu_delete'),

    path('schedule_test', learn.views.schedule_test, name='schedule_test'),
    path('schedule_test1', learn.views.schedule_test1, name='schedule_test1'),
    path('schedule_test2', learn.views.schedule_test2, name='schedule_test2'),

    path('delete_test', learn.views.delete_test, name='delete_test'),
    path('delete_test1/<id>', learn.views.delete_test1, name='delete_test1'),
    path('exam_results', learn.views.exam_results, name='exam_results'),
    path('delete_ex_re/<id>', learn.views.delete_ex_re, name='delete_ex_re'),


    path('t_messages', learn.views.t_messages, name='t_messages'),
    path('t_send_msg', learn.views.t_send_msg, name='t_send_msg'),
    path('del_msg_teacher/<id>', learn.views.del_msg_teacher, name='del_msg_teacher'),
    path('reply_msg_teacher/<id>', learn.views.reply_msg_teacher, name='reply_msg_teacher'),

    path('attendence', learn.views.attendence, name='attendence'),

    #student home paths
    path('student_home', learn.views.student_home, name='student_home'),

    path('stu_booked_courses', learn.views.student_booked_courses, name='student_booked_courses'),
    path('acc_chapter0/<id>', learn.views.acc_chapter0, name='acc_chapter0'),
    path('acc_chapter1', learn.views.acc_chapter1, name='acc_chapter1'),
    path('compp', learn.views.compp, name='compp'),

    path('stu_book_course', learn.views.stu_book_course, name='stu_book_course'),
    path('stu_book_course0', learn.views.stu_book_course0, name='stu_book_course0'),
    path('stu_book_course1', learn.views.stu_book_course1, name='stu_book_course1'),
    path('stu_course_payment/<l>/<n>', learn.views.stu_course_payment, name='stu_course_payment'),

    path('down_cer', learn.views.down_cer, name='down_cer'),
    path('stu_profile', learn.views.stu_profile, name='stu_profile'),
    path('stu_feedback', learn.views.stu_feedback, name='stu_feedback'),
    path('stu_change_pass', learn.views.stu_change_pass, name='stu_change_pass'),
    path('exam_notifi', learn.views.exam_notifi, name='exam_notifi'),
    path('start_test', learn.views.start_test, name='start_test'),
    path('save_exam', learn.views.save_exam, name='save_exam'),
    path('exam_result', learn.views.exam_result, name='exam_result'),

    path('stu_message', learn.views.stu_message, name='stu_message'),
    path('s_send_msg', learn.views.s_send_msg, name='s_send_msg'),
    path('del_msg_student/<id>', learn.views.del_msg_student, name='del_msg_student'),
    path('reply_msg_student/<id>', learn.views.reply_msg_student, name='reply_msg_student'),

]