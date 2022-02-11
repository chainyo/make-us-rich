import psycopg2

from typing import Any, Dict

from make_us_rich.utils import random_string, load_env


class DatabaseHandler:
    """
    This class handles the database connection and the queries.
    """

    @classmethod
    def authentication(cls, username:str, password:str) -> Dict[str, bool]:
        """
        Checks if the user and password are correct

        Parameters
        ----------
        username: str
            The username of the user.
        password: str
            The password of the user.
        
        Returns
        -------
        dict:
            A dictionary with the success of the authentication.
        """
        try:
            cls._connect()
            cursor = cls.connection.cursor()
            cursor.execute(f"""
                SELECT id FROM users WHERE username = '{username}' AND password = crypt('{password}', password);
            """)
            match = cursor.fetchone()
            cls._disconnect()
            return {
                "success": True, "message": "Authentication successful.", "username": username
            } if match else {"success": False}
        except Exception as e: 
            return {"error": str(e)}


    @classmethod
    def create_user(cls, username:str, password:str) -> Dict[str, Any]:
        """
        Creates a new user in the database.

        Parameters
        ----------
        username: str
            The username of the new user.
        password: str
            The password of the new user.
        
        Returns
        -------
        dict:
            A dictionary with the success of the creation.
        """
        try:
            cls._connect()
            cursor = cls.connection.cursor()
            cursor.execute(f"""
                INSERT INTO users (username, password)
                VALUES ('{username}', crypt('{password}', gen_salt('bf'))) 
                ON CONFLICT (username) DO NOTHING;
            """)
            cls.connection.commit()
            cls._disconnect()
            cls._add_member_role_to_user(username)
            cls._generate_token_for_user(username)
            cls._init_api_limit_for_user(username)
            return {
                "success": True, "message": "User created successfully.", "username": username,
            }
        except Exception as e: 
            return {"success": False, "message": str(e)}

    
    @classmethod
    def check_if_user_exist(cls, username:str) -> Dict[str, Any]:
        """
        Checks if a user exists in the database.

        Parameters
        ----------
        username: str
            The username of the user.

        Returns
        -------
        dict:
            A dictionary with the success of the check.
        """
        try:
            cls._connect()
            cursor = cls.connection.cursor()
            cursor.execute(f"""
                SELECT id FROM users WHERE username = '{username}';
            """)
            match = cursor.fetchone()
            cls._disconnect()
            return {"success": True} if match else {"success": False}
        except Exception as e:
            return {"error": str(e)}

    
    @classmethod
    def get_api_token(cls, username:str) -> Dict[str, str]:
        """
        Gets the API token of a user.

        Parameters
        ----------
        username: str
            The username of the user.
        
        Returns
        -------
        dict:
            A dictionary with the API token of the user.
        """
        try:
            cls._connect()
            cursor = cls.connection.cursor()
            cursor.execute(f"""
                SELECT token FROM api_tokens
                JOIN users ON users.id = api_tokens.user_id
                WHERE users.username = '{username}';
            """)
            token = cursor.fetchone()
            cls._disconnect()
            return {"success": True, "token": token[0]} if token else {"success": False}
        except Exception as e:
            return {"error": str(e)}

    
    @classmethod
    def increment_user_api_consumption(cls, username:str) -> Dict[str, Any]:
        """
        Increments the API consumption of a user.

        Parameters
        ----------
        username: str
            The username of the user.
        
        Returns
        -------
        dict:
            A dictionary with the success of the increment.
        """
        try:
            cls._connect()
            cursor = cls.connection.cursor()
            cursor.execute(f"""
                UPDATE user_api_consumptions SET api_consumption = api_consumption + 1
                WHERE user_id = (SELECT id FROM users WHERE username = '{username}');
            """)
            cls.connection.commit()
            cls._disconnect()
            return {"success": True}
        except Exception as e:
            return {"error": str(e)}

    
    @classmethod
    def get_user_api_consumption(cls, username:str) -> Dict[str, Any]:
        """
        Gets the API consumption of a user.

        Parameters
        ----------
        username: str
            The username of the user.
        
        Returns
        -------
        dict:
            A dictionary with the API consumption of the user.
        """
        try:
            cls._connect()
            cursor = cls.connection.cursor()
            cursor.execute(f"""
                SELECT api_consumption FROM user_api_consumptions
                WHERE user_id = (SELECT id FROM users WHERE username = '{username}');
            """)
            consumption = cursor.fetchone()
            cls._disconnect()
            return {"success": True, "consumption": consumption[0]}
        except Exception as e:
            return {"error": str(e)}


    @classmethod
    def _check_user_role(cls, username:str) -> Dict[str, str]:
        """
        Checks the role of the user.

        Parameters
        ----------
        username: str
            The username of the user.
        
        Returns
        -------
        dict:
            A dictionary with the role of the user.
        """
        try:
            cls._connect()  
            cursor = cls.connection.cursor()          
            cursor.execute(f"""
                SELECT name FROM user_roles
                JOIN users ON users.id = user_roles.user_id
                JOIN roles ON roles.id = user_roles.role_id
                WHERE users.username = '{username}'; 
            """)
            role = cursor.fetchone()[0]
            cls._disconnect()
            return {"role": role}
        except Exception as e: 
            return {"error": str(e)}


    @classmethod
    def _add_member_role_to_user(cls, username:str) -> Dict[str, Any]:
        """
        Adds the role of the user to the database.

        Parameters
        ----------
        username: str
            The username of the user.
        
        Returns
        -------
        dict:
            A dictionary with the success of the creation.
        """
        try:
            cls._connect()
            cursor = cls.connection.cursor()
            cursor.execute(f"""
                INSERT INTO user_roles (user_id, role_id)
                SELECT u.id, r.id
                FROM (SELECT id FROM users WHERE username = '{username}') u,
                (SELECT id FROM roles WHERE name = 'member') r;
            """)
            cls.connection.commit()
            cls._disconnect()
            return {"success": True}
        except Exception as e: 
            return {"success": False, "message": str(e)}
    

    @classmethod
    def _generate_token_for_user(cls, username:str) -> Dict[str, Any]:
        """
        Generates a token for the user.

        Parameters
        ----------
        username: str
            The username of the user.
        
        Returns
        -------
        str:
            The token of the user.
        """
        token = random_string()
        try:
            cls._connect()
            cursor = cls.connection.cursor()
            cursor.execute(f"""
                INSERT INTO api_tokens (user_id, token)
                SELECT u.id, '{token}'
                FROM (SELECT id FROM users WHERE username = '{username}') u;
            """)
            cls.connection.commit()
            cls._disconnect()
            return {"success": True}
        except Exception as e: 
            return {"success": False, "message": str(e)}

    
    @classmethod
    def _init_api_limit_for_user(cls, username:str) -> Dict[str, Any]:
        """
        Initializes the API limit for the user.

        Parameters
        ----------
        username: str
            The username of the user.
        
        Returns
        -------
        dict:
            A dictionary with the success of the creation.
        """
        try:
            cls._connect()
            cursor = cls.connection.cursor()
            cursor.execute(f"""
                INSERT INTO user_api_consumptions (user_id, api_consumption)
                SELECT u.id, 0
                FROM (SELECT id FROM users WHERE username = '{username}') u;
            """)
            cls.connection.commit()
            cls._disconnect()
            return {"success": True}
        except Exception as e: 
            return {"success": False, "message": str(e)}
    

    @classmethod
    def _connect(cls):
        """
        Connects to the database.
        """
        try:
            _config = load_env("postgres")
            database = _config["DATABASE"]
            user = _config["USER"]
            host = _config["HOST"]
            password = _config["PWD"]
            cls.connection = psycopg2.connect(
                database=database,
                user=user,
                host=host,
                password=password
            )
        except Exception as e:
            return e

    
    @classmethod
    def _disconnect(cls):
        """
        Closes the connection to the database.
        """
        try:
            cls.connection.close()
        except Exception as e:
            return e
