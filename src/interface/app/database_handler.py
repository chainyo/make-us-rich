import os
import psycopg2

from dotenv import load_dotenv
from typing import Any, Dict


load_dotenv()


class DatabaseHandler:
    """
    Interface to the database.
    """
    def __init__(self):
        self.db_name = os.getenv("DB_NAME")
        self.db_user = os.getenv("DB_USER")
        self.db_host = os.getenv("DB_HOST")
        self.db_password = os.getenv("DB_PASSWORD")


    def authentication(self, username:str, password:str) -> Dict[str, bool]:
        """
        Checks if the user and password are correct

        Parameters:
        -----------
        username: str
            The username of the user.
        password: str
            The password of the user.
        
        Returns:
        --------
        dict:
            A dictionary with the success of the authentication.
        """
        try:
            self._connect()
            cur = self.conn.cursor()
            cur.execute(f"""
                SELECT id FROM users WHERE username = '{username}' AND password = crypt('{password}', password);
            """)
            match = cur.fetchone()
            self._disconnect()
            return {"success": True} if match else {"success": False}
        except Exception as e: 
            return {"error": str(e)}


    def create_user(self, username:str, password:str) -> Dict[str, Any]:
        """
        Creates a new user in the database.

        Parameters:
        -----------
        username: str
            The username of the new user.
        password: str
            The password of the new user.
        
        Returns:
        --------
        dict:
            A dictionary with the success of the creation.
        """
        try:
            self._connect()
            cur = self.conn.cursor()
            cur.execute(f"""
                INSERT INTO users (username, password)
                VALUES ('{username}', crypt('{password}', gen_salt('bf'))) 
                ON CONFLICT (username) DO NOTHING;
            """)
            self.conn.commit()
            self._disconnect()
            self._add_member_role_to_user(username)
            return {
                "success": True, "message": "User created successfully.", "username": username,
            }
        except Exception as e: 
            return {"success": False, "message": str(e)}


    def _add_member_role_to_user(self, username:str) -> Dict[str, Any]:
        """
        Adds the role of the user to the database.

        Parameters:
        -----------
        username: str
            The username of the user.
        
        Returns:
        --------
        dict:
            A dictionary with the success of the creation.
        """
        try:
            self._connect()
            cur = self.conn.cursor()
            cur.execute(f"""
                INSERT INTO user_roles (user_id, role_id)
                SELECT u.id, r.id
                FROM (SELECT id FROM users WHERE username = '{username}') u,
                (SELECT id FROM roles WHERE name = 'member') r;
            """)
            self.conn.commit()
            self._disconnect()
            return {"success": True}
        except Exception as e: 
            return {"success": False, "message": str(e)}
    
    def _check_user_role(self, username:str) -> Dict[str, str]:
        """
        Checks the role of the user.

        Parameters:
        -----------
        username: str
            The username of the user.
        
        Returns:
        --------
        dict:
            A dictionary with the role of the user.
        """
        try:
            self._connect()
            cur = self.conn.cursor()
            cur.execute(f"""
                SELECT name FROM user_roles
                JOIN users ON users.id = user_roles.user_id
                JOIN roles ON roles.id = user_roles.role_id
                WHERE users.username = '{username}'; 
            """)
            role = cur.fetchone()[0]
            self._disconnect()
            return {"role": role}
        except Exception as e: 
            return {"error": str(e)}


    def _connect(self):
        """
        Connect to the database.
        """
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                host=self.db_host,
                password=self.db_password
            )
            self.cur
        except Exception as e:
            return e


    def _disconnect(self):
        """
        Disconnect from the database.
        """
        self.conn.close()
