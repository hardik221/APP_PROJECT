from MockDB import MockDb
from mock import patch
import utils
class TestDB(MockDb):
    def test_insertBookType(self):
        with self.mock_db_config:
            self.assertEqual(utils.db_write("INSERT INTO bookType (id, bookType) VALUES ('3', 'fun')"), True)

    def test_insertBook(self):
        with self.mock_db_config:
            self.assertEqual(utils.db_write("INSERT INTO book (id, title, pageCount,isEbook,typeId) VALUES ('24', 'Three series', 450, 'true', '1')"), True)

    def test_insertPublish(self):
        with self.mock_db_config:
            self.assertEqual(utils.db_write(
                "INSERT INTO publish (id, publisher, publishedDate,description,bookId) "
                "VALUES ('23', 'John', 28-08-1997, 'John has published the book', '11')"), True)

    def test_findByName(self):
        with self.mock_db_config:
            self.assertEqual(utils.db_read("SELECT * FROM bookType where bookType LIKE '%%love%%'"), [{'bookType': 'love', 'id': '1'}])

    def test_findAll(self):
        with self.mock_db_config:
            self.assertEqual(utils.db_read("SELECT * FROM bookType"), [{'bookType': 'love', 'id': '1'}, {'bookType': 'fantasy', 'id': '2'}])

    def test_update(self):
        with self.mock_db_config:
            self.assertEqual(utils.db_read("UPDATE bookType SET bookType='fun' WHERE id = '2'"), [])

    def test_deleteById(self):
        with self.mock_db_config:
            self.assertEqual(utils.db_read("DELETE p, b FROM Publish p INNER JOIN Book b on p.bookId = b.id where  b.id = '11'"), [])

    def test_deleteById(self):
        with self.mock_db_config:
            self.assertEqual(
                utils.db_read("SHOW columns FROM bookType"), [{'Default': None,
                                                              'Extra': '',
                                                              'Field': 'id',
                                                              'Key': 'PRI',
                                                              'Null': 'NO',
                                                              'Type': b'varchar(255)'},
                                                             {'Default': None,
                                                              'Extra': '',
                                                              'Field': 'bookType',
                                                              'Key': '',
                                                              'Null': 'YES',
                                                              'Type': b'varchar(255)'}])
