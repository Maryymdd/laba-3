import unittest
from unittest.mock import patch, mock_open
from main import validate_phone, search_in_text, search_in_url, search_in_file

class TestValidatePhone(unittest.TestCase):
    def test_valid_phone_numbers(self):
        valid_numbers = [
            "+7 123 456-78-90",
            "8 (123) 456 78 90",
            "1234567890",
            "+71234567890",
            "7 123 456-78-90"
        ]
        for number in valid_numbers:
            with self.subTest(number=number):
                self.assertTrue(validate_phone(number), f"Должно быть True для {number}")

    def test_invalid_phone_numbers(self):
        invalid_numbers = [
            "123-45-678",
            "+1 234 567 890",
            "abcdefg",
            "1234567",
            "+7 (123) 456-78901"
        ]
        for number in invalid_numbers:
            with self.subTest(number=number):
                self.assertFalse(validate_phone(number), f"Должно быть False для {number}")

class TestSearchInText(unittest.TestCase):
    def test_search_with_phone_numbers(self):
        text = """
        Здесь есть несколько номеров:
        +7 123 456-78-90,
        8 (987) 654-32-10 и
        +71234567890.
        """
        expected = ["+7 123 456-78-90", "8 (987) 654-32-10", "+71234567890"]
        result = search_in_text(text)
        self.assertEqual(result, expected)

    def test_search_without_phone_numbers(self):
        text = "В этом тексте нет номеров телефонов."
        result = search_in_text(text)
        self.assertEqual(result, [])

class TestSearchInURL(unittest.TestCase):
    @patch('main.requests.get')
    def test_search_in_url_success(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                Контакты: +7 123 456-78-90 и 8 (987) 654-32-10.
            </body>
        </html>
        """
        expected = ["+7 123 456-78-90", "8 (987) 654-32-10"]
        result = search_in_url("http://example.com")
        self.assertEqual(result, expected)
        mock_get.assert_called_once_with("http://example.com")

    @patch('main.requests.get')
    def test_search_in_url_failure(self, mock_get):
        mock_get.side_effect = requests.RequestException("Ошибка сети")
        result = search_in_url("http://invalid-url.com")
        self.assertEqual(result, [])

class TestSearchInFile(unittest.TestCase):
    def test_search_in_file_success(self):
        mock_file_content = """
        Здесь есть номера:
        +7 123 456-78-90
        8 (987) 654-32-10
        """
        with patch('main.open', mock_open(read_data=mock_file_content)):
            expected = ["+7 123 456-78-90", "8 (987) 654-32-10"]
            result = search_in_file("dummy_path.txt")
            self.assertEqual(result, expected)

    def test_search_in_file_failure(self):
        with patch('main.open', side_effect=IOError("Не удалось открыть файл")):
            result = search_in_file("nonexistent_file.txt")
            self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
