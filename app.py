
import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓"
)

st.title("🎓 Student Record Management System")

# Initialize student database
if "students" not in st.session_state:
    st.session_state.students = pd.DataFrame(
        columns=["ID", "Name", "Age", "Course", "Email"]
    )

df = st.session_state.students

# Sidebar menu
menu = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "View Students",
     "Update Student", "Delete Student"]
)

# CREATE
if menu == "Add Student":
    st.subheader("Add New Student")

    with st.form("add_form"):
        sid = st.number_input("Student ID", min_value=1, step=1)
        name = st.text_input("Student Name")
        age = st.number_input("Age", min_value=1, max_value=100)
        course = st.text_input("Course")
        email = st.text_input("Email")

        submit = st.form_submit_button("Add Student")

        if submit:
            if name and course and email:
                if sid not in df["ID"].values:
                    new_student = pd.DataFrame([{
                        "ID": sid,
                        "Name": name,
                        "Age": age,
                        "Course": course,
                        "Email": email
                    }])

                    st.session_state.students = pd.concat(
                        [df, new_student], ignore_index=True
                    )
                    st.success("Student added successfully!")
                else:
                    st.error("Student ID already exists.")
            else:
                st.warning("Please fill all fields.")

# READ
elif menu == "View Students":
    st.subheader("All Student Records")

    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No student records found.")

# UPDATE
elif menu == "Update Student":
    st.subheader("Update Student Details")

    if not df.empty:
        sid = st.selectbox("Select Student ID", df["ID"])

        student = df[df["ID"] == sid].iloc[0]

        with st.form("update_form"):
            name = st.text_input("Name", student["Name"])
            age = st.number_input(
                "Age", min_value=1, max_value=100,
                value=int(student["Age"])
            )
            course = st.text_input("Course", student["Course"])
            email = st.text_input("Email", student["Email"])

            update = st.form_submit_button("Update Student")

            if update:
                idx = st.session_state.students[
                    st.session_state.students["ID"] == sid
                ].index[0]

                st.session_state.students.loc[idx, [
                    "Name", "Age", "Course", "Email"
                ]] = [name, age, course, email]

                st.success("Student updated successfully!")
    else:
        st.info("No records available to update.")

# DELETE
elif menu == "Delete Student":
    st.subheader("Delete Student Record")

    if not df.empty:
        sid = st.selectbox("Select Student ID", df["ID"])

        if st.button("Delete Student"):
            st.session_state.students = df[
                df["ID"] != sid
            ].reset_index(drop=True)

            st.success("Student deleted successfully!")
    else:
        st.info("No records available to delete.")
