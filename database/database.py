import sqlite3
from pathlib import Path
from typing import Optional


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "gym_trainer.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection() -> sqlite3.Connection:
    """
    Create and return a connection to the SQLite database.
    """

    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )

    # Allows us to access columns by name:
    # user["name"]
    # user["email"]
    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database() -> None:
    """
    Create all required database tables if they don't exist.
    """

    connection = get_connection()

    cursor = connection.cursor()

    # --------------------------------------------------------
    # USERS TABLE
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT NOT NULL UNIQUE,

            password_hash TEXT NOT NULL,

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # --------------------------------------------------------
    # WORKOUTS TABLE
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            exercise TEXT NOT NULL,

            repetitions INTEGER NOT NULL,

            form_score REAL NOT NULL,

            duration REAL NOT NULL,

            feedback TEXT,

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
        )
        """
    )

    # --------------------------------------------------------
    # RUNS TABLE
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            distance REAL NOT NULL,

            duration REAL NOT NULL,

            average_pace REAL,

            route TEXT,

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
        )
        """
    )

    connection.commit()

    connection.close()


# ============================================================
# USER FUNCTIONS
# ============================================================

def create_user(
    name: str,
    email: str,
    password_hash: str
) -> bool:
    """
    Create a new user.

    Returns:
        True  -> User created successfully
        False -> Email already exists
    """

    connection = get_connection()

    try:

        connection.execute(
            """
            INSERT INTO users (
                name,
                email,
                password_hash
            )
            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                password_hash
            )
        )

        connection.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        connection.close()


# ============================================================
# GET USER BY EMAIL
# ============================================================

def get_user_by_email(
    email: str
) -> Optional[sqlite3.Row]:
    """
    Find a user using their email address.

    Returns:
        sqlite3.Row if user exists
        None otherwise
    """

    connection = get_connection()

    user = connection.execute(
        """
        SELECT
            id,
            name,
            email,
            password_hash,
            created_at
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    connection.close()

    return user


# ============================================================
# WORKOUT FUNCTIONS
# ============================================================

def save_workout(
    user_id: int,
    exercise: str,
    repetitions: int,
    form_score: float,
    duration: float,
    feedback: str
) -> int:
    """
    Save a completed workout session.

    Returns:
        ID of the newly created workout.
    """

    connection = get_connection()

    try:

        cursor = connection.execute(
            """
            INSERT INTO workouts (
                user_id,
                exercise,
                repetitions,
                form_score,
                duration,
                feedback
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                exercise,
                repetitions,
                form_score,
                duration,
                feedback
            )
        )

        connection.commit()

        workout_id = cursor.lastrowid

        return workout_id

    finally:

        connection.close()


# ============================================================
# GET USER WORKOUTS
# ============================================================

def get_user_workouts(
    user_id: int
):
    """
    Get all workouts belonging to a specific user.

    Newest workouts are returned first.
    """

    connection = get_connection()

    try:

        workouts = connection.execute(
            """
            SELECT
                id,
                exercise,
                repetitions,
                form_score,
                duration,
                feedback,
                created_at
            FROM workouts
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,)
        ).fetchall()

        return workouts

    finally:

        connection.close()


# ============================================================
# WORKOUT STATISTICS
# ============================================================

def get_workout_statistics(
    user_id: int
):
    """
    Calculate workout statistics for a specific user.

    Returns:
        total_workouts
        total_reps
        average_form
    """

    connection = get_connection()

    try:

        statistics = connection.execute(
            """
            SELECT

                COUNT(*) AS total_workouts,

                COALESCE(
                    SUM(repetitions),
                    0
                ) AS total_reps,

                COALESCE(
                    AVG(form_score),
                    0
                ) AS average_form

            FROM workouts

            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()

        return statistics

    finally:

        connection.close()


# ============================================================
# RUN FUNCTIONS
# ============================================================

def save_run(
    user_id: int,
    distance: float,
    duration: float,
    average_pace: Optional[float],
    route: Optional[str]
) -> int:
    """
    Save a completed running session.

    Args:
        user_id:
            ID of the logged-in user.

        distance:
            Distance in kilometers.

        duration:
            Duration in seconds.

        average_pace:
            Average pace in minutes per kilometer.

        route:
            GPS route data.
    """

    connection = get_connection()

    try:

        cursor = connection.execute(
            """
            INSERT INTO runs (
                user_id,
                distance,
                duration,
                average_pace,
                route
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                distance,
                duration,
                average_pace,
                route
            )
        )

        connection.commit()

        run_id = cursor.lastrowid

        return run_id

    finally:

        connection.close()


# ============================================================
# GET USER RUNS
# ============================================================

def get_user_runs(
    user_id: int
):
    """
    Get all running sessions belonging to a specific user.
    """

    connection = get_connection()

    try:

        runs = connection.execute(
            """
            SELECT
                id,
                distance,
                duration,
                average_pace,
                route,
                created_at
            FROM runs
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,)
        ).fetchall()

        return runs

    finally:

        connection.close()


# ============================================================
# RUN STATISTICS
# ============================================================

def get_run_statistics(
    user_id: int
):
    """
    Calculate running statistics for a specific user.

    Returns:
        total_runs
        total_distance
    """

    connection = get_connection()

    try:

        statistics = connection.execute(
            """
            SELECT

                COUNT(*) AS total_runs,

                COALESCE(
                    SUM(distance),
                    0
                ) AS total_distance

            FROM runs

            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()

        return statistics

    finally:

        connection.close()