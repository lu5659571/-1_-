# учет серверов СУБД вариант 1

class DatabaseConnectionManager:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connections = {}
        return cls._instance

    def get_connection(self, db_type: str) -> str:
        if db_type not in self.connections:
            self.connections[db_type] = f"Connection to {db_type}"
        return self.connections[db_type]


# аудит действий в БД вариант 6

class AuditLogger:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logs = []
        return cls._instance

    def log(self, event: str):
        self.logs.append(event)
        return f"Logged: {event}"


# мониторинг медленных запросов вариант 11

class SlowQueryMonitor:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.slow_queries = []
        return cls._instance

    def add_query(self, query: str, time: float):
        self.slow_queries.append({"query": query, "time": time})
        return f"Added slow query: {query} ({time}s)"