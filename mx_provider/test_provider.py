from mx_provider import providers


def test_create_database():
    providers.create_database()
    con = providers.sqlite3.connect("providers.db")
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='providers'")
    assert cur.fetchone() is not None
    con.close()


def test_add_provider():
    providers.add_provider("example.com", "mail.example.com", "Example")
    con = providers.sqlite3.connect("providers.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM providers WHERE domain = 'example.com'")
    assert cur.fetchone() == ("example.com", "mail.example.com", "Example")
    con.close()


def test_search_mx():
    assert providers.search_mx("example.com") == ("mail.example.com",)


def test_search_domain():
    assert providers.search_domain("Example") == ("example.com",)


def test_search_all():
    assert providers.search_all() == [("example.com", "mail.example.com", "Example")]


def test_update_provider():
    providers.update_provider("example.com", "mail.example.com", "Example2")
    con = providers.sqlite3.connect("providers.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM providers WHERE domain = 'example.com'")
    assert cur.fetchone() == ("example.com", "mail.example.com", "Example2")
    con.close()


def test_update_mx():
    providers.update_mx("example.com", "mail2.example.com")
    con = providers.sqlite3.connect("providers.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM providers WHERE domain = 'example.com'")
    assert cur.fetchone() == ("example.com", "mail2.example.com", "Example2")
    con.close()


def test_remove_provider():
    providers.remove_provider("example.com")
    con = providers.sqlite3.connect("providers.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM providers WHERE domain = 'example.com'")
    assert cur.fetchone() is None
    con.close()

