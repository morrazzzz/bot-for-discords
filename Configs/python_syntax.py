from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QTextCharFormat, QColor, QSyntaxHighlighter


class PythonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlight_rules = []
        
        # Ключевые слова Python
        keywords = ["False", "None", "True", "and", "as", "assert", "async", "await", "break", "class", "continue",
                    "def", "del", "elif", "else", "except", "finally", "for", "from", "global", "if", "import",
                    "in", "is", "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try", "while", "with",
                    "yield"]
        
        # Зарезервированные слова Python
        reserved_words = ["True", "False", "None"]
        
        # Операторы Python
        operators = ["+", "-", "*", "/", "//", "%", "**", "=", "+=", "-=", "*=", "/=", "//=", "%=", "**=",
                     "==", "!=", "<", "<=", ">", ">=", "and", "or", "not"]
        
        # Комментарии Python
        comments = ["#"]
        
        # Строковые литералы Python
        string_literals = ["'", "\""]
        
        # Подсветка ключевых слов
        self.highlight_rules += [(r"\b{}\b".format(keyword), "keyword") for keyword in keywords]
        
        # Подсветка зарезервированных слов
        self.highlight_rules += [(r"\b{}\b".format(reserved_word), "reserved") for reserved_word in reserved_words]
        
        # Подсветка операторов
        self.highlight_rules += [(r"{}".format(operator), "operator") for operator in operators]
        
        # Подсветка комментариев
        self.highlight_rules += [(r"{}[^\n]*".format(comment), "comment") for comment in comments]
        
        # Подсветка строковых литералов
        self.highlight_rules += [(r"{}.*?{}".format(string_literal, string_literal), "string") for string_literal in string_literals]

    def highlightBlock(self, text):
        for pattern, color_name in self.highlight_rules:
            format_ = QTextCharFormat()
            format_.setForeground(QColor(color_name))
            
            regex = QRegExp(pattern)
            i = regex.indexIn(text)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(i, length, format_)
                i = regex.indexIn(text, i + length)
        
        self.setCurrentBlockState(0)