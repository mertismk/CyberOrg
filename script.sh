#!/bin/bash
find templates -type f -name "*.html" -exec sed -i '' \
  -e "s/url_for('auth.login'/url_for('login'/g" \
  -e "s/url_for('auth.logout'/url_for('logout'/g" \
  -e "s/url_for('auth.profile'/url_for('profile'/g" \
  -e "s/url_for('student.students_list'/url_for('students_list'/g" \
  -e "s/url_for('student.student_detail'/url_for('student_detail'/g" \
  -e "s/url_for('student.student_new'/url_for('student_new'/g" \
  -e "s/url_for('student.student_edit'/url_for('student_edit'/g" \
  -e "s/url_for('student.guide'/url_for('guide'/g" \
  -e "s/url_for('webinar.webinars_list'/url_for('webinars_list'/g" \
  -e "s/url_for('webinar.search'/url_for('search'/g" \
  -e "s/url_for('webinar.add_webinar_comment'/url_for('add_webinar_comment'/g" \
  -e "s/url_for('webinar.delete_webinar_comment'/url_for('delete_webinar_comment'/g" \
  -e "s/url_for('webinar.import_webinars'/url_for('import_webinars'/g" \
  -e "s/url_for('user.users_list'/url_for('users_list'/g" \
  -e "s/url_for('user.user_new'/url_for('user_new'/g" \
  -e "s/url_for('user.user_edit'/url_for('user_edit'/g" \
  -e "s/url_for('plan.create_study_plan'/url_for('create_study_plan'/g" \
  -e "s/url_for('plan.view_study_plan'/url_for('view_study_plan'/g" \
  -e "s/url_for('plan.edit_study_plan'/url_for('edit_study_plan'/g" \
  -e "s/url_for('student.mark_webinar_watched'/url_for('mark_webinar_watched'/g" \
  -e "s/url_for('student.update_known_tasks'/url_for('update_known_tasks'/g" \
  -e "s/url_for('plan.delete_study_plan'/url_for('delete_study_plan'/g" \
  -e "s/url_for('plan.mark_all_webinars_watched'/url_for('mark_all_webinars_watched'/g" \
  {} \;
