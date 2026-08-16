import re
import bcrypt
import streamlit as st

from database.database import (
    create_user,
    get_user_by_email
)


# --------------------------------------------------
# Password functions
# --------------------------------------------------

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    """

    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(
        password_bytes,
        salt
    )

    return hashed.decode("utf-8")


def verify_password(
    password: str,
    password_hash: str
) -> bool:
    """
    Verify a plain password against a bcrypt hash.
    """

    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    )


# --------------------------------------------------
# Email validation
# --------------------------------------------------

def is_valid_email(email: str) -> bool:
    """
    Basic email validation.
    """

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return re.match(
        pattern,
        email
    ) is not None


# --------------------------------------------------
# Login state
# --------------------------------------------------

def initialize_session() -> None:
    """
    Initialize authentication-related Streamlit
    session state variables.
    """

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    if "user_name" not in st.session_state:
        st.session_state.user_name = None

    if "user_email" not in st.session_state:
        st.session_state.user_email = None


# --------------------------------------------------
# Login
# --------------------------------------------------

def login_user(
    email: str,
    password: str
) -> bool:
    """
    Authenticate a user.

    Returns:
        True if login succeeds.
        False otherwise.
    """

    user = get_user_by_email(email)

    if user is None:
        return False

    if not verify_password(
        password,
        user["password_hash"]
    ):
        return False

    st.session_state.logged_in = True
    st.session_state.user_id = user["id"]
    st.session_state.user_name = user["name"]
    st.session_state.user_email = user["email"]

    return True


# --------------------------------------------------
# Logout
# --------------------------------------------------

def logout_user() -> None:
    """
    Log the current user out.
    """

    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_name = None
    st.session_state.user_email = None

    st.rerun()


# --------------------------------------------------
# Login / Signup UI
# --------------------------------------------------

def show_auth_page() -> None:

    st.title("🏋️ AI Gym Trainer")

    st.caption(
        "Your personal AI-powered fitness assistant"
    )

    st.divider()

    login_tab, signup_tab = st.tabs(
        [
            "🔐 Login",
            "📝 Create Account"
        ]
    )

    # ==============================================
    # LOGIN
    # ==============================================

    with login_tab:

        st.subheader("Welcome Back!")

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            type="primary",
            use_container_width=True
        ):

            email = email.strip().lower()

            if not email or not password:
                st.error(
                    "Please enter your email and password."
                )

            else:

                success = login_user(
                    email,
                    password
                )

                if success:
                    st.success(
                        "Login successful!"
                    )

                    st.rerun()

                else:
                    st.error(
                        "Invalid email or password."
                    )

    # ==============================================
    # SIGN UP
    # ==============================================

    with signup_tab:

        st.subheader("Create Your Account")

        name = st.text_input(
            "Full Name",
            key="signup_name"
        )

        email = st.text_input(
            "Email",
            key="signup_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="signup_confirm_password"
        )

        st.caption(
            "Password must contain at least 8 characters."
        )

        if st.button(
            "Create Account",
            type="primary",
            use_container_width=True
        ):

            name = name.strip()
            email = email.strip().lower()

            # --------------------------------------
            # Validation
            # --------------------------------------

            if not name:
                st.error(
                    "Please enter your name."
                )

            elif not is_valid_email(email):
                st.error(
                    "Please enter a valid email address."
                )

            elif len(password) < 8:
                st.error(
                    "Password must contain at least 8 characters."
                )

            elif password != confirm_password:
                st.error(
                    "Passwords do not match."
                )

            else:

                password_hash = hash_password(
                    password
                )

                created = create_user(
                    name,
                    email,
                    password_hash
                )

                if created:

                    st.success(
                        "Account created successfully! "
                        "You can now login."
                    )

                else:

                    st.error(
                        "An account with this email "
                        "already exists."
                    )