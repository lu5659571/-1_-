# учет серверов СУБД вариант 1

class DatabaseServer:
    def __init__(self, name: str, ip_address: str, port: int = None):
        self.name = name
        self.ip_address = ip_address
        self.port = port
    def get_info(self) -> str:
        raise NotImplementedError()

class PostgreSQLServer(DatabaseServer):
    def get_info(self) -> str:
        return f"PostgreSQL: {self.name} ({self.ip_address}:{self.port or 5432})"

class MySQLServer(DatabaseServer):
    def get_info(self) -> str:
        return f"MySQL: {self.name} ({self.ip_address}:{self.port or 3306})"

class ServerFactory:
    _registry = {"postgresql": PostgreSQLServer, "mysql": MySQLServer}
    @classmethod
    def create_server(cls, server_type, name, ip_address, port=None):
        if server_type not in cls._registry:
            raise ValueError(f"Неизвестный тип сервера: {server_type}")
        return cls._registry[server_type](name, ip_address, port)

# аудит действий в БД вариант 6

class AuditEvent:
    def __init__(self, query: str):
        self.query = query
    def get_description(self) -> str:
        raise NotImplementedError()

class SelectEvent(AuditEvent):
    def get_description(self) -> str:
        return f"SELECT query executed: {self.query}"

class InsertEvent(AuditEvent):
    def get_description(self) -> str:
        return f"INSERT query executed: {self.query}"

class AuditEventFactory:
    _registry = {"select": SelectEvent, "insert": InsertEvent}
    @classmethod
    def create_event(cls, event_type, query):
        if event_type not in cls._registry:
            raise ValueError(f"Unknown event: {event_type}")
        return cls._registry[event_type](query)

# мониторинг медленных запросов вариант 11

class Report:
    def generate(self) -> str:
        raise NotImplementedError()

class DailyReport(Report):
    def generate(self): return "Generating DAILY report of slow queries."

class WeeklyReport(Report):
    def generate(self): return "Generating WEEKLY report of slow queries."

class QueryReportFactory:
    _registry = {"daily": DailyReport, "weekly": WeeklyReport}
    @classmethod
    def create_report(cls, report_type):
        if report_type not in cls._registry:
            raise ValueError("Unknown report type")
        return cls._registry[report_type]()