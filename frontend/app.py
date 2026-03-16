import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Recruitment System", layout="wide")

st.markdown("""
# AI Recruitment System
### Smart AI Candidate Screening Platform
""")

# =========================
# SESSION DEFAULTS
# =========================
if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.token = None
    
# Store resume matching results
if "match_results" not in st.session_state:
    st.session_state.match_results = []    

if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0

# =========================
# API HELPERS
# =========================
def get_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}


def safe_get(url):
    try:
        res = requests.get(url, headers=get_headers())
        if res.status_code == 200:
            return res.json()
        else:
            return None
    except Exception:
        st.error("Backend not reachable")


def safe_post(url, data=None, files=None):
    try:
        res = requests.post(url, data=data, files=files, headers=get_headers())

        if res.status_code == 200:
            return res.json()
        else:
            st.error(res.text)   # show backend error
            return None

    except Exception as e:
        st.error(str(e))

# =========================
# LOGIN + SIGNUP + FORGOT
# =========================
if not st.session_state.login:

    st.subheader("🔐 Authentication")

    tab1, tab2, tab3 = st.tabs(["Login", "Signup", "Forgot Password"])

    # -----------------
    # LOGIN
    # -----------------
    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            res = requests.post(
                "http://127.0.0.1:8000/login",
                data={"username": username, "password": password},
            )

            data = res.json()

            if "access_token" in data:
                st.session_state.login = True
                st.session_state.role = data["role"]
                st.session_state.username = username
                st.session_state.token = data["access_token"]
                st.rerun()
            else:
                st.error("Invalid login")

    # -----------------
    # SIGNUP
    # -----------------
    with tab2:
        new_user = st.text_input("Username")
        new_email = st.text_input("Email")
        new_pass = st.text_input("Password", type="password")

        if st.button("Signup"):
            res = requests.post(
                "http://127.0.0.1:8000/signup",
                data={
                    "username": new_user,
                    "email": new_email,
                    "password": new_pass,
                },
            )

            if res.status_code == 200:
                st.success("Signup successful")
            else:
                st.error(res.text)

    # -----------------
    # FORGOT PASSWORD
    # -----------------
    with tab3:

        email = st.text_input("Enter your registered email")

        if st.button("Send OTP"):
            res = requests.post(
                "http://127.0.0.1:8000/forgot_password",
                data={"email": email},
            )

            if res.status_code == 200:
                st.success("OTP sent to email")

        otp = st.text_input("Enter OTP")
        new_password = st.text_input("New Password", type="password")

        if st.button("Reset Password"):
            verify = requests.post(
                "http://127.0.0.1:8000/verify_otp",
                data={"email": email, "otp": otp},
            )

            if verify.status_code == 200:
                reset = requests.post(
                    "http://127.0.0.1:8000/reset_password",
                    data={
                        "email": email,
                        "new_password": new_password,
                    },
                )

                if reset.status_code == 200:
                    st.success("Password reset successful")
                else:
                    st.error("Reset failed")
            else:
                st.error("Invalid OTP")

    st.stop()


# =========================
# SIDEBAR
# =========================
menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📄 Resume Matching",
        "👩‍💼 Candidates",
        "⭐ Recommendations",
        "🔍 Search",
        "📊 Analytics",
    ],
)

st.sidebar.markdown("---")
st.sidebar.write("👤 User:", st.session_state.username)
st.sidebar.write("🔑 Role:", st.session_state.role)

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()


# =========================
# DASHBOARD
# =========================
if menu == "🏠 Dashboard":

    st.subheader("📊 System Overview")

    data = safe_get("http://127.0.0.1:8000/analytics")

    if data:
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Candidates", data.get("total_candidates", 0))

        skills = data.get("skill_distribution", {})
        top = max(skills, key=skills.get) if skills else "N/A"
        col2.metric("Top Skill", top)

        scores = data.get("scores", [])
        avg = round(sum(scores) / len(scores), 2) if scores else 0
        col3.metric("Avg Score", avg)

    # =========================
    # UPCOMING INTERVIEWS
    # =========================
    st.markdown("## 📅 Upcoming Interviews")

    upcoming = safe_get(
        "http://127.0.0.1:8000/upcoming_interviews"
    )

    if upcoming:
        df = pd.DataFrame(upcoming)
        st.dataframe(df)

    else:
        st.info("No upcoming interviews")

# =========================
# RESUME MATCHING
# =========================
elif menu == "📄 Resume Matching":

    st.subheader("Upload Resumes & Match")

    # File uploader
    files = st.file_uploader(
        "Upload Resume(s)",
        type=["pdf"],
        accept_multiple_files=True,
        key=f"resume_files_{st.session_state.reset_counter}"
    )

    # Job description
    job = st.text_area(
        "Job Description",
        key=f"job_description_{st.session_state.reset_counter}"
    )

    # ======================
    # MATCH BUTTON
    # ======================
    if st.button("Match Candidates"):

        if files and job:

            results = []

            with st.spinner("Running AI Matching..."):

                for file in files:

                    data = safe_post(
                        "http://127.0.0.1:8000/match",
                        data={"job_description": job},
                        files={"file": file},
                    )

                    if data:

                        explanation = data.get("explanation", {})

                        results.append({
                            "Candidate": file.name,
                            "Score": round(data.get("score", 0), 3),
                            "Matched Skills": ", ".join(
                                explanation.get("matched_skills", [])
                            ),
                            "Missing Skills": ", ".join(
                                explanation.get("missing_skills", [])
                            ),
                        })

            # Save results to session
            st.session_state.match_results = results

        else:
            st.warning("Upload resumes and enter job description")

    # ======================
    # SHOW RESULTS
    # ======================
    if st.session_state.get("match_results"):

        st.success("Matching Completed")

        df = pd.DataFrame(st.session_state.match_results)

        df = df.sort_values("Score", ascending=False).reset_index(drop=True)

        # Add rank column
        df.insert(0, "Rank", range(1, len(df) + 1))

        st.dataframe(df, width="stretch", hide_index=True)

        # ======================
        # CLEAR RESULTS BUTTON
        # ======================
        if st.button("Clear Results"):

           st.session_state.match_results = []

        # change widget keys to reset them
           st.session_state.reset_counter += 1

           st.rerun()
# =========================
# CANDIDATES
# =========================
elif menu == "👩‍💼 Candidates":

    st.subheader("Candidate List")

    candidates = safe_get("http://127.0.0.1:8000/ranked_candidates")

    if not candidates:
        st.warning("No candidates")

    else:
        for c in candidates:

            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

            # ------------------
            # Candidate Info
            # ------------------
            with col1:
                st.write(f"### {c.get('name')}")
                st.write("Email:", c.get("email"))
                st.write("Score:", round(c.get("score", 0), 3))
                st.write("Skills:", c.get("skills", []))

                # Status display
                status = c.get("status", "AI Recommended")

                if status == "Approved":
                    st.success(f"Status: {status}")
                elif status == "Denied":
                    st.error(f"Status: {status}")
                else:
                    st.info(f"Status: {status}")

                # ------------------
                # Interview display
                # ------------------
                interview = safe_get(
                    f"http://127.0.0.1:8000/interview/{c['_id']}"
                )

                if interview:
                    st.markdown("📅 **Interview Scheduled**")
                    st.write("Date:", interview.get("date"))
                    st.write("Time:", interview.get("time"))

            # ------------------
            # Status dropdown
            # ------------------
            if st.session_state.role in ["admin", "recruiter"]:
                with col2:

                    options = ["AI Recommended", "Approved", "Denied"]
                    current = c.get("status", "AI Recommended")

                    selected = st.selectbox(
                        "Status",
                        options,
                        index=options.index(current),
                        key=f"status_{c['_id']}",
                    )

                    if st.button("Update", key=f"update_{c['_id']}"):
                        safe_post(
                            f"http://127.0.0.1:8000/update_status/{c['_id']}",
                            data={"status": selected},
                        )
                        st.success("Updated")
                        st.rerun()

            # ------------------
            # Interview scheduling
            # ------------------
            if st.session_state.role in ["admin", "recruiter"]:
                with col3:
                    date = st.date_input("Date", key=f"d_{c['_id']}")
                    time = st.time_input("Time", key=f"t_{c['_id']}")

                    if st.button("Schedule", key=f"s_{c['_id']}"):
                        safe_post(
                            f"http://127.0.0.1:8000/schedule_interview/{c['_id']}",
                            data={"date": str(date), "time": str(time)},
                        )
                        st.success("Interview Scheduled")
                        st.rerun()

            # ------------------
            # Delete
            # ------------------
            if st.session_state.role == "admin":
                with col4:
                    if st.button("Delete", key=f"del_{c['_id']}"):
                        requests.delete(
                            f"http://127.0.0.1:8000/delete_candidate/{c['_id']}",
                            headers=get_headers(),
                        )
                        st.success("Deleted")
                        st.rerun()

            st.markdown("---")
    # =========================
    # DELETE ALL (Admin Only)
    # =========================
    if st.session_state.role == "admin":

        st.markdown("### ⚠️ Admin Controls")

        confirm = st.checkbox("Confirm delete all candidates")

        if st.button("🗑 Delete All Candidates"):

            if confirm:
                response = requests.delete(
                    "http://127.0.0.1:8000/clear_all",
                    headers=get_headers()
                )

                if response.status_code == 200:
                    st.success("All candidates deleted successfully")
                    st.rerun()
                else:
                    st.error("Delete failed")
            else:
                st.warning("Please confirm before deleting.")

# =========================
# RECOMMENDATIONS
# =========================
elif menu == "⭐ Recommendations":

    st.subheader("Top AI Recommendations")

    limit = st.slider("Top Candidates", 1, 10, 5)

    rec = safe_get(
        f"http://127.0.0.1:8000/recommend_candidates?limit={limit}"
    )

    if rec:
        for r in rec:
            st.write(f"### {r.get('name')}")
            st.write("Score:", round(r.get("score", 0), 3))
            st.write("Skills:", r.get("skills", []))
            st.markdown("---")


# =========================
# SEARCH
# =========================
elif menu == "🔍 Search":

    st.subheader("Search Candidates")

    skill = st.text_input("Enter Skill")

    if st.button("Search"):

        results = safe_get(
            f"http://127.0.0.1:8000/search_candidates?skill={skill}"
        )

        if results:
            for r in results:
                st.write(f"### {r.get('name')}")
                st.write("Skills:", r.get("skills", []))
                st.markdown("---")


# =========================
# ANALYTICS
# =========================
elif menu == "📊 Analytics":

    st.subheader("AI Analytics")

    data = safe_get("http://127.0.0.1:8000/analytics")

    if data:

        skills = data.get("skill_distribution", {})

        if skills:
            df = pd.DataFrame(skills.items(), columns=["Skill", "Count"])
            st.dataframe(df)

            plt.figure()
            plt.bar(df["Skill"], df["Count"])
            plt.xticks(rotation=45)
            st.pyplot(plt)

        scores = data.get("scores", [])

        if scores:
            plt.figure()
            plt.hist(scores)
            st.pyplot(plt)