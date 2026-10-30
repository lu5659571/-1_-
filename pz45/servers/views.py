from django.shortcuts import render
from .singleton import DatabaseConnectionManager, AuditLogger, SlowQueryMonitor
from .models import ServerFactory, AuditEventFactory, QueryReportFactory


def index(request):
    # --- 1. СЕРВЕРЫ СУБД ---
    db_mgr1 = DatabaseConnectionManager()
    db_mgr2 = DatabaseConnectionManager()
    is_singleton_db = id(db_mgr1) == id(db_mgr2)
    db_mgr1.get_connection("postgresql")

    pg_server = ServerFactory.create_server("postgresql", "MainDB", "192.168.1.10")
    mysql_server = ServerFactory.create_server("mysql", "DevDB", "192.168.1.20", 3307)

    # --- 2. АУДИТ ---
    audit1 = AuditLogger()
    audit2 = AuditLogger()
    is_singleton_audit = id(audit1) == id(audit2)
    audit1.log("User admin logged in")

    select_event = AuditEventFactory.create_event("select", "SELECT * FROM users")

    # --- 3. МЕДЛЕННЫЕ ЗАПРОСЫ ---
    slow_q1 = SlowQueryMonitor()
    slow_q2 = SlowQueryMonitor()
    is_singleton_slow = id(slow_q1) == id(slow_q2)
    slow_q1.add_query("SELECT * FROM big_table", 5.2)

    daily_rep = QueryReportFactory.create_report("daily")

    # Собираем все данные в словарь, чтобы отправить в HTML
    context = {
        'is_singleton_db': is_singleton_db,
        'pg_info': pg_server.get_info(),
        'mysql_info': mysql_server.get_info(),

        'is_singleton_audit': is_singleton_audit,
        'audit_logs': audit2.logs,
        'select_event': select_event.get_description(),

        'is_singleton_slow': is_singleton_slow,
        'slow_queries': slow_q2.slow_queries,
        'daily_report': daily_rep.generate()
    }

    return render(request, 'index.html', context)