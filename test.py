import streamlit as st
import pandas as pd

# --- CORE LOGIC START ---

# 1. Student Class
class Student:
    def __init__(self, student_name, student_id, fees):
        self.student_name = student_name
        self.student_id = student_id
        self.fees = fees

# --- CORE LOGIC END (No more file-handling functions) ---


# --- STREAMLIT APP START ---

st.title("👨‍🎓 Student Management System (In-Memory Storage)")
st.info("Data is stored only in the current browser session's memory and will be lost on page refresh or app restart.")

# --- Initialization and State Management ---

# Initial data load: Use a simple list if session state is empty.
# This list is the variable storage for all student data.
if 'students' not in st.session_state:
    st.session_state.students = [] # Initialize with an empty list

# --- Replacing the CLI Menu with a Sidebar Radio Button ---
st.sidebar.header("Actions")
menu_choice = st.sidebar.radio(
    "Select a Task:",
    ('View All Students', 'Add New Student', 'Update Fees', 'Display Single Student Details')
)

# --- Common Function to Display Data ---
def display_all_students(student_list):
    """Converts student list to a DataFrame and displays it."""
    # Use st.session_state.students directly for the list
    data = [{
        'Name': s.student_name, 
        'ID': s.student_id, 
        'Fees Due': s.fees
    } for s in student_list]
    
    st.subheader("Current Student Roster")
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No students registered yet.")

# --- 1. View All Students ---
if menu_choice == 'View All Students':
    display_all_students(st.session_state.students)

# --- 2. Add New Student (Replaces add_student CLI logic) ---
elif menu_choice == 'Add New Student':
    st.header("➕ Add New Student")
    
    with st.form("add_student_form"):
        # Replacing input() with Streamlit widgets
        name = st.text_input("Enter student name:", key="new_name")
        student_id = st.text_input("Enter student ID:", key="new_id")
        fees = st.number_input("Enter initial fees amount:", min_value=0.0, format="%.2f", key="new_fees")
        
        submitted = st.form_submit_button("Add Student")
        
        if submitted:
            if name and student_id:
                # Check for duplicate ID
                if any(s.student_id == student_id for s in st.session_state.students):
                    st.error(f"Student ID **{student_id}** already exists. Please use a unique ID.")
                else:
                    new_student = Student(name, student_id, fees)
                    
                    # Store data directly in the session variable
                    st.session_state.students.append(new_student)
                    
                    st.success(f"Student **{name}** (ID: {student_id}) added successfully!")
                    st.rerun() # Rerun to clear form and update view
            else:
                st.error("Name and ID are required.")

# --- 3. Update Fees (Replaces update_fees CLI logic) ---
elif menu_choice == 'Update Fees':
    st.header("💸 Update Fees Payment")
    
    # Get available IDs for selection
    id_list = [s.student_id for s in st.session_state.students]
    
    if not id_list:
        st.warning("No students available to update fees. Please add a student first.")
    else:
        with st.form("update_fees_form"):
            student_id_to_update = st.selectbox("Select Student ID:", id_list)
            amount_paid = st.number_input("Enter the amount paid:", min_value=0.0, format="%.2f", key="paid_amount")
            
            submitted = st.form_submit_button("Submit Payment")
            
            if submitted:
                found = False
                for student in st.session_state.students:
                    if student.student_id == student_id_to_update:
                        student.fees -= amount_paid
                        st.success(f"Payment of ${amount_paid:.2f} recorded for **{student.student_name}**.")
                        st.info(f"Remaining fees: **${student.fees:.2f}**")
                        found = True
                        break
                
                if not found:
                    # This should ideally not happen if ID comes from selectbox
                    st.error(f"Student with ID **{student_id_to_update}** not found.")
                
                # Data is updated in st.session_state, no file I/O needed
                st.rerun()

# --- 4. Display Single Student Details ---
elif menu_choice == 'Display Single Student Details':
    st.header("🔎 Student Details & Due Fees")
    
    id_list = [s.student_id for s in st.session_state.students]
    
    if not id_list:
        st.warning("No students available to display details.")
    else:
        selected_id = st.selectbox("Select Student ID:", id_list)

        if selected_id:
            # Find the student object in the list
            found_student = next((s for s in st.session_state.students if s.student_id == selected_id), None)
            
            if found_student:
                st.markdown("### Information")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(label="Student Name", value=found_student.student_name)
                with col2:
                    st.metric(label="Student ID", value=found_student.student_id)
                with col3:
                    st.metric(label="Fees Due", value=f"${found_student.fees:.2f}", delta="Remaining Balance")
            # If not found (unlikely if selected from the list)
            # st.warning(f"Data for ID {selected_id} not found.")

# --- STREAMLIT APP END ---
